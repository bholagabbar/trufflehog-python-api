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
                 commit: str,
                 diff: str,
                 commit_hash: str,
                 reason: str,
                 path: str):
        """TODO"""
        self._commit_time: datetime.datetime = commit_time
        self._branch_name: str = branch_name
        self._commit: str = commit
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
    def commit(self) -> str:
        """TODO"""
        return self._commit

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
        """
        :return: Returns a string containing all the attributes of a Secret
        """
        return json.dumps(self.to_dict(), indent=2)

    def __repr__(self):
        """
        :return: Returns a string containing all the attributes of a Secret
        """
        return "Secret(commit_time={commit_time}, "\
            "branch_name={branch_name}, commit={commit}, "\
            "commit_hash={commit_hash}, diff={diff}, reason={reason}, " \
            "path={path})".format(
            commit_time=self._commit_time, branch_name=self._branch_name, commit=self._commit, commit_hash=self._commit_hash, diff=self._diff, reason=self._reason, path=self._path
        )

    def to_dict(self):
        """
        :return: Returns a dict containing all the attributes of a Secret
        """
        secret_dict = dict()
        secret_dict["commit_time"] = self._commit_time
        secret_dict["branch_name"] = self._branch_name
        secret_dict["commit"] = self._commit
        secret_dict["diff"] = self._diff
        secret_dict["commit_hash"] = self._commit_hash
        secret_dict["reason"] = self._reason
        secret_dict["path"] = self._path
        return secret_dict


def _convert_default_output_to_secrets(output: dict) -> List[Secret]:
    secrets = []
    issues = output["foundIssues"]
    for issue_file in issues:
        with open(issue_file) as result_file:
            issue = json.loads(result_file.read())
            secret = Secret(commit_time=issue['date'],
                            branch_name=issue['branch'],
                            commit=issue['commit'],
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
        # If environment variable token is present give warning.
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
    secrets = _convert_default_output_to_secrets(output)
    _clean_up(output)
    return secrets
    