"""
Example of how to use the SearchConfigBuilder.
"""

from trufflehog_api import FindSecretsConfigBuilder


def main():
  """
  Creates and prints a builder.
  """
  builder = FindSecretsConfigBuilder()
  print(builder)

if __name__ == '__main__':
  main()
