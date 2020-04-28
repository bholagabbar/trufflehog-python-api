"""
TODO: Documentation
"""

import datetime
import os
import shutil
import stat
import tempfile
from typing import List

from git import Repo

from trufflehog_api.find_secrets_config import FindSecretsConfig


class Secret():
  """
  TODO: Documentation
  A secret found in a repository.
  """

  def __init__(self,
               commit_time: datetime.datetime,
               branch_name: str,
               prev_commit: str,
               printable_diff: str,
               commit_hash: str,
               reason: str,
               path: str):
    """TODO"""
    self._commit_time: datetime.datetime = commit_time
    self._branch_name: str = branch_name
    self._prev_commit: str = prev_commit
    self._printable_diff: str = printable_diff
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

  @property
  def prev_commit(self) -> str:
    """TODO"""
    return self._prev_commit

  @property
  def printable_diff(self) -> str:
    """TODO"""
    return self._printable_diff

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


def find_secrets(repo: Repo, settings: FindSecretsConfig) -> List[Secret]:
  """TODO"""
  raise NotImplementedError()


def find_secrets_remote(url: str, settings: FindSecretsConfig) -> List[Secret]:
  """
  Identical to find_secrets, but creates a Repo based on the provided URL.

  The repo is cloned into a temporary directory, which gets deleted when the
  function finishes.
  """
  project_path: str = tempfile.mkdtemp()

  try:
    repo: Repo = Repo.clone_from(url, project_path)
    result: List[Secret] = find_secrets(repo, settings)
  finally:
    def del_rw(_action, name, _exc):
      os.chmod(name, stat.S_IWRITE)
      os.remove(name)
    shutil.rmtree(project_path, onerror=del_rw)

  return result


def find_secrets_local(path: str, settings: FindSecretsConfig) -> List[Secret]:
  """
  Identical to find_secrets, but creates a Repo based on the provided path to
  a local repository.
  """
  repo: Repo = Repo(path)
  return find_secrets(repo, settings)
