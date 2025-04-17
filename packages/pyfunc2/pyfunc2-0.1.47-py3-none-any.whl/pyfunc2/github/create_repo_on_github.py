import sys
import requests


from pyfunc2.github.getHeaders import getHeaders

# Create a repo on GitHub
def create_repo_on_github(api_token, org_name, repo_folder, description="This is your first repository", domain = 'legacycode.info'):
    url = f'https://api.github.com/orgs/{org_name}/repos'
    print(url)
    data = {
        'name': repo_folder,
        "description": description,
        "homepage": "https://" + domain,
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }

    # Make the request
    response = requests.post(url, json=data, headers=getHeaders(api_token))

    # Check the response from GitHub
    if response.status_code == 201:
        print(f'created repo {repo_folder} under organization {org_name}.')
    else:
        print('Failed to create repo:', response.content)

    return response