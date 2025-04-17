import sys
sys.path.append('../')
from .folder_exist import folder_exist

def clone_repos_from_org(org_name: object, repos: object, path_folder: object) -> object:
    if repos:
        for repo in repos:
            if 'clone_url' in repo:
                if folder_exist(path_folder + "/" + repo['name']):
                    print(f"Exist: {org_name}/{repo['name']}")
                    continue
                if (repo['fork'] == False):
                    print(f"Clone: {org_name}/{repo['name']}")
                    # clone_repo(repo['clone_url'], repo['name'], path_folder)
                else:
                    print(f"Fork: {org_name}/{repo['name']}")
                    # if(remove_fork) remove
    else:
        print(f"Failed to fetch repositories for organization: {org_name}")