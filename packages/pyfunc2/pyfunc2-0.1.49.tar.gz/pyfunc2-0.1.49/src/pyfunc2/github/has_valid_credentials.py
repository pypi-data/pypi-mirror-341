import sys
import requests


def has_valid_credentials(org_name, headers):
    repos_url = f'https://api.github.com/orgs/{org_name}/repos'
    response = requests.get(repos_url, headers=headers)
    #print(response.status_code)
    return response.status_code != 401