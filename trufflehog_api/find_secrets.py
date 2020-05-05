"""
TODO: Documentation
"""

import datetime
from typing import List

from trufflehog_api.repository import Repository
from trufflehog_api.search_config import SearchConfig


class Secret:
    """
    TODO: Documentation
    A secret found in a repository.
    """

    def __init__(self, *,
                 commit_time: datetime.datetime,
                 branch_name: str,
                 prev_commit: str,
                 diff: str,
                 commit_hash: str,
                 reason: str,
                 path: str):
        """TODO"""
        self._commit_time: datetime.datetime = commit_time
        self._branch_name: str = branch_name
        self._prev_commit: str = prev_commit
        self._diff: str = diff
        self._commit_hash: str = commit_hash
        self._reason: str = reason
        self._path: str = path

    @property
    def commit_time(self) -> datetime.datetime:
        """TODO"""
        return self._commit_time

    @property
    def branch_name(self) -> str:
        """TODO"""
        return self._branch_name

    # TODO: Figure out how this is handled with no previous (Might be only commit).
    @property
    def prev_commit(self) -> str:
        """TODO"""
        return self._prev_commit

    @property
    def diff(self) -> str:
        """TODO"""
        return self._diff

    @property
    def commit_hash(self) -> str:
        """TODO"""
        return self._commit_hash

    @property
    def reason(self) -> str:
        """TODO"""
        return self._reason

    @property
    def path(self) -> str:
        """TODO"""
        return self._path

    def __str__(self):
        """TODO"""
        raise NotImplementedError()

    def __repr__(self):
        """TODO"""
        raise NotImplementedError()

    def to_dict(self):
        """TODO"""
        raise NotImplementedError()


def _find_strings_to_secrets(output: dict) -> List[Secret]:
    secrets = []
    issues = output["foundIssues"]
    for issue in issues:
        secret = Secret(commit_time=issue['date'],
                        branch_name=issue['branch'],
                        prev_commit=issue['commit'],
                        diff=issue['printDiff'],
                        commit_hash=issue['commitHash'],
                        reason=issue['reason'],
                        path=issue['path'])
        secrets.append(secret)
    return secrets


def find_secrets(repo: Repository, config: SearchConfig) -> List[Secret]:
    """TODO"""
    raise NotImplementedError()
