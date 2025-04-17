import sys
import os

sys.path.append('../')
from local.git_folders_in_path import git_folders_in_path

def init_local_repo(local_path):
    git_local_repos = git_folders_in_path(local_path)
    for repo_folder in git_local_repos:
        repo_name = repo_folder.split('/')[-1]
        org_name = repo_folder.split('/')[-2]

        ssh_url = f"git@github.com:{org_name}/{repo_name}.git"
        # print(repo_folder)
        # print(ssh_url)
        # Navigate to the local path
        os.chdir(repo_folder)
        # Initialize the local repository and add the remote
        # os.system(f'git init')
        # os.system('eval "$(ssh-agent -s)"')
        os.system(f'ssh-add ~/.ssh/github')
        # os.system(f'ssh -T git@github.com')
        os.system(f'ssh -i ~/.ssh/github -T git@github.com')
        os.system(f'git remote set-url origin {ssh_url}')
        os.system(f'git remote rm origin')
        os.system(f'git remote add origin {ssh_url}')
        os.system(f'git config advice.setUpstreamFailure false"')
        os.system(f'git branch -m master main')
        os.system(f'git fetch origin')
        os.system(f'git branch -u origin/main main')
        os.system(f'git remote set-head origin -a')
        os.system(f'git config --global push.default current')
        os.system(f'git branch --set-upstream-to=origin/main main')
        # os.system(f'git push --set-upstream origin main')
        os.system('git pull')