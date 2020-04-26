"""
TODO: Documentation
SearchConfig class.
"""

from __future__ import annotations
from typing import List


class FindSecretsConfig():
  """
  A set of parameters that specify a search.
  """

  def __init__(self):
    self._enable_entropy_checks: bool = False


class FindSecretsConfigBuilder():
  """
  A builder for creating a SearchConfig.
  """

  def __init__(self):
    self._since_commit: int
    self._max_depth: int
    self._enable_entropy_checks: bool
    self._branch: str
    self._path_inclusions: List[str]

  def since_commit(self, commit: int) -> FindSecretsConfigBuilder:
    """
    TODO: Documentation
    """
    self._since_commit = commit
    return self

  def max_depth(self, max_depth: int) -> FindSecretsConfigBuilder:
    """
    TODO: Documentation
    """
    self._max_depth = max_depth
    return self

  def enable_entropy_checks(self, enable_entropy: bool) -> FindSecretsConfigBuilder:
    """
    TODO: Documentation
    """
    self._enable_entropy_checks = enable_entropy
    return self

  def branch(self, branch: str) -> FindSecretsConfigBuilder:
    """
    TODO: Documentation
    """
    self._branch = branch
    return self

  def path_inclusions(self, path_inclusions: List[str]) -> FindSecretsConfigBuilder:
    """
    TODO: Documentation
    """
    self._path_inclusions = list(path_inclusions)
    return self

  def path_exclusions(self, path_exclusions: List[str]) -> FindSecretsConfigBuilder:
    """
    TODO: Documentation
    """
    self._path_inclusions: List[str] = list(path_exclusions)
    return self

  def build(self) -> FindSecretsConfig:
    """
    Returns a SearchConfig whose settings correspond to the builder's.
    """
    result = FindSecretsConfig()
    # TODO: Build result
    return result
