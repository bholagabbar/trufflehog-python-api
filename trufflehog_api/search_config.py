from typing import List
from typing import Dict
from truffleHogRegexes.regexChecks import regexes


class SearchConfig:
    """Class to hold truffleHog search configurations
    """

    def __init__(self, *,
                 max_depth: int = 1000000,
                 search_paths_included: List[str] = None,
                 search_paths_excluded: List[str] = None):
        """Creates a new default search configuration object with entropy and regex checks switched off

        :param str max_depth:
            Maximum commit depth to continue search till (default is 1000000)
        :param str search_paths_included:
            List of regular expressions restricting search to matching object paths only. At least
            one of these must match a Git object path in order for the repository to be searched
            (default is None, all object paths are searched unless otherwise excluded by search_paths_excluded)
        :param str search_paths_excluded:
            List of regular expressions restricting search to exclude matching object paths
            (default is None, no object paths are excluded).
        """
        self._max_depth: int = max_depth
        self._search_paths_included: List[str] = search_paths_included
        self._search_paths_excluded: List[str] = search_paths_excluded

        # Set defaults
        self._entropy_checks_enabled = False
        self._regex_search_enabled = False
        self._regex_dict = regexes.copy()

    @property
    def max_depth(self) -> int:
        """Maximum commit depth to continue search till.
        """
        return self._max_depth

    @property
    def search_paths_included(self) -> List[str]:
        """List of regular expressions restricting search to matching object paths only.
        """
        return self._search_paths_included

    @property
    def search_paths_excluded(self) -> List[str]:
        """List of regular expressions restricting search to exclude matching object paths.
        """
        return self._search_paths_excluded

    @property
    def entropy_checks_enabled(self) -> bool:
        """Indicates whether entropy checks are enabled
        """
        return self._entropy_checks_enabled

    @property
    def regex_checks_enabled(self) -> bool:
        """Indicates whether high signal regex checks are enabled
        """
        return self._entropy_checks_enabled

    @property
    def regex_dict(self) -> Dict:
        """Returns a copy of the dictionary storing the high signal regexes used for the regex search
        (default dict is provided by truffleHogRegexes package)
        """
        return self._regex_dict.copy()

    def with_entropy_checks_enabled(self):
        """Builder method to enable entropy checks for the search configuration object
        """
        self._entropy_checks_enabled = True
        return self

    def with_regex_checks_enabled(self, override_regex_dict=None):
        """Builder method to enable regex checks for the search configuration object

        :param dict override_regex_dict:
            Allows the user to override the default regex dictionary by creating a copy of the object passed
            and assigning it as the object's regex_dict
        """
        self._regex_search_enabled = True
        if override_regex_dict:
            _regex_search_dict = override_regex_dict.copy()
        return self

    def __str__(self):
        """
        TODO
        """
        raise NotImplementedError()

    def __repr__(self):
        """
        TODO
        """
        raise NotImplementedError()
