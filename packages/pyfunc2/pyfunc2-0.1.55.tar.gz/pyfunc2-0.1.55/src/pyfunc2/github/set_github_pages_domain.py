import sys
import requests


from pyfunc2.github.get_repository_list_wtih_github_pages import get_repository_list_wtih_github_pages
from pyfunc2.github.getHeaders import getHeaders
from pyfunc2.github.enable_github_pages import enable_github_pages
from pyfunc2.github.update_github_pages import update_github_pages


def set_github_pages_domain(api_token, org_name, domain, default_branch):
    url = f'https://api.github.com/orgs/{org_name}/repos'
    # Iterate over all pages of repositories
    while url:
        response = requests.get(url, headers=getHeaders(api_token))
        print(url)

        if response.status_code != 200:
            print('Failed to retrieve repositories:', response.content)
            return

        # Loop over each repo and set the GitHub Pages domain
        for repo in response.json():
            if repo['name'] == '.github':
                #subdomain = "www" + "." + domain
                continue
            else:
                subdomain = repo['name'] + "." + domain

            print("==========", repo)
            if repo['name']:
                print("0", repo['name'])

                result = get_repository_list_wtih_github_pages(api_token, org_name, repo['name'])
                print("1", result)
                # repo['default_branch']
                branch = default_branch
                #branch = 'master'

                if not result:
                    result = enable_github_pages(api_token, org_name, repo['name'], branch, subdomain)

                print('2', result)

                if result and not result['cname']:
                    result = update_github_pages(api_token, org_name, repo['name'], branch, subdomain)

                print('3', result)

                # if (result['status'] == 'built'):

                # update_github_pages(api_token, org_name, repo['name'], repo['default_branch'], subdomain)

        # Fetch the next page of repositories, if available
        url = response.links.get('next', {}).get('url', None)