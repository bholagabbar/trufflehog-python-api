import os
import unittest

from .context import (SearchConfig, find_secrets, RepoConfig)

# Set this locally or in the CI config, value should be Github API Token
TOKEN_ENV_KEY = "TEST_GITHUB_TOKEN"


class TestFindSecrets(unittest.TestCase):

    def test_find_secrets_local(self):
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

    def test_find_secrets_remote(self):
        # If value for TOKEN_ENV_KEY has been set in CI, runs the complete remote find_secrets flow
        if TOKEN_ENV_KEY in os.environ:
            print('TOKEN_ENV_KEY is set, attempting to run find_secrets for remote private repo!')

            r_config = RepoConfig(access_token_env_key=TOKEN_ENV_KEY)
            s_config = SearchConfig(entropy_checks_enabled=False,
                                    regexes=SearchConfig.default_regexes())

            # Private remote git repository created specifically for testing
            secrets = find_secrets("https://github.com/4751395/test.git", repo_config=r_config,
                                   search_config=s_config)

            self.assertIsNot(secrets, [])
            self.assertEqual(len(secrets), 2)

            num_generic_secrets = 0
            secret_hashes = []
            for secret in secrets:
                if secret.reason == "Generic Secret":
                    num_generic_secrets += 1
                secret_hashes.append(secret.commit_hash)

            self.assertEqual(num_generic_secrets, 2)
            self.assertTrue("756568e922f868d798949f1d25c5b08292dcc49b" in secret_hashes)
            self.assertTrue("ed8aab163431cbea0886db4961f5f9bde172cdd4" in secret_hashes)
        else:
            print('TOKEN_ENV_KEY, skipped execution!')


if __name__ == '__main__':
    unittest.main()
