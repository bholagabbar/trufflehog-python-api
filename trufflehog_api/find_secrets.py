"""
Allows users to search for secrets within a git repository as specified
by RepoConfig and SearchConfig. Presents the output as a list of Secret
objects that can be easily parsed or outputted.
"""

import concurrent.futures
import datetime
import json
import os
import shutil
import stat
import tempfile
import warnings
from typing import List

from git import Repo
from git.repo.fun import is_git_dir
from truffleHog import truffleHog

from trufflehog_api.error import TrufflehogApiError
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
        :return: time when the secret was committed
        """
        return self._commit_time

    @property
    def branch_name(self) -> str:
        """
        :return: branch where the secret was committed
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

    def __str__(self):
        """
        :return: Returns a string containing all the attributes of a Secret
        besides the diff.
        """
        return ("commit_time: {commit_time}\n"
                "branch_name: {branch_name}\n"
                "commit: {commit}\n"
                "commit_hash: {commit_hash}\n"
                "reason: {reason}\n"
                "path: {path}\n".format(commit_time=self._commit_time,
                                        branch_name=self._branch_name,
                                        commit=self._commit.strip('\n'),
                                        commit_hash=self._commit_hash,
                                        reason=self._reason,
                                        path=self._path))

    def __repr__(self):
        """
        :return: Returns a string containing all the attributes of a Secret
        """
        return ("Secret(commit_time={commit_time}, "
                "branch_name={branch_name}, "
                "commit={commit}, "
                "commit_hash={commit_hash}, "
                "diff={diff}, "
                "reason={reason},"
                "path={path})".format(commit_time=self._commit_time,
                                      branch_name=self._branch_name,
                                      commit=self._commit,
                                      commit_hash=self._commit_hash,
                                      diff=self._diff,
                                      reason=self._reason,
                                      path=self._path))


class FindSecretsRequest:
    """
    Represents a request to search for secrets in a specific repository
    with RepoConfig and SearchConfig
    """

    def __init__(self,
                 path: str,
                 repo_config: RepoConfig = None,
                 search_config: SearchConfig = None):
        """Creates a new FindSecretsRequest object

        :param str path:
        Path to the git repository

        :param repo_config:
        Configuration object to specify repository specific attributes for the search
        Default is None which gives the default RepoConfig object

        :param search_config:
        Configuration object to specify other attributes for the search that can be
        generalized to many searches
        Default is None which gives the default SearchConfig object
        """
        self._path = path
        self._repo_config = repo_config
        self._search_config = search_config

    @property
    def path(self) -> str:
        """
        :return: request's path to git repository
        """
        return self._path

    @property
    def repo_config(self) -> RepoConfig:
        """
        :return: request's repository specific attributes for the search
        """
        return self._repo_config

    @property
    def search_config(self) -> SearchConfig:
        """
        :return: request's other attributes for the search
        """
        return self._search_config

    def __str__(self):
        """
        :return: Returns a json string containing all the attributes of the FindSecretsRequest
        """
        n_config = dict()
        s_config = self._search_config
        n_config["max_depth"] = s_config.max_depth
        n_config["entropy_checks_enabled"] = s_config.entropy_checks_enabled
        n_config["include_search_paths"] = s_config.include_search_paths
        n_config["exclude_search_paths"] = s_config.exclude_search_paths

        request = dict()
        request["path"] = self._path
        request["repo_config"] = self._repo_config.to_dict()
        request["search_config"] = n_config
        request_string = json.dumps(request, indent=2)
        return request_string

    def __repr__(self):
        """
        :return: Returns a string containing all the attributes of the FindSecretsRequest
        """
        repr_repo = repr(self._repo_config)
        repr_search = repr(self._search_config)
        return ("FindSecretsRequest(path={path}, "
                "repo_config={repo_config}, "
                "search_config={search_config})").format(path=self._path,
                                                         repo_config=repr_repo,
                                                         search_config=repr_search)


