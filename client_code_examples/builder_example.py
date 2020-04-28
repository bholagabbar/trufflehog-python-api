"""
Example of how to use the SearchConfigBuilder.
"""

from trufflehog_api import FindSecretsConfigBuilder


def main():
  """
  Creates and prints a builder.
  """
  builder = FindSecretsConfigBuilder()
  builder.set_branch('dev').set_entropy_checks_enabled(False).set_since_commit('beaedf0d4217b10901b7234001761dd6305cbace')

  print(builder)

  print("Branch: %s" % builder.branch)

  # Currently fails since there is no default
  # print(builder.max_depth())

if __name__ == '__main__':
  main()
