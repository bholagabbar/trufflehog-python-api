"""
TODO: Documentation
"""

from typing import List
from find_secrets_config import FindSecretsConfig


class Secret():
  """
  TODO: Documentation
  A secret found in a repository.
  """


class SecretFinder():
  """
  TODO: Documentation
  """

  # Maybe we don't need two methods for url vs. path, but I'm not sure
  # the best way to distinguish these strings.
  def find_secrets_with_url(self, git_url: str, settings: FindSecretsConfig) -> List[Secret]:
    """
    TODO: Documentation
    """

  def find_secrets_with_repo_path(self,
                                  repo_path: str,
                                  settings: FindSecretsConfig) -> List[Secret]:
    """
    TODO: Documentation
    """

  # As above, parameters subject to change, may be cleaved
  def find_batch_secrets(self, repo_path: str, settings: FindSecretsConfig) -> List[Secret]:
    """
    TODO: Documentation
    """
