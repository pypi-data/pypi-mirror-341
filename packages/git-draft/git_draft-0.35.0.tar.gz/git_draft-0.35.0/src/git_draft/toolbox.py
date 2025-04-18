"""Functionality available to bots"""

from __future__ import annotations

from collections.abc import Callable, Sequence
import logging
from pathlib import PurePosixPath
import tempfile
from typing import Protocol, override

from .git import GitError, Repo


_logger = logging.getLogger(__name__)


class Toolbox:
    """File-system intermediary

    Note that the toolbox is not thread-safe. Concurrent operations should be
    serialized by the caller.
    """

    # TODO: Something similar to https://aider.chat/docs/repomap.html,
    # including inferring the most important files, and allowing returning
    # signature-only versions.

    # TODO: Support a diff-based edit method.
    # https://gist.github.com/noporpoise/16e731849eb1231e86d78f9dfeca3abc

    def __init__(self, visitors: Sequence[ToolVisitor] | None = None) -> None:
        self._visitors = visitors or []

    def _dispatch(self, effect: Callable[[ToolVisitor], None]) -> None:
        for visitor in self._visitors:
            effect(visitor)

    def list_files(self, reason: str | None = None) -> Sequence[PurePosixPath]:
        paths = self._list()
        self._dispatch(lambda v: v.on_list_files(paths, reason))
        return paths

    def read_file(
        self,
        path: PurePosixPath,
        reason: str | None = None,
    ) -> str | None:
        try:
            contents = self._read(path)
        except FileNotFoundError:
            contents = None
        self._dispatch(lambda v: v.on_read_file(path, contents, reason))
        return contents

    def write_file(
        self,
        path: PurePosixPath,
        contents: str,
        reason: str | None = None,
    ) -> None:
        self._dispatch(lambda v: v.on_write_file(path, contents, reason))
        return self._write(path, contents)

    def delete_file(
        self,
        path: PurePosixPath,
        reason: str | None = None,
    ) -> bool:
        self._dispatch(lambda v: v.on_delete_file(path, reason))
        return self._delete(path)

    def rename_file(
        self,
        src_path: PurePosixPath,
        dst_path: PurePosixPath,
        reason: str | None = None,
    ) -> None:
        self._dispatch(lambda v: v.on_rename_file(src_path, dst_path, reason))
        self._rename(src_path, dst_path)

    def _list(self) -> Sequence[PurePosixPath]:  # pragma: no cover
        raise NotImplementedError()

    def _read(self, path: PurePosixPath) -> str:  # pragma: no cover
        raise NotImplementedError()

    def _write(
        self, path: PurePosixPath, contents: str
    ) -> None:  # pragma: no cover
        raise NotImplementedError()

    def _delete(self, path: PurePosixPath) -> bool:  # pragma: no cover
        raise NotImplementedError()

    def _rename(
        self, src_path: PurePosixPath, dst_path: PurePosixPath
    ) -> None:
        # We can provide a default implementation here.
        contents = self._read(src_path)
        self._write(dst_path, contents)
        self._delete(src_path)


class ToolVisitor(Protocol):
    """Tool usage hook"""

    def on_list_files(
        self, paths: Sequence[PurePosixPath], reason: str | None
    ) -> None: ...  # pragma: no cover

    def on_read_file(
        self, path: PurePosixPath, contents: str | None, reason: str | None
    ) -> None: ...  # pragma: no cover

    def on_write_file(
        self, path: PurePosixPath, contents: str, reason: str | None
    ) -> None: ...  # pragma: no cover

    def on_delete_file(
        self, path: PurePosixPath, reason: str | None
    ) -> None: ...  # pragma: no cover

    def on_rename_file(
        self,
        src_path: PurePosixPath,
        dst_path: PurePosixPath,
        reason: str | None,
    ) -> None: ...  # pragma: no cover


class StagingToolbox(Toolbox):
    """Git-index backed toolbox implementation

    All files are directly read from and written to the index. This allows
    concurrent editing without interference with the working directory.
    """

    def __init__(
        self, repo: Repo, visitors: Sequence[ToolVisitor] | None = None
    ) -> None:
        super().__init__(visitors)
        self._repo = repo
        self._updated = set[str]()

    @override
    def _list(self) -> Sequence[PurePosixPath]:
        # Show staged files.
        return [
            PurePosixPath(p)
            for p in self._repo.git("ls-files").stdout.splitlines()
        ]

    @override
    def _read(self, path: PurePosixPath) -> str:
        # Read the file from the index.
        return self._repo.git("show", f":{path}").stdout

    @override
    def _write(self, path: PurePosixPath, contents: str) -> None:
        self._updated.add(str(path))
        # Update the index without touching the worktree.
        # https://stackoverflow.com/a/25352119
        with tempfile.NamedTemporaryFile(delete_on_close=False) as temp:
            temp.write(contents.encode("utf8"))
            temp.close()
            sha = self._repo.git(
                "hash-object", "-w", temp.name, "--path", str(path)
            ).stdout
            mode = 644  # TODO: Read from original file if it exists.
            self._repo.git(
                "update-index", "--add", "--cacheinfo", f"{mode},{sha},{path}"
            )

    @override
    def _delete(self, path: PurePosixPath) -> bool:
        try:
            self._repo.git("rm", "--cached", "--", str(path))
        except GitError as err:
            _logger.warning("Failed to delete file. [err=%r]", err)
            return False
        else:
            self._updated.add(str(path))
            return True

    def trim_index(self) -> None:
        """Unstage any files which have not been written to"""
        git = self._repo.git("diff", "--name-only", "--cached")
        untouched = [
            path
            for path in git.stdout.splitlines()
            if path and path not in self._updated
        ]
        if untouched:
            self._repo.git("reset", "--", *untouched)
            _logger.debug("Trimmed index. [reset_paths=%s]", untouched)
