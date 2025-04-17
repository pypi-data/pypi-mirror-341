import sys
import requests

from pyfunc2.github.getHeaders import getHeaders

# Retrieve a list of all repositories within the organization
def get_repos(api_token, org_name):
    url = f'https://api.github.com/orgs/{org_name}/repos?per_page=100'
    response = requests.get(url, headers=getHeaders(api_token))

    if response.status_code!= 200:
        print('Failed to retrieve repositories:', response.content)
        return

    return response