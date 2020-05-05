"""
TODO: Documentation
"""

import datetime
import json
import os
import shutil
from typing import List
import git

from truffleHog import truffleHog

from trufflehog_api.repo_config import RepoConfig
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

def _clean_up(output: dict):
    issues_path = output.get("issues_path", None)
    if issues_path and os.path.isdir(issues_path):
        shutil.rmtree(output["issues_path"])

def find_secrets(path: str, repo_config: RepoConfig = None,
                 search_config: SearchConfig = None) -> List[Secret]:
    """Searches for secrets in the repository repo using the search configuration config
       Returns a list of Secret objects, one for each secret found."""
    if git.repo.fun.is_git_dir(path + os.path.sep + ".git"):
        # Is local repository
        # If envvironment variable token is present give warning.
        git_url = None
        repo_path = path
    else:
        # Is remote repository
        # Append token if present in environment variable
        git_url = path
        repo_path = None

    if not repo_config:
        repo_config = RepoConfig()

    if not search_config:
        search_config = SearchConfig()

    do_regex = search_config.regexes

    output = truffleHog.find_strings(git_url=git_url,
                                     since_commit=repo_config.since_commit,
                                     max_depth=search_config.max_depth,
                                     do_regex=do_regex,
                                     do_entropy=search_config.entropy_checks_enabled,
                                     custom_regexes=search_config.regexes,
                                     branch=repo_config.branch,
                                     repo_path=repo_path,
                                     path_inclusions=search_config.include_search_paths,
                                     path_exclusions=search_config.exclude_search_paths)
    secrets = _find_strings_to_secrets(output)
    _clean_up(output)
    return secrets
    