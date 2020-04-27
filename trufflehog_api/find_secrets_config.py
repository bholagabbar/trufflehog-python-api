"""
TODO: Documentation
A configuration class and its builder.  These are passed into the methods in
find_secrets.
"""

from __future__ import annotations
from typing import List


class FindSecretsConfig():
  """
  A set of parameters that specify a search.
  """

  def __init__(self, *,
               branch: str,
               entropy_checks_enabled: bool,
               max_depth: int,
               path_exclusions: List[str],
               path_inclusions: List[str],
               regexes: List[str],
               since_commit: int):
    """TODO"""
    self._branch: str = branch
    self._entropy_checks_enabled: bool = entropy_checks_enabled
    self._max_depth: int = max_depth
    self._path_exclusions: List[str] = list(path_exclusions)
    self._path_inclusions: List[str] = list(path_inclusions)
    self._regexes: List[str] = list(regexes)
    self._since_commit: int = since_commit

  @property
  def branch(self) -> str:
    """TODO"""
    return self._branch

  @property
  def entropy_checks_enabled(self) -> bool:
    """TODO"""
    return self._entropy_checks_enabled

  @property
  def max_depth(self) -> int:
    """TODO"""
    return self._max_depth

  @property
  def path_exclusions(self) -> List[str]:
    """TODO"""
    return list(self._path_exclusions)

  @property
  def path_inclusions(self) -> List[str]:
    """TODO"""
    return list(self._path_inclusions)

  @property
  def regexes(self) -> List[str]:
    """TODO"""
    return list(self._regexes)

  @property
  def since_commit(self) -> int:
    """TODO"""
    return self._since_commit


class FindSecretsConfigBuilder():
  """
  A builder for creating a SearchConfig.
  """

  def __init__(self):
    self._branch: str = None
    self._entropy_checks_enabled: bool = True
    self._max_depth: int = 1_000_000
    self._path_exclusions: List[str] = []
    self._path_inclusions: List[str] = []
    self._regexes: List[str] = []
    self._since_commit: int = None

  @property
  def branch(self) -> str:
    """TODO"""
    return self._branch

  @property
  def entropy_checks_enabled(self) -> bool:
    """TODO"""
    return self._entropy_checks_enabled

  @property
  def max_depth(self) -> int:
    """TODO"""
    return self._max_depth

  @property
  def path_exclusions(self) -> List[str]:
    """TODO"""
    return list(self._path_exclusions)

  @property
  def path_inclusions(self) -> List[str]:
    """TODO"""
    return list(self._path_inclusions)

  @property
  def regexes(self) -> List[str]:
    """TODO"""
    return list(self._regexes)

  @property
  def since_commit(self) -> int:
    """TODO"""
    return self._since_commit

  def set_branch(self, branch: str) -> FindSecretsConfigBuilder:
    """TODO"""
    self._branch = branch
    return self

  def set_entropy_checks_enabled(self, enable: bool) -> FindSecretsConfigBuilder:
    """TODO"""
    self._entropy_checks_enabled = enable
    return self

  def set_max_depth(self, max_depth: int) -> FindSecretsConfigBuilder:
    """TODO"""
    self._max_depth = max_depth
    return self

  def set_path_exclusions(self, path_exclusions: List[str]) -> FindSecretsConfigBuilder:
    """TODO"""
    self._path_exclusions: List[str] = list(path_exclusions)
    return self

  def set_path_inclusions(self, path_inclusions: List[str]) -> FindSecretsConfigBuilder:
    """TODO"""
    self._path_inclusions = list(path_inclusions)
    return self

  def set_regexes(self, regexes: List[str]) -> FindSecretsConfigBuilder:
    """TODO"""
    self._regexes = list(regexes)
    return self

  def set_since_commit(self, commit: int) -> FindSecretsConfigBuilder:
    """TODO"""
    self._since_commit = commit
    return self

  def build(self) -> FindSecretsConfig:
    """
    Returns a FindSecretsConfig whose settings correspond to the builder's.
    """
    result = FindSecretsConfig(
        branch=self._branch,
        entropy_checks_enabled=self._entropy_checks_enabled,
        max_depth=self._max_depth,
        path_exclusions=self._path_exclusions,
        path_inclusions=self._path_inclusions,
        regexes=self._regexes,
        since_commit=self._since_commit
    )
    return result
