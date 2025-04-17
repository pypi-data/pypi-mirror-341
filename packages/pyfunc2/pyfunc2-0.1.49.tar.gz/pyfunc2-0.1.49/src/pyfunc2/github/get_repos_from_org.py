import sys
import requests



def get_repos_from_org(org_name, headers):
    repos_url = f'https://api.github.com/orgs/{org_name}/repos'
    response = requests.get(repos_url, headers=headers)
    print(response)
    return response.json() if response.status_code == 200 else None