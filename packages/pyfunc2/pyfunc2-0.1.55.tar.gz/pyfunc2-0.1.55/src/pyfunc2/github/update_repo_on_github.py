import requests
import sys
from pyfunc2.github.getHeaders import getHeaders

GITHUB_API_URL="https://api.github.com"
# moduletool
# Repository=1
# org_name=1
# f'Update a {Repository,org_name} on {org_name}'
# doc: https://developer.github.com/v3/repos/#create-a-repository
# Connect to {Github|api.github.com|GITHUB_API_URL} by {API token|api_token|GITHUB_API_TOKEN}
# Update a {Repository|repo_name|GITHUB_REPOSITORY_DEFAULT} on {GitHub Organization|org_name|GITHUB_ORGANIZATION_DEFAULT}
# Set a {Description|description|GITHUB_DESCRIPTION_DEFAULT}
# Set a {Domain|domain|GITHUB_DOMAIN_DEFAULT}
def update_repo_on_github(api_token, org_name, repo_name, description, domain):
    # Endpoint to create a repo within an organization
    url = f'{GITHUB_API_URL}/repos/{org_name}/{repo_name}/pages'
    print(url)
    # Data for the new repo
    data = {
        'name': repo_name,
        'description': description,
        'homepage': "http://" + repo_name + "." + domain,
        # 'html_url': "http://" + repo_name + "." + domain,
        # 'private': False  # Set to True if you want a private repository
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }

    # Make the request
    response = requests.patch(url, json=data, headers=getHeaders(api_token))

    # Check the response from GitHub
    if response.status_code == 201:
        print(f'updated repo {repo_name} under organization {org_name}.')
    else:
        print('Failed to update repo:', response.content)
