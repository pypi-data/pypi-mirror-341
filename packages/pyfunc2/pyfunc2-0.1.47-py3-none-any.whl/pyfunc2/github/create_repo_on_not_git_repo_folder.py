import sys


from pyfunc2.local.non_git_folders_in_path import non_git_folders_in_path
from function.differenceElementsInArrays import differenceElementsInArrays
from pyfunc2.local.load_file import load_file
from function.flat_array import flat_array
from pyfunc2.github.create_repo_on_github_and_local import create_repo_on_github_and_local

def create_repo_on_not_git_repo_folder(api_token, repos, org_name, local_path, domain):
    # Git not exist, check if exist the remote repo on github
    remote_repos = flat_array(repos, 'name')
    print(remote_repos)
    print(local_path)
    non_git_local_repos = non_git_folders_in_path(local_path)
    # print('non_git_local_repos', non_git_local_repos)
    not_expected_folders = [local_path + '/.idea']
    # print('not_expected_folders', not_expected_folders)
    # remove from array existing elements from another array
    filtered_non_git_folders = differenceElementsInArrays(non_git_local_repos, not_expected_folders)
    print(filtered_non_git_folders)
    for repo_folder in filtered_non_git_folders:
        # get last folder from path
        repo_name = repo_folder.split('/')[-1]
        print(repo_name)
        # create repository on github by api call
        description = load_file(repo_folder + "/description.txt")
        create_repo_on_github_and_local(api_token, org_name, repo_name, repo_folder, description, domain)