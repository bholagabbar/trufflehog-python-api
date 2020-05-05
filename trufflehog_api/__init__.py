"""
A rewritten version of the truffleHog API [1].

[1]: https://github.com/dxa4481/truffleHog/tree/53a16df0a6f9a56ec11ad85abd193ea6feac5ff1
"""

from trufflehog_api.find_secrets import (Secret, find_secrets)
from trufflehog_api.repository import (Repository, RepositoryPathType)
from trufflehog_api.search_config import SearchConfig
