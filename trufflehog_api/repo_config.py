"""
Contains the RepoConfig class that specifies attributes for a repository
when searching for secrets.
"""

class RepoConfig:
    """Class to encapsulate details of a Git repository to search secrets in.
    """

    def __init__(self, *,
                 branch: str = None,
                 since_commit: str = None):
        """Creates a new RepoConfig

        :param str branch:
            Branch to restrict search to
            (default is None, all branches searched)

        :param str since_commit:
            Optional commit ID hash to search upwards from
            (default is None, all commits searched)
        """
        self._branch: str = branch
        self._since_commit: str = since_commit

    @classmethod
    def from_repo_config(cls, repoconfig, branch: str = None, since_commit: str = None):
        """Static factory method which creates a new RepoConfig from an existing repoconfig,
        allowing user to override branch and since_commit attributes

        :param RepoConfig repoconfig:
            RepoConfig object to copy attributes over from

        :param str branch:
            Overridden value for branch to set
            (default is None)

        :param str since_commit:
            Overridden value for since_commit to set
            (default is None)

        :return: An RepoConfig object which is a deep copy of the repoconfig parameter passed
        with optionally overridden passed values.
        """
        branch_to_set = branch if branch else repoconfig.branch
        since_commit_to_set = since_commit if since_commit else repoconfig.since_commit

        return cls(branch=branch_to_set,
                   since_commit=since_commit_to_set)

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


    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        """
        :return: A string with the repoconfig's branch and since_commit
        attributes
        """
        return ('RepoConfig(branch={0}, since_commit={1})'
                .format(str(self.branch), str(self.since_commit)))
