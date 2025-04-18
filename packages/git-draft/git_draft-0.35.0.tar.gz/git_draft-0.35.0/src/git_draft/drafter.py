"""Git state management logic"""

from __future__ import annotations

from collections.abc import Callable, Sequence
import dataclasses
from datetime import datetime, timedelta
import enum
import json
import logging
from pathlib import Path, PurePosixPath
import re
from re import Match
import textwrap
import time

from .bots import Action, Bot, Goal
from .common import JSONObject, Table, qualified_class_name, random_id
from .git import Commit, Repo
from .prompt import PromptRenderer, TemplatedPrompt
from .store import Store, sql
from .toolbox import StagingToolbox, ToolVisitor


_logger = logging.getLogger(__name__)


class Accept(enum.Enum):
    """Valid change accept mode"""

    MANUAL = 0
    CHECKOUT = enum.auto()
    FINALIZE = enum.auto()
    NO_REGRETS = enum.auto()


@dataclasses.dataclass(frozen=True)
class Draft:
    """Collection of generated changes"""

    branch_name: str


@dataclasses.dataclass(frozen=True)
class _Branch:
    """Draft branch"""

    _pattern = re.compile(r"drafts/(.+)")

    folio_id: str

    @property
    def name(self) -> str:
        return f"drafts/{self.folio_id}"

    def __str__(self) -> str:
        return self.name

    @classmethod
    def active(cls, repo: Repo, name: str | None = None) -> _Branch | None:
        match: Match | None = None
        active_branch = name or repo.active_branch()
        if active_branch:
            match = cls._pattern.fullmatch(active_branch)
        if not match:
            if name:
                raise ValueError(f"Not a valid draft branch name: {name!r}")
            return None
        return _Branch(match[1])

    @staticmethod
    def new_suffix() -> str:
        return random_id(9)


