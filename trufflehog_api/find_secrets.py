"""
TODO: Documentation
"""

import datetime
import json
from typing import List

from truffleHog import truffleHog

from trufflehog_api.repository import Repository, RepositoryPathType
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
    for issue_file in issues:
        with open(issue_file) as result_file:
            issue = json.loads(result_file.read())
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
    """Searches for secrets in the repository repo using the search configuration config
       Returns a list of Secret objects, one for each secret found."""
    if repo.path_type == RepositoryPathType.LOCAL:
        git_url = None
        repo_path = repo.path
    else:
        git_url = repo.path
        repo_path = None

    do_regex = config.regexes

    output = truffleHog.find_strings(git_url=git_url,
                                     since_commit=repo.since_commit,
                                     max_depth=config.max_depth,
                                     do_regex=do_regex,
                                     do_entropy=config.entropy_checks_enabled,
                                     custom_regexes=config.regexes,
                                     branch=repo.branch,
                                     repo_path=repo_path,
                                     path_inclusions=config.include_search_paths,
                                     path_exclusions=config.exclude_search_paths)
    return _find_strings_to_secrets(output)
    