"""
Allows users to search for secrets within a git repository as specified
by RepoConfig and SearchConfig. Presents the output as a list of Secret
objects that can be easily parsed or outputted.
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
    A secret found in a repository. Contains information about where the secret
    is found and why it was flagged.
    """

    def __init__(self, *,
                 commit_time: datetime.datetime,
                 branch_name: str,
                 commit: str,
                 diff: str,
                 commit_hash: str,
                 reason: str,
                 path: str):
        """Creates a new Secret

        :param str commit_time:
            Time when the secret was committed

        :param str branch_name:
            Branch where the secret was committed

        :param str commit:
            Commit where the secret was found

        :param str diff:
            Git diff where secret can be found

        :param str commit_hash:
            Commit hash for the commit where the secret was found

        :param str reason:
            Reason why the secret was flagged (Eg. regex description or High Entropy)

        :param str path:
            Path to file in which secret can be found
        """
        self._commit_time: datetime.datetime = commit_time
        self._branch_name: str = branch_name
        self._commit: str = commit
        self._diff: str = diff
        self._commit_hash: str = commit_hash
        self._reason: str = reason
        self._path: str = path

    @property
    def commit_time(self) -> datetime.datetime:
        """
        :return time when the secret was committed
        """
        return self._commit_time

    @property
    def branch_name(self) -> str:
        """
        :return branch where the secret was committed
        """
        return self._branch_name

    @property
    def commit(self) -> str:
        """
        :return: commit where the secret was found
        """
        return self._commit

    @property
    def diff(self) -> str:
        """
        :return: git diff where secret can be found
        """
        return self._diff

    @property
    def commit_hash(self) -> str:
        """
        :return: commit hash for the commit where the secret was found
        """
        return self._commit_hash

    @property
    def reason(self) -> str:
        """
        :return: reason why the secret was flagged
        (Eg. regex description or High Entropy)
        """
        return self._reason

    @property
    def path(self) -> str:
        """
        :return: path to file in which secret can be found
        """
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


def _convert_default_output_to_secrets(output: dict) -> List[Secret]:
    """
    Takes the output from truffleHog.find_strings() and converts
    to a list of Secret objects that are easier to programatically
    parse and output.

    :param dict output:
        Output from truffleHog.find_strings()

    :return: List of Secret Objects
    """
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
    """
    Removes files containing the output from truffleHog.find_strings()
    from the file system.

    :param dict output:
        Output from truffleHog.find_strings()
    """
    issues_path = output.get("issues_path", None)
    if issues_path and os.path.isdir(issues_path):
        shutil.rmtree(output["issues_path"])

def find_secrets(path: str, repo_config: RepoConfig = None,
                 search_config: SearchConfig = None) -> List[Secret]:
    """
    Searches for secrets in the repository repo using the search configuration config
       Returns a list of Secret objects, one for each secret found.

    :param str path:
        Path to the git repository

    :param repo_config:
        Configuration object to specify repository specific attributes for the search

    :param search_config:
        Configuration object to specify other attributes for the search that can be
        generalized to many searches

    :return: list of secret objects that represent the secrets found by the search
    """
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
    