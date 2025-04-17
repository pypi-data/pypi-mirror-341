import os
import sys


from function.extract_domain_name_from_url import extract_domain_name_from_url
from pyfunc2.github.set_github_pages_domain import set_github_pages_domain
from pyfunc2.local.create_path import create_path
from pyfunc2.github.create_repo_on_not_git_repo_folder import create_repo_on_not_git_repo_folder
from pyfunc2.local.init_local_repo import init_local_repo
from pyfunc2.local.push_local_repo import push_local_repo
from pyfunc2.github.defaults import defaults
from pyfunc2.github.create_repo_on_github_and_local import create_repo_on_github_and_local


def new_organization_scenario(api_token, repos, org_name, repo_name, path_name):
    # print(repos)
    # path_name = "~/github"
    local_path = path_name + "/" + org_name
    create_path(local_path)

    domain, homepage, description = defaults('legacycode.info', 'identity','', org_name)

    print(org_name, domain, homepage, description)
    create_repo_on_github_and_local(api_token, org_name, repo_name, description, domain)

    #change_default_branch(api_token, org_name)


    root_path = os.path.dirname(os.path.realpath(__file__))
    # create_notexisting_folder(api_token, org_name, repos, local_path, domain, root_path)
    exit()
    create_repo_on_not_git_repo_folder(api_token, repos, org_name, local_path, domain)

    # push_all_repos(api_token, org_name, repos, local_path)
    # pull_all_repos(local_path)
    init_local_repo(local_path)
    push_local_repo(local_path)

    # configure_github_pages_branch(api_token, org_name, 'main')
    # configure_github_pages_domain(api_token, org_name, domain)
    # print(f'{org_name} / {repo_name} / {branch}..')
    set_github_pages_domain(api_token, org_name, domain)
    set_github_pages_domain(api_token, org_name, domain)