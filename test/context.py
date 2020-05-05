from __future__ import absolute_import

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import trufflehog_api

# Copy import style from trufflehog_api.__init__.py
from trufflehog_api import RepoConfig
from trufflehog_api.search_config import SearchConfig
from trufflehog_api.find_secrets import (Secret, find_secrets)
