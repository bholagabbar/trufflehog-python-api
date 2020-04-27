"""
A rewritten version of the truffleHog API [1].

[1]: https://github.com/dxa4481/truffleHog/tree/53a16df0a6f9a56ec11ad85abd193ea6feac5ff1
"""

from .find_secrets import (Secret, find_secrets, find_secrets_local,
                           find_secrets_remote)
from .find_secrets_config import FindSecretsConfig, FindSecretsConfigBuilder
