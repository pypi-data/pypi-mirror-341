import sys
import requests

from pyfunc2.github.getHeaders import getHeaders

# Change the default branch for a
def change_default_branch(api_token, org_name, default_branch='main'):
    # Retrieve a list of all repositories within the organization
    repos_url = f'https://api.github.com/orgs/{org_name}/repos?per_page=100'
    repos_response = requests.get(repos_url, headers=getHeaders(api_token))

    if repos_response.status_code != 200:
        print(f"Failed to retrieve repositories: {repos_response.content}")
        return

    for repo in repos_response.json():
        repo_name = repo['name']
        repo_url = f"https://api.github.com/repos/{org_name}/{repo_name}"

        # Change the default branch
        data = {
            #"name": repo_name,
            #"description": repo_name,
            #"homepage": homepage,
            "default_branch": default_branch,
            #"private": False,
            #"has_issues": True,
            #"has_projects": True,
            #"has_wiki": True
        }
        patch_response = requests.patch(repo_url, headers=getHeaders(api_token), json=data)

        if patch_response.status_code in (200, 202):
            print(f"Default branch updated to 'main' for repo: {repo_name}")
        else:
            print(f"Failed to update default branch for repo: {repo_name}")
        print(f"Status code: {patch_response.status_code}, Response: {patch_response.json()}")