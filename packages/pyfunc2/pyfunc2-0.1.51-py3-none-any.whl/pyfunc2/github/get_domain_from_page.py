import sys
import requests


from pyfunc2.github.getHeaders import getHeaders

# Retrieve a list of all repositories within the organization
def get_domain_from_page(api_token, owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/pages'
    response = requests.get(url, headers=getHeaders(api_token))

    if response.status_code != 200:
        print('Failed to retrieve repositories:', response.content)
        return

    return response