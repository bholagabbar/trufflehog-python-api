import unittest

from truffleHogRegexes.regexChecks import regexes as default_regexes

from .context import SearchConfig


class TestSearchConfig(unittest.TestCase):

    def test_creation(self):
        include_search_paths = ['*.py']
        exclude_search_paths = ['/docs']
        regexes = {"random": ".*"}
        search_config = SearchConfig(max_depth=10,
                                     include_search_paths=include_search_paths,
                                     exclude_search_paths=exclude_search_paths,
                                     regexes=regexes
                                     )
        self.assertEqual(search_config.max_depth, 10)
        self.assertCountEqual(search_config.include_search_paths, include_search_paths)
        self.assertCountEqual(search_config.exclude_search_paths, exclude_search_paths)
        self.assertCountEqual(search_config.regexes, regexes)

    def test_immutability(self):
        include_search_paths = ['*.py']
        exclude_search_paths = ['/docs']
        regexes = {"random": ".*"}
        search_config = SearchConfig(max_depth=10,
                                     include_search_paths=include_search_paths,
                                     exclude_search_paths=exclude_search_paths,
                                     regexes=regexes
                                     )
        # Object references should be different
        self.assertTrue(regexes is regexes)
        self.assertTrue(search_config.include_search_paths is not include_search_paths)
        self.assertTrue(search_config.exclude_search_paths is not exclude_search_paths)
        self.assertTrue(search_config.regexes is not regexes)

    def test_default_dict(self):
        # Content should be same, references should be different
        self.assertCountEqual(SearchConfig.default_regexes(), default_regexes)
        self.assertTrue(SearchConfig.default_regexes() is not default_regexes)

    def test_str(self):
        # TODO
        return

    def test_repr(self):
        # TODO
        return


if __name__ == '__main__':
    unittest.main()
