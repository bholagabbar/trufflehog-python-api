import unittest

import datetime
from .context import (SearchConfig, find_secrets, Secret)


class TestFindSecrets(unittest.TestCase):

    def test_find_secrets(self):
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

    def test_print_secret(self):
        secret = Secret(commit_time=datetime.datetime(2020, 9, 16),
        branch_name="branch", commit="commit", diff="diff",
        commit_hash="commit_hash", reason="reason", path="path")

        #Testing str
        self.assertEqual(str(secret).replace(" ", ""),
        '''commit_time: 2020-09-16 00:00:00,
        branch_name: branch,
        commit: commit,
        commit_hash: commit_hash,
        reason: reason,
        path: path'''.replace(" ", ""))

        #Testing repr
        self.assertEqual(repr(secret).replace(" ",""), 
        "Secret(commit_time=2020-09-16 00:00:00, " \
        "branch_name=branch, commit=commit, commit_hash=commit_hash, " \
        "diff=diff, reason=reason, path=path)"
        .replace(" ", ""))

    def test_dict(self):

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



if __name__ == '__main__':
    unittest.main()
