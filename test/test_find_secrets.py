"""
Tests find_secrets methods.
"""
import unittest

from .context import (Repository, RepositoryPathType,
                      SearchConfig, Secret, find_secrets)

class TestFindSecrets(unittest.TestCase):
    """Unit tests for find_secrets method."""

    def test_find_secrets(self):
        """Tests if the output from truffleHog's find_strings can be placed in Secret objects"""
        #output = truffleHog.find_strings(None, repo_path=".", do_entropy=False, do_regex=True)
        repo = Repository(path=".", path_type=RepositoryPathType.LOCAL)
        config = SearchConfig()

        secrets = find_secrets(repo, config)
        self.assertIsNot(secrets, [])

if __name__ == '__main__':
    unittest.main()
