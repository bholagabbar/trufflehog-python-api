"""
Contains the RepoConfig class that specifies attributes for a repository
when searching for secrets.
"""
import json

class RepoConfig:
    """Class to encapsulate details of a Git repository to search secrets in.
    """

    def __init__(self, *,
                 branch: str = None,
                 since_commit: str = None,
                 access_token_env_key: str = None):
        """Creates a new RepoConfig object

        :param str branch:
            Branch to restrict search to
            (default is None, all branches searched)

        :param str since_commit:
            Optional commit ID hash to search upwards from
            (default is None, all commits searched)

        :param str access_token_env_key:
            Optional access token key to be extracted from the env vars for remote,
            private repo access
            (default is None, no access key needed to access repo)
        """
        self._branch: str = branch
        self._since_commit: str = since_commit
        self._access_token_env_key: str = access_token_env_key

    @classmethod
    def from_repo_config(cls, repo_config,
                         branch_override: str = None,
                         since_commit_override: str = None,
                         access_token_env_key_override: str = None):
        """Static factory method which creates a new RepoConfig object from an existing RepoConfig
        object allowing user to override certain attributes attributes

        :param RepoConfig repo_config:
            RepoConfig object to copy attributes over from

        :param str branch_override:
            Overridden value for branch to set
            (default is None, value copied over from repo_config)

        :param str since_commit_override:
            Overridden value for since_commit to set
            (default is None, value copied over from repo_config)

        :param str access_token_env_key_override:
            Overridden value for access_token_env_key to set.
            (default is None, value copied over from repo_config)

        :return: An RepoConfig object which is a deep copy of the repo_config object passed
        with optionally overridden passed values.
        """
        branch_to_set = repo_config.branch
        if branch_override:
            branch_to_set = branch_override

        since_commit_to_set = repo_config.since_commit
        if since_commit_override:
            since_commit_to_set = since_commit_override

        access_token_env_key_to_set = repo_config.access_token_env_key
        if access_token_env_key_override:
            access_token_env_key_to_set = access_token_env_key_override

        return cls(branch=branch_to_set,
                   since_commit=since_commit_to_set,
                   access_token_env_key=access_token_env_key_to_set)

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
    def access_token_env_key(self) -> str:
        """
        :return: Access token key to be extracted from the env vars for remote private repo access
        """
        return self._access_token_env_key

    @staticmethod
    def from_dict(config_dict: dict()):

        """
        Takes a dictionary with the desired configurations and generates a RepoConfig object

        Dict Format \t
        {\t
            "branch": string, \t
            "since_commit": string, \t
            "access_token_env": string \t
        }\t

        :param str input_config:
            The json string containing the configuration

        :return: Returns a RepoConfig from the a json string
        """
        branch = None
        since_commit = None
        access_token_env_key = None

        if "branch" in config_dict:
            branch = config_dict["branch"]
        if "since_commit" in config_dict:
            since_commit = config_dict["since_commit"]
        if  "access_token_env_key" in config_dict:
            access_token_env_key = config_dict["access_token_env_key"]

        return RepoConfig(branch=branch, since_commit=since_commit,
                          access_token_env_key=access_token_env_key)

    def __str__(self):
        """
        :return: A string with the RepoConfig object's attributes
        """
        config_dict = dict()
        config_dict["branch"] = self._branch
        config_dict["since_commit"] = self._since_commit
        return json.dumps(config_dict, indent=2)

    def to_dict(self):
        """
        :return: A dict with the RepoConfig object's attributes
        """
        config_dict = dict()
        config_dict["branch"] = self._branch
        config_dict["since_commit"] = self._since_commit
        return config_dict

    def __repr__(self):
        """
        :return: A string listing out the RepoConfig object's attributes
        attributes
        """
        return ('RepoConfig(branch={0}, since_commit={1}, access_token_env_key={2})'
                .format(str(self.branch), str(self.since_commit), str(self.access_token_env_key)))
