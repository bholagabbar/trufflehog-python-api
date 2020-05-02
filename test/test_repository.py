import unittest
from .context import Repository


class TestRepository(unittest.TestCase):

    def test_default_repository_creation(self):
        test_path = 'test_path'
        r = Repository(path=test_path)
        self.assertEqual(r.path, test_path, "Path should match")
        self.assertEqual(r.path_type.value, 'REMOTE')
        self.assertIsNone(r.branch)
        self.assertIsNone(r.since_commit)

    def test_custom_repository_creation(self):
        test_path = 'test_path'
        test_branch = 'master'
        test_commit = 'x123'
        r = Repository(path=test_path, branch=test_branch, since_commit=test_commit)
        self.assertEqual(r.path, test_path, "Path should match")
        self.assertEqual(r.branch, test_branch, "since branch should match")
        self.assertEqual(r.since_commit, test_commit, "since commit should match")

    def test_repository_str(self):
        test_path = 'test_path'
        r = Repository(path=test_path)
        self.assertEqual(r.__str__(), r.path)

    def test_repository_repr(self):
        test_path = 'test_path'
        r = Repository(path=test_path)
        self.assertEqual(r.__repr__(), 'Repository(path=RepositoryPathType.REMOTE, branch=None, '
                                       'since_commit=None, path_type=RepositoryPathType.REMOTE)')


if __name__ == '__main__':
    unittest.main()
