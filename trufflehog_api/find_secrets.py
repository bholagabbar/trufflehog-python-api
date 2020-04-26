"""
TODO: Documentation
"""

from typing import List
from .find_secrets_config import FindSecretsConfig


class Secret():
  """
  TODO: Documentation
  A secret found in a repository.
  """

  def __init__(self):
    """TODO"""
    raise NotImplementedError()


def find_secrets(settings: FindSecretsConfig) -> List[Secret]:
  """TODO"""
  # How to specify which repo to search?
  #   - Multiple methods that take git_url, repo_path, etc.
  #     - Seems a little messy
  #   - One method that takes in some GitRepo object in addition to the settings
  #     - Might be overkill / annoying for client to use
  #     - Are there existing GitRepo objects that we should leverage?
  raise NotImplementedError()
