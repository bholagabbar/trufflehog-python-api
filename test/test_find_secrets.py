import concurrent.futures
import datetime
import unittest

from .context import (SearchConfig, find_secrets, RepoConfig,
                      TrufflehogApiError, Secret, FindSecretsRequest,
                      batch_execute_find_secrets_request)

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

    def test_print_secret(self):
        secret = Secret(commit_time=datetime.datetime(2020, 9, 16),
                        branch_name="branch", commit="commit", diff="diff",
                        commit_hash="commit_hash", reason="reason", path="path")

        # Testing str
        self.assertEqual(str(secret).replace(" ", ""),
                         """commit_time: 2020-09-16 00:00:00,
                         branch_name: branch,
                         commit: commit,
                         commit_hash: commit_hash,
                         reason: reason,
                         path: path """.replace(" ", ""))

        # Testing repr
        self.assertEqual(repr(secret).replace(" ", ""),
                         "Secret(commit_time=2020-09-16 00:00:00, "
                         "branch_name=branch, commit=commit, commit_hash=commit_hash, "
                         "diff=diff, reason=reason, path=path)"
                         .replace(" ", ""))

    def test_to_dict(self):
        secret = Secret(commit_time=datetime.datetime(2020, 9, 16),
                        branch_name="branch", commit="commit", diff="diff",
                        commit_hash="commit_hash", reason="reason", path="path")
        secret_dict = secret.to_dict()
        self.assertEqual(secret_dict["commit_time"], secret.commit_time)
        self.assertEqual(secret_dict["branch_name"], secret.branch_name)
        self.assertEqual(secret_dict["commit"], secret.commit)
        self.assertEqual(secret_dict["diff"], secret.diff)
        self.assertEqual(secret_dict["commit_hash"], secret.commit_hash)
        self.assertEqual(secret_dict["reason"], secret.reason)
        self.assertEqual(secret_dict["path"], secret.path)

    def test_find_secrets_request_creation(self):
        path = "https://github.com/user/test_repo.git"
        branch = "test"
        regexes = SearchConfig.default_regexes()
        include_search_paths = ['*.py']

        repo_config = RepoConfig(branch=branch)
        search_config = SearchConfig(include_search_paths=include_search_paths,
                                     regexes=regexes)

        request = FindSecretsRequest(path,
                                     repo_config=repo_config,
                                     search_config=search_config)

        self.assertEqual(request.path, path)
        self.assertEqual(request.repo_config, repo_config)
        self.assertEqual(request.search_config, search_config)

    def test_find_secrets_request_defaults(self):
        path = "https://github.com/user/test_repo.git"

        request = FindSecretsRequest(path)

        self.assertEqual(request.path, path)
        self.assertEqual(request.repo_config, None)
        self.assertEqual(request.search_config, None)

    def test_find_secrets_request_repr(self):
        path = "https://github.com/user/test_repo.git"
        branch = "test"
        repo_config = RepoConfig(branch=branch)

        request = FindSecretsRequest(path,
                                     repo_config=repo_config)

        self.assertEqual(repr(request), "FindSecretsRequest(path="
                                        "https://github.com/user/test_repo.git, "
                                        "repo_config=RepoConfig(branch=test, "
                                        "since_commit=None, "
                                        "access_token_env_key=None), "
                                        "search_config=None)")

    def test_find_secrets_error(self):
        self.assertRaises(TrufflehogApiError, find_secrets, 'invalid_url')

    def test_batch_execute_find_secrets_request_local(self):
        config = SearchConfig(entropy_checks_enabled=False, regexes=SearchConfig.default_regexes())

        r1 = FindSecretsRequest(".", search_config=config)
        r2 = FindSecretsRequest(".", search_config=config)
        r3 = FindSecretsRequest(".", search_config=config)

        request_list = [r1, r2, r3]

        res = batch_execute_find_secrets_request(request_list)
        for r in res:
            self.assertIsInstance(r, concurrent.futures.Future)
            secrets = r.result()
            for s in secrets:
                self.assertIsInstance(s, Secret)
                self.assertEqual(s.path, "test/resources/test_file.txt")


if __name__ == '__main__':
    unittest.main()
