from enum import Enum


class RepositoryPathType(Enum):
    """Indicates whether a repository path is a remote git url or local filesystem path
    """
    REMOTE = 'REMOTE'
    LOCAL = 'LOCAL'


class Repository:
    """Class to encapsulate details of a Git repository to search secrets in.
    """

    def __init__(self, *,
                 path: str,
                 branch: str = None,
                 since_commit: str = None,
                 path_type: RepositoryPathType = RepositoryPathType.REMOTE):
        """Creates a new repository

        :param str path:
            Path of the repository.
        :param str branch:
            Branch to restrict search to
            (default is None, all branches searched)
        :param str since_commit:
            Optional commit ID hash to search upwards from
            (default is None, all commits searched)
        :param RepositoryPathType path_type:
            Indicates type of the repository
            (default is RepositoryPathType.REMOTE)
        """
        self._path: str = path
        self._branch: str = branch
        self._since_commit: str = since_commit
        self._path_type: RepositoryPathType = path_type

    @classmethod
    def from_repository(cls, repository, branch: str = None, since_commit: str = None):
        """Static factor method which creates a new repository from an existing repository,
        allowing user to override branch and since_commit attributes

        :param Repository repository:
            Repository object to copy attributes over from.
            (default is None)
        :param str branch:
            Overridden value for branch to set.
            (default is None)
        :param str since_commit:
            Overridden value for since_commit to set.
            (default is None)
        :return: An Repository object which is a deep copy of the repository parameter passed
        with optionally overridden passed values.
        """
        branch_to_set = branch if branch else repository.branch
        since_commit_to_set = since_commit if since_commit else repository.since_commit

        return cls(path=repository.path, path_type=repository.path_type, branch=branch_to_set,
                   since_commit=since_commit_to_set)

    @property
    def path(self) -> str:
        """
        :return: Path to access the repository.
        """
        return self._path

    @property
    def branch(self) -> str:
        """
        :return: The specific branch to search for in the repository
        """
        return self._branch

    @property
    def since_commit(self) -> str:
        """
        :return: Specific commit ID hash to search upwards from
        """
        return self._since_commit

    @property
    def path_type(self) -> RepositoryPathType:
        """
        :return: Indicates whether a repository path is git remote or local filesystem path
        """
        return self._path_type

    def __str__(self):
        """
        :return: The repository's path
        """
        return self.path

    def __repr__(self):
        """
        :return: A string with the repository's path, branch, since_commit
        and path_type attributes
        """
        return ('Repository(path={0}, branch={1}, since_commit={2}, path_type={3})'
                .format(self.path_type, str(self.branch), str(self.since_commit),
                        str(self.path_type)))
