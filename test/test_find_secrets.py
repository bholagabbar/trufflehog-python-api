import unittest

import datetime
from .context import (SearchConfig, find_secrets, Secret)


class TestFindSecrets(unittest.TestCase):

    def test_find_secrets(self):
        output = truffleHog.find_strings(None, repo_path=".", do_entropy=False, do_regex=True)
        secrets = find_secrets(".")
        self.assertIsNot(secrets, [])

    def test_secret(self):
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

    def print_secret(self):
        print("got here")
        secret = Secret(datetime.datetime(2020,9,16), "branch", "prev_commit", "diff",
        "commit_hash", "reason", "path")
        print(secret)

if __name__ == '__main__':
    print("dsffds")
    unittest.main()
