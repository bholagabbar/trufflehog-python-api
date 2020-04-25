"""
TODO: Documentation
SearchConfig class.
"""

from typing import List


class SearchConfig():
  """
  A set of parameters that specify a search.
  """

  def __init__(self):
    self._enable_entropy_checks: bool = False


class SearchConfigBuilder():
  """
  A builder for creating a SearchConfig.
  """

  def __init__(self):
    self._since_commit: int
    self._max_depth: int
    self._enable_entropy_checks: bool
    self._branch: str
    self._path_inclusions: List[str]

  def since_commmit(self, commit: int) -> "SearchConfigBuilder":
    """
    TODO: Documentation
    """
    self._since_commit = commit
    return self

  def max_depth(self, max_depth: int) -> "SearchConfigBuilder":
    """
    TODO: Documentation
    """
    self._max_depth = max_depth
    return self

  def enable_entropy_checks(self, enable_entropy: bool) -> "SearchConfigBuilder":
    """
    TODO: Documentation
    """
    self._enable_entropy_checks = enable_entropy
    return self

  def branch(self, branch: str):
    """
    TODO: Documentation
    """
    self._branch = branch
    return self

  def path_inclusions(self, path_inclusions: List[str]) -> "SearchConfigBuilder":
    """
    TODO: Documentation
    """
    self._path_inclusions = list(path_inclusions)
    return self

  def path_exclusions(self, path_exclusions: List[str]) -> "SearchConfigBuilder":
    """
    TODO: Documentation
    """
    self._path_inclusions: List[str] = list(path_exclusions)
    return self

  def build(self) -> SearchConfig:
    """
    Returns a SearchConfig whose settings correspond to the builder's.
    """
    result = SearchConfig()
    # TODO: Build result
    return result
