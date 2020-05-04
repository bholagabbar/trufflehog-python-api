from copy import copy
from typing import List
from typing import Dict
from truffleHogRegexes.regexChecks import regexes as default_regexes


class SearchConfig:
    """Class to hold truffleHog search configurations
    """

    def __init__(self, *,
                 max_depth: int = 1000000,
                 include_search_paths: List[str] = None,
                 exclude_search_paths: List[str] = None,
                 entropy_checks_enabled: bool = True,
                 regexes: Dict[str, str] = None,
                 ):
        """Creates a new default search configuration object with entropy and regex checks switched off

        :param str max_depth:
            Maximum commit depth to continue search till (default is 1000000)
        :param str include_search_paths:
            List of regular expressions restricting search to matching object paths only. At least
            one of these must match a Git object path in order for the repository to be searched
            (default is None, all object paths are searched unless otherwise excluded by search_paths_excluded)
        :param str exclude_search_paths:
            List of regular expressions restricting search to exclude matching object paths
            (default is None, no object paths are excluded).
        :param str entropy_checks_enabled:
            Enable high signal entropy checks, this is the default secret finding mechanism of the library.
            truffleHog will evaluate the shannon entropy for both the base64 char set and hexadecimal char set
            for every blob of text greater than 20 characters comprised  of those character sets in each diff.
            If at any point a high entropy string >20 characters is detected
            (default is True, this is the default secret finding mechanism in the library).
        :param dict regexes:
            Use this argument to pass in a custom dictionary of regexes, eg. to search for project specific
            strings. The dictionary has keys as the description of a regex and value as the the regex string
            itself. For the user's convenience, the library provides a prebuilt regex dict populated with
            regexes corresponding to popular 3rd party API services. This dict is accessible as a static method
            SearchConfig.default_regexes(). Search may be slower than than usual (default is None, no regexes to search)
        """

        self._max_depth: int = max_depth
        self._entropy_checks_enabled: bool = entropy_checks_enabled

        # Defensively copy all mutable arguments passed
        self._include_search_paths: List[str] = copy(include_search_paths)
        self._exclude_search_paths: List[str] = copy(exclude_search_paths)
        self._regexes: Dict[str, str] = copy(regexes)

    @property
    def max_depth(self) -> int:
        """Returns an integer corresponding to the maximum commit depth to continue search till.
        """
        return self._max_depth

    @property
    def include_search_paths(self) -> List[str]:
        """Returns a copy of the list of regular expressions restricting search to matching object paths only.
        """
        return copy(self._include_search_paths)

    @property
    def exclude_search_paths(self) -> List[str]:
        """Returns a copy of the list of regular expressions restricting search to exclude matching object paths.
        """
        return copy(self._exclude_search_paths)

    @property
    def entropy_checks_enabled(self) -> bool:
        """Returns a boolean value indicating whether entropy checks are enabled
        """
        return self._entropy_checks_enabled

    @property
    def regexes(self) -> Dict[str, str]:
        """Returns a copy of the dict of custom regexes to search search matching project strings against
        """
        return copy(self._regexes)

    @staticmethod
    def default_regexes() -> Dict[str, str]:
        """
        Returns a copy of the prebuilt regex dict provided by truffleHogRegexes
        populated with regexes corresponding to popular 3rd party API services
        """
        return copy(default_regexes)

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
