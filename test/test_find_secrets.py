"""
Tests find_secrets methods.
"""
import unittest

from .context import (Repository, RepositoryPathType,
                      SearchConfig, find_secrets)

class TestFindSecrets(unittest.TestCase):
    """Unit tests for find_secrets method."""

    def test_find_secrets(self):
        """Tests if the output from truffleHog's find_strings can be placed in Secret objects"""
        #output = truffleHog.find_strings(None, repo_path=".", do_entropy=False, do_regex=True)
        repo = Repository(path=".", path_type=RepositoryPathType.LOCAL)
        config = SearchConfig()

        secrets = find_secrets(repo, config)
        self.assertIsNot(secrets, [])

    def test_secret(self):
        """Tests that the secrets found by the search are correctly represented in the Secret
        object """
        repo = Repository(path=".", path_type=RepositoryPathType.LOCAL)
        config = SearchConfig(entropy_checks_enabled=False, regexes=SearchConfig.default_regexes())

        found_pgp_secret = False
        path_to_secret = ''
        secrets = find_secrets(repo, config)
        for secret in secrets:
            if secret.reason == "PGP private key block":
                found_pgp_secret = True
                path_to_secret = secret.path

        self.assertTrue(found_pgp_secret)
        self.assertEqual(path_to_secret, "test/resources/test_file.txt")

if __name__ == '__main__':
    unittest.main()
