"""
Tests find_secrets methods.
"""
import unittest

from .context import (SearchConfig, find_secrets)

class TestFindSecrets(unittest.TestCase):
    """Unit tests for find_secrets method."""

    def test_find_secrets(self):
        """Tests if the output from truffleHog's find_strings can be placed in Secret objects"""
        #output = truffleHog.find_strings(None, repo_path=".", do_entropy=False, do_regex=True)
        secrets = find_secrets(".")
        self.assertIsNot(secrets, [])

    def test_secret(self):
        """Tests that the secrets found by the search are correctly represented in the Secret
        object """
        config = SearchConfig(entropy_checks_enabled=False, regexes=SearchConfig.default_regexes())

        secrets = find_secrets(".", search_config=config)
        self.assertIsNot(secrets, [])

        found_pgp_secret = False
        path_to_secret = ''
        for secret in secrets:
            if secret.reason == "PGP private key block":
                found_pgp_secret = True
                path_to_secret = secret.path

        self.assertTrue(found_pgp_secret)
        self.assertEqual(path_to_secret, "test/resources/test_file.txt")

if __name__ == '__main__':
    unittest.main()
