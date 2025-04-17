import os
import sys


from function.extract_domain_name_from_url import extract_domain_name_from_url
from pyfunc2.github.change_default_branch import change_default_branch


def defaults(domain='', repo_name='identity', homepage='', org_name=''):
    if not domain:
        domain = org_name + '.com'

    # homepage = get_param_from_repo(repos, 'homepage')
    # print(homepage)
    if homepage:
        # set_github_pages_domain(api_token, org_name, domain)
        # homepage = f'{org_name}.github.io/{repo_folder}'
        domain = extract_domain_name_from_url(homepage)

    if not homepage:
        homepage = 'http://www.' + domain

    description = repo_name + ', ' + homepage

    return domain, homepage, description
