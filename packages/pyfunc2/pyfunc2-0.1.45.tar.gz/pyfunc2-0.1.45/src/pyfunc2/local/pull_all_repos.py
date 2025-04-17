import sys
import os

sys.path.append('../')
from local.git_folders_in_path import git_folders_in_path
from function.differenceElementsInArrays import differenceElementsInArrays


def pull_all_repos(local_path):
    # Git not exist, check if exist the remote repo on github
    git_local_repos = git_folders_in_path(local_path)
    # print(git_local_repos)
    not_expected_folders = [local_path + '/.idea']
    # remove from array existing elements from another array
    filtered_non_git_folders = differenceElementsInArrays(git_local_repos, not_expected_folders)
    print(filtered_non_git_folders)
    # not_existing_folder = differenceElementsInArrays(expected_folders, repos_in_orgs)
    for repo_folder in filtered_non_git_folders:
        # get last folder from path
        repo_name = repo_folder.split('/')[-1]
        print(repo_name)
        # create repository on github by api call

        # Navigate to the local path
        os.chdir(repo_folder)
        # Initialize the local repository and add the remote
        # os.system(f'git push --set-upstream origin main')
        os.system(f'git pull')
        os.system(f'git add .')
        os.system(f'git commit -m "Initial commit"')
        os.system(f'git push')