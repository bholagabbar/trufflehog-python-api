import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from trufflehog_api import *


'''
Get all paths that contain high entropy strings 
This would search for secrets in the current repository with default settings

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
'''
def simple_search_local(): 
    suspicious_paths = []
    #Search for secrets in current repository with default settings
    secrets = find_secrets(".")
    for secret in secrets:
        suspicious_paths.append(secret.path)
    return suspicious_paths

'''
Get all paths that contain high entropy strings 
This would search for secrets in the truffleHog.git repository with default settings
'''
def simple_search_remote(): 
    suspicious_paths = []
    #Search for secrets in the given url
    secrets = find_secrets("https://github.com/dxa4481/truffleHog.git")
    for secret in secrets:
        suspicious_paths.append(secret.path)
    return suspicious_paths

simple_search_local()

'''
Find the secrets in a private remote repo. 
Uses TOKEN_ENV_KEY to obtain the access token for the remote private repo
'''
def private_search_remote():
    if TOKEN_ENV_KEY in os.environ:
        print('TOKEN_ENV_KEY is set, attempting to run find_secrets for remote private repo!')
        r_config = RepoConfig(access_token_env_key=TOKEN_ENV_KEY)
        s_config = SearchConfig(entropy_checks_enabled=False, \
                                regexes=SearchConfig.default_regexes())

        secrets = find_secrets("https://github.com/4751395/test.git", repo_config=r_config, \
                               search_config=s_config)

        return secrets
    else: 
        return []

'''
Find the secrets with the set configurations 
Save the secrets to a file specified in filename
'''
def save_search_to_file(filename: str):
    return ""

'''
Perform a simple search but with a json string
'''
def simple_search_with_json():
    s_config = '''
    {
        "max_depth" : 10000,
        "entropy_checks_enabled" : true, 
        "regexes" : "default"
    }
    '''                        
    r_config = '''
    {
        "branch" : "master", 
        "since_commit" : "53a16df0a6f9a56ec11ad85abd193ea6feac5ff1"
    }
    '''
    
    SearchConfig.from_str(s_config)
    RepoConfig.from_str(r_config)

    #Search through the truffleHog repo with the search configs specfied in s_config
    #and the repo configs in r_config
    #secrets is the List of Secrets that were found by the truffleHog API
    secrets = find_secrets("https://github.com/dxa4481/truffleHog.git", \
                            repo_config=r_config, \
                            search_config=s_config)

    #Loop through the secrets generated in the first search
    for secret in secrets:
        print(secret) #Print each secret formatted with all the attributes
        print(secret.commit_time) #Time when the secret was committed
        print(secret.branch_name) #Branch where the secret was committed
        print(secret.commit) #Commit where the secret was found
        print(secret.diff) #Git diff where secret can be found
        print(secret.commit_hash) #Commit hash for the commit where the secret was found
        print(secret.reason) #Reason why the secret was flagged (Eg. regex description or High Entropy)
        print(secret.path) #Path to file in which secret can be found

