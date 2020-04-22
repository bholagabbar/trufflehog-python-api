"""
TODO: Documentation
SearchConfig class.
"""

class SearchConfig():
  """
  A set of parameters that specify a search.
  """

  def __init__(self):
    self._use_regex: bool = False
    self._enable_entropy_checks: bool = False


class SearchConfigBuilder():
  """
  A builder for creating a SearchConfig.
  """

  def __init__(self):
    pass

  def build(self) -> SearchConfig:
    """
    Returns a SearchConfig whose settings correspond to the builder's.
    """
    result = SearchConfig()
    # TODO: Build result
    return result
