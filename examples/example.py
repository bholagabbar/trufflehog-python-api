import os
import sys
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from trufflehog_api import *


# Set this locally or in the CI config, value should be Github API Token
TOKEN_ENV_KEY = "TEST_GITHUB_TOKEN"

"""
Default settings:
max_depth = 1000000
    Maximum commit depth to continue search till

include_search_paths = None
    List of regular expressions restricting search to matching object paths only. At least
    one of these must match a Git object path in order for the repository to be searched
    (default is None, all object paths are searched unless otherwise excluded by
    search_paths_excluded)

exclude_search_paths = None
    List of regular expressions restricting search to exclude matching object paths
    (default is None, no object paths are excluded).

entropy_checks_enables = True
    Enable high signal entropy checks, this is the default secret finding mechanism of the
    library. truffleHog will evaluate the shannon entropy for both the base64 char set and
    hexadecimal char set for every blob of text greater than 20 characters comprised  of
    those character sets in each diff. If at any point a high entropy string >20 characters
    is detected
    (default is True, this is the default secret finding mechanism).

regexes = None
    A custom dictionary of regexes, eg. to search for project
    specific strings. The dictionary has keys as the description of a regex and value as
    the the regex string itself. For the user's convenience, the library provides a
    prebuilt regex dict populated with regexes corresponding to popular 3rd party API
    services. This dict is accessible as a static method SearchConfig.default_regexes().
    Search may be slower than than usual
    (default is None, no regexes to search)
"""

"""
Get all paths that contain high entropy strings
This would search for secrets in the current repository with default settings
"""
def simple_search_local():
    suspicious_paths = []
    #Search for secrets in current repository with default settings
    secrets = find_secrets(".")
    for secret in secrets:
        suspicious_paths.append(secret.path)
    return suspicious_paths

"""
Get all paths that contain high entropy strings
This would search for secrets in the truffleHog.git repository with default settings
"""
def simple_search_remote():
    suspicious_paths = []
    #Search for secrets in the given url
    secrets = find_secrets("https://github.com/dxa4481/truffleHog.git")
    for secret in secrets:
        suspicious_paths.append(secret.path)
    return suspicious_paths

"""
Find the secrets in a private remote repo.
Uses TOKEN_ENV_KEY to obtain the access token for the remote private repo
"""
def private_search_remote():
    if TOKEN_ENV_KEY in os.environ:
        print('TOKEN_ENV_KEY is set, attempting to run find_secrets for remote private repo!')
        r_config = RepoConfig(access_token_env_key=TOKEN_ENV_KEY)
        s_config = SearchConfig(entropy_checks_enabled=False,
                                regexes=SearchConfig.default_regexes())

        secrets = find_secrets("https://github.com/4751395/test.git", repo_config=r_config,
                               search_config=s_config)

        for secret in secrets:
            print(secret)
"""
Perform a simple search but with a json string and save the results into a file
"""
def simple_search_with_json():
    s_json_config = """
    {
        "max_depth" : 10000,
        "entropy_checks_enabled" : true
    }
    """
    r_json_config = """
    {
        "branch" : "master",
        "since_commit": "709f22821820a7815106f82a03e8d90f50b2b653"
    }
    """
    s_dict = json.loads(s_json_config)
    r_dict = json.loads(r_json_config)

    #Create a SearchConfig object from the string
    s_config = SearchConfig.from_dict(s_dict)
    #Create a RepoConfig object from the string
    r_config = RepoConfig.from_dict(r_dict)

    # #Search through the truffleHog repo with the search configs specfied in s_config
    # #and the repo configs in r_config
    # #secrets is the List of Secrets that were found by the truffleHog API
    secrets = find_secrets("https://github.com/dxa4481/truffleHog.git",
                           repo_config=r_config,
                           search_config=s_config)

    with open('outputfile.txt', 'w') as output_file:
        for secret in secrets:
            secret_dict = secret.to_dict()
            del secret_dict['diff'] #Do not include the diff
            output_file.write(str(secret_dict) + "\n")


"""
Perform a batch search
"""
def batch_search():
    #Create configurations for the search
    s_config = SearchConfig(max_depth=1000, entropy_checks_enabled=False,
                            regexes=SearchConfig.default_regexes())

    r_config = RepoConfig(since_commit="709f22821820a7815106f82a03e8d90f50b2b653")

    #Generate requests to be executed
    r1 = FindSecretsRequest("https://github.com/dxa4481/truffleHog.git",
                            search_config=s_config,
                            repo_config=r_config)


    r2 = FindSecretsRequest("https://github.com/user/test.git",
                            search_config=s_config,
                            repo_config=r_config)

    r3 = FindSecretsRequest("https://github.com/user/test2.git",
                            search_config=s_config,
                            repo_config=r_config)


    request_list = [r1, r2, r3] #List of requests to be executed

    res = batch_execute_find_secrets_request(request_list)
    for r in res: #for every request
        secrets = r.result()
        for s in secrets:
            print(s)
