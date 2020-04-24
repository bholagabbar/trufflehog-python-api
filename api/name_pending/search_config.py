"""
TODO: Documentation
SearchConfig class.
"""

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
    pass
  
  def since_commmit(self, commit: int):
    self._since_commit : int = commit
    return self

  def max_depth(self, max_depth: int ):
    self._max_depth : int = max_depth
    return self

  def enable_entropy_checks(self, enable_entropy: bool):
    self._enable_entropy_checks: bool = enable_entropy
    return self

  def branch(self, branch: str):
    self._branch: str = branch
    return self

  def path_inclusions(self, path_inclusions: str[]):
    self._path_inclusions: str[] = path_inclusions
    return self

  def path_exclusions(self, path_exclusions: str[]):
    self._path_inclusions: str[] = path_exclusions
    return self

  def build(self) -> SearchConfig:
    """
    Returns a SearchConfig whose settings correspond to the builder's.
    """
    result = SearchConfig()
    # TODO: Build result
    return result
