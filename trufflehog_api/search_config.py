import json
from copy import copy
from typing import List, Dict

from truffleHogRegexes.regexChecks import regexes as default_regexes


class SearchConfig:
    """Class to hold trufflehog_api's search configurations
    """

    def __init__(self, *,
                 max_depth: int = 1000000,
                 include_search_paths: List[str] = None,
                 exclude_search_paths: List[str] = None,
                 entropy_checks_enabled: bool = True,
                 regexes: Dict[str, str] = None,
                 ):
        """Creates a new default search configuration object with entropy and regex checks off

        :param str max_depth:
            Maximum commit depth to continue search till (default is 1000000)
        :param list include_search_paths:
            List of regular expressions restricting search to matching object paths only. At least
            one of these must match a Git object path in order for the repository to be searched
            (default is None, all object paths are searched unless otherwise excluded by
            search_paths_excluded)
        :param list exclude_search_paths:
            List of regular expressions restricting search to exclude matching object paths
            (default is None, no object paths are excluded).
        :param str entropy_checks_enabled:
            Enable high signal entropy checks, this is the default secret finding mechanism of the
            library. truffleHog will evaluate the shannon entropy for both the base64 char set and
            hexadecimal char set for every blob of text greater than 20 characters comprised  of
            those character sets in each diff. If at any point a high entropy string >20 characters
            is detected
            (default is True, this is the default secret finding mechanism).
        :param dict regexes:
            Use this argument to pass in a custom dictionary of regexes, eg. to search for project
            specific strings. The dictionary has keys as the description of a regex and value as
            the the regex string itself. For the user's convenience, the library provides a
            prebuilt regex dict populated with regexes corresponding to popular 3rd party API
            services. This dict is accessible as a static method SearchConfig.default_regexes().
            Search may be slower than than usual
            (default is None, no regexes to search)
        """

        self._max_depth: int = max_depth
        self._entropy_checks_enabled: bool = entropy_checks_enabled

        # Defensively copy all mutable arguments passed
        self._include_search_paths: List[str] = copy(include_search_paths)
        self._exclude_search_paths: List[str] = copy(exclude_search_paths)
        self._regexes: Dict[str, str] = copy(regexes)

    @property
    def max_depth(self) -> int:
        """
        :return: Returns an integer which is the the maximum commit depth to continue
        search till
        """
        return self._max_depth

    @property
    def include_search_paths(self) -> List[str]:
        """
        :return: Returns a copy of the list of regexes restricting search to matching
        object paths only
        """
        return copy(self._include_search_paths)

    @property
    def exclude_search_paths(self) -> List[str]:
        """
        :return: Returns a copy of the list of regexes restricting search to exclude
        matching object paths.
        """
        return copy(self._exclude_search_paths)

    @property
    def entropy_checks_enabled(self) -> bool:
        """
        :return: Returns a boolean value indicating whether entropy checks are enabled
        """
        return self._entropy_checks_enabled

    @property
    def regexes(self) -> Dict[str, str]:
        """
        :return: Returns a copy of the dict of custom regexes to search search matching
        project strings against
        """
        return copy(self._regexes)

    @staticmethod
    def default_regexes() -> Dict[str, str]:
        """
        :return: Returns a copy of the prebuilt regex dict provided by truffleHogRegexes
        library
        """
        return copy(default_regexes)

    @staticmethod 
    def from_str(input_config: str):
        """
        :return: Returns a SearchConfig from the a dictionary string 
        """ 
        config_dict = json.loads(input_config)
        max_depth = 1000000
        include_search_paths = None
        exclude_search_paths = None
        entropy_checks_enabled = True
        regexes = None
                
        if "max_depth" in config_dict:
            max_depth = int(config_dict["max_depth"])
        if "include_search_paths" in config_dict:
            include_search_paths = config_dict.get("include_search_paths")
        if "exclude_search_paths" in config_dict:
            exclude_search_paths = config_dict.get("exclude_search_paths")
        if "entropy_checks_enabled" in config_dict:
            entropy_checks_enabled = config_dict.get("entropy_checks_enabled")
            if entropy_checks_enabled.lower() == "true":
                entropy_checks_enabled = True
            else:
                entropy_checks_enabled = False
        if "regexes" in config_dict:
            regexes = json.loads(config_dict.get("regexes"))

        config = SearchConfig(
                 max_depth=max_depth,
                 include_search_paths=include_search_paths,
                 exclude_search_paths=exclude_search_paths,
                 entropy_checks_enabled=entropy_checks_enabled,
                 regexes=regexes,
                 )

        return config

    def __str__(self):
        """
        :return: Returns a dictionary string containing all the attributes of the SearchConfig
        """
        string =  "max_depth: {max_depth}, \nentropy_checks_enabled: {entropy_enabled}, \ninclude_search_paths: {incl_search_paths}, \nexclude_search_paths: {excl_search_paths}, \nregexes: {regexes}".format(max_depth=str(self._max_depth), 
            entropy_enabled=str(self._entropy_checks_enabled),
            incl_search_paths=str(self._include_search_paths),
            excl_search_paths=str(self._exclude_search_paths),
            regexes=str(self._regexes));
        return "{\n" + string + "\n}"

    def __repr__(self):
        """
        :return: Returns a string containing all the attributes of the SearchConfig
        """
        return ("SearchConfig(max_depth={entropy_enabled}, include_search_parts={incl_search_paths}, exclude_seach_parts={excl_search_paths}, entropy_checks_enabled={entropy_enabled}, regexes={regexes}").format(max_depth=str(self._max_depth), 
            entropy_enabled=str(self._entropy_checks_enabled),
            incl_search_paths=str(self._include_search_paths),
            excl_search_paths=str(self._exclude_search_paths),
            regexes=str(self._regexes));