class Drafter:
    """Draft state orchestrator"""

    def __init__(self, store: Store, repo: Repo) -> None:
        with store.cursor() as cursor:
            cursor.executescript(sql("create-tables"))
        self._store = store
        self._repo = repo

    @classmethod
    def create(cls, store: Store, path: str | None = None) -> Drafter:
        return cls(store, Repo.enclosing(Path(path) if path else Path.cwd()))

    def generate_draft(  # noqa: PLR0913
        self,
        prompt: str | TemplatedPrompt,
        bot: Bot,
        accept: Accept = Accept.MANUAL,
        bot_name: str | None = None,
        prompt_transform: Callable[[str], str] | None = None,
        reset: bool = False,
        timeout: float | None = None,
        tool_visitors: Sequence[ToolVisitor] | None = None,
    ) -> Draft:
        if timeout is not None:
            raise NotImplementedError()  # TODO: Implement

        if self._repo.has_staged_changes():
            if not reset:
                raise ValueError("Please commit or reset any staged changes")
            self._repo.git("reset")

        # Ensure that we are on a draft branch.
        branch = _Branch.active(self._repo)
        if branch:
            self._stage_repo()
            _logger.debug("Reusing active branch %s.", branch)
        else:
            branch = self._create_branch()
            _logger.debug("Created branch %s.", branch)

        # Handle prompt templating and editing.
        prompt_contents = self._prepare_prompt(prompt, prompt_transform)
        with self._store.cursor() as cursor:
            [(prompt_id,)] = cursor.execute(
                sql("add-prompt"),
                {
                    "branch_suffix": branch.folio_id,
                    "template": prompt.template
                    if isinstance(prompt, TemplatedPrompt)
                    else None,
                    "contents": prompt_contents,
                },
            )

        operation_recorder = _OperationRecorder()
        change = self._generate_change(
            bot,
            Goal(prompt_contents, timeout),
            [operation_recorder, *list(tool_visitors or [])],
        )
        with self._store.cursor() as cursor:
            cursor.execute(
                sql("add-action"),
                {
                    "commit_sha": change.commit,
                    "prompt_id": prompt_id,
                    "bot_name": bot_name,
                    "bot_class": qualified_class_name(bot.__class__),
                    "walltime_seconds": change.walltime.total_seconds(),
                    "request_count": change.action.request_count,
                    "token_count": change.action.token_count,
                },
            )
            cursor.executemany(
                sql("add-operation"),
                [
                    {
                        "commit_sha": change.commit,
                        "tool": o.tool,
                        "reason": o.reason,
                        "details": json.dumps(o.details),
                        "started_at": o.start,
                    }
                    for o in operation_recorder.operations
                ],
            )
        _logger.info("Created new change on %s.", branch)

        delta = change.delta()
        if delta and accept.value >= Accept.CHECKOUT.value:
            delta.apply()
        if accept.value >= Accept.FINALIZE.value:
            self.finalize_draft(delete=accept == Accept.NO_REGRETS)
        return Draft(str(branch))

    def _prepare_prompt(
        self,
        prompt: str | TemplatedPrompt,
        prompt_transform: Callable[[str], str] | None,
    ) -> str:
        if isinstance(prompt, TemplatedPrompt):
            renderer = PromptRenderer.for_toolbox(StagingToolbox(self._repo))
            contents = renderer.render(prompt)
        else:
            contents = prompt
        if prompt_transform:
            contents = prompt_transform(contents)
        if not contents.strip():
            raise ValueError("Empty prompt")
        return contents

    def _generate_change(
        self,
        bot: Bot,
        goal: Goal,
        tool_visitors: Sequence[ToolVisitor],
    ) -> _Change:
        # Trigger code generation.
        _logger.debug("Running bot... [bot=%s]", bot)
        toolbox = StagingToolbox(self._repo, tool_visitors)
        start_time = time.perf_counter()
        action = bot.act(goal, toolbox)
        end_time = time.perf_counter()
        walltime = end_time - start_time
        _logger.info("Completed bot action. [action=%s]", action)

        # Generate an appropriate commit.
        toolbox.trim_index()
        title = action.title
        if not title:
            title = _default_title(goal.prompt)
        commit = self._repo.create_commit(
            f"draft! {title}\n\n{goal.prompt}",
            skip_hooks=True,
        )

        return _Change(
            commit.sha, timedelta(seconds=walltime), action, self._repo
        )

    def finalize_draft(self, *, delete: bool = False) -> Draft:
        branch = _Branch.active(self._repo)
        if not branch:
            raise RuntimeError("Not currently on a draft branch")
        self._stage_repo()

        with self._store.cursor() as cursor:
            rows = cursor.execute(
                sql("get-branch-by-suffix"), {"suffix": branch.folio_id}
            )
            if not rows:
                raise RuntimeError("Unrecognized draft branch")
            [(origin_branch, origin_sha)] = rows

        # We do a small dance to move back to the original branch, keeping the
        # draft branch untouched. See https://stackoverflow.com/a/15993574 for
        # the inspiration.
        self._repo.git("checkout", "--detach")
        self._repo.git("reset", "-N", origin_branch)
        self._repo.git("checkout", origin_branch)

        if delete:
            self._repo.git("branch", "-D", branch.name)
            _logger.debug("Deleted branch %s.", branch)

        _logger.info("Exited %s.", branch)
        return Draft(branch.name)

    def _create_branch(self) -> _Branch:
        if self._repo.active_branch() is None:
            raise RuntimeError("No currently active branch")
        origin_branch = self._repo.active_branch()
        origin_sha = self._repo.head_commit().sha

        self._repo.git("checkout", "--detach")
        self._stage_repo()
        suffix = _Branch.new_suffix()

        with self._store.cursor() as cursor:
            cursor.execute(
                sql("add-branch"),
                {
                    "suffix": suffix,
                    "repo_path": str(self._repo.working_dir),
                    "origin_branch": origin_branch,
                    "origin_sha": origin_sha,
                },
            )

        branch = _Branch(suffix)
        self._repo.checkout_new_branch(branch.name)
        return branch

    def _stage_repo(self) -> Commit | None:
        self._repo.git("add", "--all")
        if not self._repo.has_staged_changes():
            return None
        return self._repo.create_commit("draft! sync")

    def history_table(self, branch_name: str | None = None) -> Table:
        path = self._repo.working_dir
        branch = _Branch.active(self._repo, branch_name)
        with self._store.cursor() as cursor:
            if branch:
                results = cursor.execute(
                    sql("list-prompts"),
                    {
                        "repo_path": str(path),
                        "branch_suffix": branch.folio_id,
                    },
                )
            else:
                results = cursor.execute(
                    sql("list-drafts"), {"repo_path": str(path)}
                )
            return Table.from_cursor(results)

    def latest_draft_prompt(self) -> str | None:
        """Returns the latest prompt for the current draft"""
        branch = _Branch.active(self._repo)
        if not branch:
            return None
        with self._store.cursor() as cursor:
            result = cursor.execute(
                sql("get-latest-prompt"),
                {
                    "repo_path": str(self._repo.working_dir),
                    "branch_suffix": branch.folio_id,
                },
            ).fetchone()
            return result[0] if result else None


