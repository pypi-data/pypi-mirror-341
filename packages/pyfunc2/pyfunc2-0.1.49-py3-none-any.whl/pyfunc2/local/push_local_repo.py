import sys
import os

sys.path.append('../')
from local.git_folders_in_path import git_folders_in_path


def push_local_repo(local_path):
    git_local_repos = git_folders_in_path(local_path)
    for repo_folder in git_local_repos:
        repo_name = repo_folder.split('/')[-1]
        org_name = repo_folder.split('/')[-2]

        ssh_url = f"git@github.com:{org_name}/{repo_name}.git"
        print(repo_folder)
        print(ssh_url)
        # Navigate to the local path
        os.chdir(repo_folder)
        # Initialize the local repository and add the remote
        os.system(f'git pull origin main')
        os.system(f'git add .')
        os.system(f'git commit -m "Initial commit"')
        os.system(f'git push')