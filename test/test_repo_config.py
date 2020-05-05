import unittest

from test.context import RepoConfig


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

    # TODO: Fix when we get representation
    #def test_repository_str(self):
    #    test_path = 'test_path'
    #    r = RepoConfig(path=test_path)
    #    self.assertEqual(r.__str__(), r.path)

    def test_repository_repr(self):
        r = RepoConfig()
        self.assertEqual(r.__repr__(), 'RepoConfig(branch=None, '
                                       'since_commit=None)')

    def test_from_repo_config(self):
        r1_branch = 'master'
        r1 = RepoConfig(branch=r1_branch)
        r2_branch = 'segment'
        r2 = RepoConfig.from_repo_config(r1, branch=r2_branch)

        self.assertEqual(r2.since_commit, r1.since_commit)
        self.assertEqual(r2.branch, r2_branch)


if __name__ == '__main__':
    unittest.main()
