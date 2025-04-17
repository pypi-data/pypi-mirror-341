import sys
import requests


from pyfunc2.github.getHeaders import getHeaders

# Delete branch remote branch on github
def delete_branch_on_github(api_token, org_name, repo_name, branch):
    url = f'https://api.github.com/repos/{org_name}/{repo_name}/git/refs/heads/{branch}'
    print(url)
    response = requests.delete(url, headers=getHeaders(api_token))

    # Check the response from GitHub
    if response.status_code == 204:
        print(f'deleted branch {branch} on repo {repo_name} under organization {org_name}.')
    else:
        print('Failed to delete branch:', response.content)

        branch = 'master'
        delete_branch_on_github(api_token, org_name, repo_name, branch)