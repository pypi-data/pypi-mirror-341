import sys
import requests


from pyfunc2.github.get_repos import get_repos
from pyfunc2.github.getHeaders import getHeaders

# List all repositories in the organization
# Set your custom domain (must be configured in your DNS) for each repository in Organisation
def set_domain_on_github_org_pages(api_token, org_name, domain, headers):
    if not headers:
        headers = getHeaders(api_token)
    # List all repositories in the organization
    repos_url = f'https://api.github.com/orgs/{org_name}/repos'
    response = requests.get(repos_url, headers=headers)

    if response.status_code != 200:
        print('Failed to retrieve repositories:', response.content)
        return

    for repo in get_repos(api_token, org_name).json():
        # If GitHub Pages API allows enabling Pages, the code would be similar to this:
        pages_url = repo['url'] + '/pages'
        pages_data = {
            'cname': domain,  # Set your custom domain (must be configured in your DNS)
            # Any additional settings...
        }
        pages_response = requests.post(pages_url, json=pages_data, headers=headers)

        if pages_response.status_code == 200 or pages_response.status_code == 201:
            print(f"Configured GitHub Pages for repo: {repo['name']}")
        elif pages_response.status_code == 409:
            print(f"GitHub Pages is already set up for repo: {repo['name']}")
        else:
            print(f"Failed to configure GitHub Pages for repo: {repo['name']}")