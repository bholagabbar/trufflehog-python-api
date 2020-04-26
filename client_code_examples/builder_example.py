"""
Example of how to use the SearchConfigBuilder.
"""

from trufflehog_api import FindSecretsConfigBuilder


def __main__():
  builder = FindSecretsConfigBuilder()
  print(builder)
