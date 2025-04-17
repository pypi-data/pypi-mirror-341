import sys
import requests


from pyfunc2.github.getHeaders import getHeaders
from pyfunc2.github.get_repos import get_repos

# Iterate over all pages of repositories
# Set the GitHub Pages domain, branch, path for each repo
def set_page_on_github_org_repos(api_token, org_name, branch='main', path='/', cname=''):
    for repo in get_repos(api_token, org_name).json():
        repo_name = repo['name']
        pages_url = repo['url'] + '/pages'

        # Get the current GitHub Pages configuration
        response = requests.get(pages_url, headers=getHeaders(api_token))

        if response.status_code == 404:
            print(f"GitHub Pages is not enabled for repo: {repo_name}, skipping...")
            continue
        
        if response.status_code != 200:
            print('Failed to retrieve repositories:', response.content)
            continue
        
        if response.status_code == 200:
            # Update the existing GitHub Pages configuration
            pages_data = {
                'source': {
                    'branch': branch, # Assuming the branch with your site content is named 'gh-pages'
                    'path': path # The root path where your site is located
                }
            }
            
            if cname: 
                pages_data['cname'] = cname  # Set your custom domain (must be configured in your DNS)'

            update_response = requests.patch(pages_url, json=pages_data, headers=getHeaders(api_token))

            if update_response.status_code == 200 or update_response.status_code == 201:
                print(f"Updated GitHub Pages source branch to '{branch}' for repo: {repo_name}")
            else:
                print(f"Failed to update GitHub Pages configuration for repo: {repo_name}")
