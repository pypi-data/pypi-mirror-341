import sys


from function.extract_domain_name_from_url import extract_domain_name_from_url
from pyfunc2.local.clone_repo import clone_repo
from pyfunc2.local.create_path import create_path

# Clone a repository from a GitHub organization
def clone_repo_from_org(org_name, repo_name, local_path= "~/github"):
    local_path = local_path + "/" + org_name
    create_path(local_path)
    print(local_path, org_name, repo_name)
    clone_url = 'https://github.com/' + org_name + '/' + repo_name + '.git'
    clone_repo(clone_url, repo_name, local_path)