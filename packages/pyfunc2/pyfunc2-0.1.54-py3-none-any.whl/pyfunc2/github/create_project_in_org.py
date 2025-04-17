import sys


from function.extract_domain_name_from_url import extract_domain_name_from_url
from pyfunc2.local.clone_repo import clone_repo
from pyfunc2.local.create_path import create_path
from pyfunc2.github.defaults import defaults


# TODO: not used?
# Create project on Github Organisation=@org_name in
def create_project_in_org(org_name, repo_name, path_name):
    # print(repos)
    # path_name = "~/github"
    local_path = path_name + "/" + org_name
    create_path(local_path)

    # TODO: fix
    domain, homepage, description = defaults(org_name, path_name)


    print(org_name, domain, homepage, description)
    #create_repo_on_github_and_local(api_token, org_name, repo_name, description, domain)
    #rename_branch_on_github(api_token, org_name, repo_name, 'master', 'main')
    clone_url = 'https://github.com/' + org_name + '/' + repo_name + '.git'
    clone_repo(clone_url, repo_name, local_path)