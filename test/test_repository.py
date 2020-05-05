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

    def test_from_repository(self):
        r1_path = 'test_path'
        r1_branch = 'master'
        r1 = Repository(path=r1_path, branch=r1_branch)
        r2_branch = 'segment'
        r2 = Repository.from_repository(r1, branch=r2_branch)

        self.assertEqual(r2.path, r1.path)
        self.assertEqual(r2.path_type, r1.path_type)
        self.assertEqual(r2.since_commit, r1.since_commit)
        self.assertEqual(r2.branch, r2_branch)


if __name__ == '__main__':
    unittest.main()