def execute_find_secrets_request(request: FindSecretsRequest) -> List[Secret]:
    """
    Executes the search for secrets with the given request

    :param FindSecretsRequest request:
        request object containing the path to the git repository and
        other configurations for the search

    :return: list of secret objects that represent the secrets found by the search
    """
    path = request.path
    repo_config = request.repo_config
    search_config = request.search_config

    if not repo_config:
        repo_config = RepoConfig()

    if not search_config:
        search_config = SearchConfig()

    token_key = repo_config.access_token_env_key
    token_exists = token_key and token_key in os.environ

    repo = None
    repo_path = path

    if is_git_dir(path + os.path.sep + ".git"):
        # If repo is local and env key for access token is present, display warning
        if token_exists:
            warnings.warn("Warning: local repository path provided with an access token - "
                          "Token will be ignored")
    else:
        # If repo is remote, append access token to path from its env key
        git_url = path
        if token_exists:
            git_url = _append_env_access_token_to_path(path, token_key)

        # We pre-clone the repo to fix a bug that causes truffleHog to crash
        # on Windows machines when run on remote repositories.
        try:
            repo_path = tempfile.mkdtemp()
            repo = Repo.clone_from(git_url, repo_path)
        except Exception as e:
            _delete_tempdir(repo_path)
            raise TrufflehogApiError(e)

    do_regex = search_config.regexes

    secrets = None
    try:
        output = truffleHog.find_strings(git_url=None,
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
    except Exception as e:
        raise TrufflehogApiError(e)

    # Delete our clone of the remote repo (if it exists)
    if repo is not None:
        repo.close()  # truffleHog doesn't do this, which causes a bug on Windows
        _delete_tempdir(repo_path)

    return secrets


def _delete_tempdir(path: str):
    """Deletes a Repo that was cloned to path.  For use in execute_find_secrets_request.
    """
    def del_rw(func, path, _exc):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    shutil.rmtree(path, onerror=del_rw)


def _convert_default_output_to_secrets(output: dict) -> List[Secret]:
    """
    Takes the output from truffleHog.find_strings() and converts
    to a list of Secret objects that are easier to programmatically
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
    """Removes files containing the output from truffleHog.find_strings()
    from the file system.

    :param dict output:
        Output from truffleHog.find_strings()
    """
    issues_path = output.get("issues_path", None)
    if issues_path and os.path.isdir(issues_path):
        shutil.rmtree(output["issues_path"])


def _append_env_access_token_to_path(path, token_key):
    """Appends the secret token to a valid git url

    :param str path:
        Repository path
    :param str token_key:
        Env variable key which stores the secret token
    """
    # FIXME - This only supports github!
    idx = path.find("github.com/")
    if idx > -1:
        path = path[:idx] + os.environ.get(token_key) + ":x-oauth-basic@" + path[idx:]
    return path


def find_secrets(path: str,
                 repo_config: RepoConfig = None,
                 search_config: SearchConfig = None) -> List[Secret]:
    """
    Searches for secrets in the repository repo using the search configuration config
    Does so by creating and executing a request to search.

    :param str path:
        Path to the git repository

    :param repo_config:
        Configuration object to specify repository specific attributes for the search
        Default is None which will give the default RepoConfig object

    :param search_config:
        Configuration object to specify other attributes for the search that can be
        generalized to many searches
        Default is None which will give the default SearchConfig object

    :raises TrufflehogApiError:
        wraps an exception that occurred on calling truffleHog.find_strings()

    :return: list of secret objects that represent the secrets found by the search

    :rtype: List[Secret]
    """

    return execute_find_secrets_request(
        FindSecretsRequest(path, repo_config=repo_config, search_config=search_config))


def batch_execute_find_secrets_request(requests: List[FindSecretsRequest],
                                       concurrency_level=4):
    """
    Executes a search for secrets for the list of requests concurrently

     :param list requests:
         List of FindSecretRequest objects

     :param int concurrency_level:
         Maximum number of threads to spawn while creating a ThreadPoolExecutor
         instance which manages the execution of the jobs.

     :raises TrufflehogApiError:
         wraps an exception that occurred on calling truffleHog.find_strings(),
         creating a ThreadPoolExecutor instance or submitting jobs

     :return: list of futures jobs that were submitted to the ThreadPoolExecutor for processing
     """
    res = []
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency_level) as executor:
            for request in requests:
                future_result = executor.submit(execute_find_secrets_request, request)
                res.append(future_result)
        return res
    except Exception as e:
        raise TrufflehogApiError(e)
