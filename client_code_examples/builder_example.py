"""
Example of how to use the SearchConfigBuilder.
"""

from trufflehog_api import FindSecretsConfigBuilder


def main():
  """
  Creates and prints a builder.
  """
  builder = FindSecretsConfigBuilder()
  builder.with_branch('dev').with_enable_entropy_checks(False).with_since_commit(150)

  print(builder)

  print("Branch: %s" % builder.branch)

  # Currently fails since there is no default
  # print(builder.max_depth())

if __name__ == '__main__':
  main()
