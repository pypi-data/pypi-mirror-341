import requests
import os
import sys


from pyfunc2.github.create_repo_on_github import create_repo_on_github

# Initialize the local project and add the remote GitHub
def create_repo_on_github_and_local(api_token, org_name, repo_folder, local_path, description, domain, default_branch ='main'):
    # Endpoint to create a repo within an organization
    response = create_repo_on_github(api_token, org_name, repo_folder, description, domain)
    # Check the response from GitHub
    if response.status_code == 201:
        print(f'Successfully created repo {repo_folder} under organization {org_name}.')
        repo_info = response.json()

        # Navigate to the local path
        os.chdir(local_path)

        print('create_repo_on_github_and_local default_branch: ' + default_branch)
        # Initialize the local repository and add the remote
        os.system('git init')
        os.system(f'git config --global init.defaultBranch {default_branch}')
        os.system(f'git remote add origin {repo_info["ssh_url"]}')
        os.system(f'git push --set-upstream origin {default_branch}')
        os.system('git pull')
        os.system('git remote set-head origin -a')
        os.system('git add .')
        os.system('git commit -m "Initial commit"')
        os.system('git push')

        print('Initialized local git repository and added remote origin.')

    else:
        print('Failed to create repo:', response.content)