type _CommitSHA = str


@dataclasses.dataclass(frozen=True)
class _Change:
    """A bot-generated draft, may be a no-op"""

    commit: _CommitSHA
    walltime: timedelta
    action: Action
    repo: Repo = dataclasses.field(repr=False)

    def delta(self) -> _Delta | None:
        diff = self.repo.git("diff-tree", "--patch", self.commit).stdout
        return _Delta(diff, self.repo) if diff else None


@dataclasses.dataclass(frozen=True)
class _Delta:
    """A change's effects, guaranteed non-empty"""

    diff: str
    repo: Repo = dataclasses.field(repr=False)

    def apply(self) -> None:
        # For patch applcation to work as expected (adding conflict markers as
        # needed), files in the patch must exist in the index.
        self.repo.git("add", "--all")
        git = self.repo.git(
            "apply", "--3way", "-", stdin=self.diff, expect_codes=()
        )
        if "with conflicts" in git.stderr:
            raise ConflictError()
        if git.code != 0:
            raise NotImplementedError()  # TODO: Raise better error
        self.repo.git("reset")


class ConflictError(Exception):
    """A change could not be applied cleanly"""


class _OperationRecorder(ToolVisitor):
    def __init__(self) -> None:
        self.operations = list[_Operation]()

    def on_list_files(
        self, paths: Sequence[PurePosixPath], reason: str | None
    ) -> None:
        self._record(reason, "list_files", count=len(paths))

    def on_read_file(
        self, path: PurePosixPath, contents: str | None, reason: str | None
    ) -> None:
        self._record(
            reason,
            "read_file",
            path=str(path),
            size=-1 if contents is None else len(contents),
        )

    def on_write_file(
        self, path: PurePosixPath, contents: str, reason: str | None
    ) -> None:
        self._record(reason, "write_file", path=str(path), size=len(contents))

    def on_delete_file(self, path: PurePosixPath, reason: str | None) -> None:
        self._record(reason, "delete_file", path=str(path))

    def on_rename_file(
        self,
        src_path: PurePosixPath,
        dst_path: PurePosixPath,
        reason: str | None,
    ) -> None:
        self._record(
            reason,
            "rename_file",
            src_path=str(src_path),
            dst_path=str(dst_path),
        )

    def _record(self, reason: str | None, tool: str, **kwargs) -> None:
        op = _Operation(
            tool=tool, details=kwargs, reason=reason, start=datetime.now()
        )
        _logger.debug("Recorded operation. [op=%s]", op)
        self.operations.append(op)


@dataclasses.dataclass(frozen=True)
class _Operation:
    tool: str
    details: JSONObject
    reason: str | None
    start: datetime


def _default_title(prompt: str) -> str:
    return textwrap.shorten(prompt, break_on_hyphens=False, width=72)
