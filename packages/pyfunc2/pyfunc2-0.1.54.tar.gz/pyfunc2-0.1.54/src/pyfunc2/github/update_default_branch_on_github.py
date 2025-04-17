import sys
import requests


from pyfunc2.github.getHeaders import getHeaders


def update_default_branch_on_github(api_token, org_name, repo_name, branch):
    url = f'https://api.github.com/repos/{org_name}/{repo_name}'
    print(url)
    data = {
        'default_branch': branch
    }

    # Make the request
    response = requests.patch(url, json=data, headers=getHeaders(api_token))

    # Check the response from GitHub
    if response.status_code == 200:
        print(f'updated default branch {branch} on repo {repo_name} under organization {org_name}.')
    else:
        print('Failed to update default branch:', response.content)