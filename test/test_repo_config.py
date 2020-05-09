import unittest
import json

from .context import RepoConfig


class TestRepoConfig(unittest.TestCase):

    def test_default_repository_creation(self):
        r = RepoConfig()
        self.assertIsNone(r.branch)
        self.assertIsNone(r.since_commit)

    def test_custom_repository_creation(self):
        test_branch = 'master'
        test_commit = 'x123'
        r = RepoConfig(branch=test_branch, since_commit=test_commit)
        self.assertEqual(r.branch, test_branch, "since branch should match")
        self.assertEqual(r.since_commit, test_commit, "since commit should match")

    def test_from_dict(self):
        config = """
        {
            "branch" : "master",
            "since_commit": "123"
        }
        """
        config_dict = json.loads(config)
        r_config = RepoConfig.from_dict(config_dict)
        self.assertEqual(r_config.branch, "master")
        self.assertEqual(r_config.since_commit, "123")

    def test_repository_str(self):
        test_branch = 'master'
        test_commit = 'x123'
        test_dict = dict()
        test_dict["branch"] = test_branch
        test_dict["since_commit"] = test_commit
        r_config = RepoConfig(branch=test_branch, since_commit=test_commit)
        self.assertEqual(r_config.__str__(), json.dumps(test_dict, indent=2))

    def test_repository_repr(self):
        r = RepoConfig()
        self.assertEqual(r.__repr__(), 'RepoConfig(branch=None, '
                                       'since_commit=None, '
                                       'access_token_env_key=None)')

    def test_from_repo_branch(self):
        r1_branch = 'master'
        r1 = RepoConfig(branch=r1_branch)
        r2_branch = 'segment'
        r2 = RepoConfig.from_repo_config(r1, branch_override=r2_branch)

        self.assertEqual(r2.branch, r2_branch)
        self.assertEqual(r2.since_commit, r1.since_commit)

    def test_from_repo_since_commit(self):
        r1_since_commit = 'x1234'
        r1 = RepoConfig(since_commit=r1_since_commit)
        r2_since_commit = 'x4567'
        r2 = RepoConfig.from_repo_config(r1, since_commit_override=r2_since_commit)

        self.assertEqual(r2.since_commit, r2_since_commit)
        self.assertEqual(r2.branch, r1.branch)

    def test_from_repo_config_token(self):
        r1 = RepoConfig()
        self.assertIsNone(r1.access_token_env_key)

        r2_access_token_env_key = 'GITHUB_ACCESS_TOKEN_NA'
        r2 = RepoConfig.from_repo_config(r1, access_token_env_key_override=r2_access_token_env_key)
        self.assertEqual(r2.access_token_env_key, r2_access_token_env_key)

        r3_access_token_env_key = 'GITHUB_ACCESS_TOKEN_EU'
        r3 = RepoConfig.from_repo_config(r1, access_token_env_key_override=r3_access_token_env_key)
        self.assertEqual(r3.access_token_env_key, r3_access_token_env_key)


if __name__ == '__main__':
    unittest.main()
