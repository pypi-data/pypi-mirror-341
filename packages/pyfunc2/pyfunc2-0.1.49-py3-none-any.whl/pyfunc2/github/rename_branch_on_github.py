import sys
import requests


from pyfunc2.github.getHeaders import getHeaders


def rename_branch_on_github(api_token, org_name, repo_name, branch, new_name):
    url = f'https://api.github.com/repos/{org_name}/{repo_name}/branches/{branch}/rename'
    print(url)
    data = {
        'new_name': new_name
    }

    # Make the request
    response = requests.post(url, json=data, headers=getHeaders(api_token))

    # Check the response from GitHub
    if response.status_code == 200:
        print(f'renamed branch {branch} on repo {repo_name} under organization {org_name}.')
    else:
        print('Failed to rename branch:', response.content)