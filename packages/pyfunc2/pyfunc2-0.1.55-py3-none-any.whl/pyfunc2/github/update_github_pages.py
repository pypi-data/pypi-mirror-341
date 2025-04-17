import sys
import requests


from pyfunc2.github.getHeaders2 import getHeaders2


def update_github_pages(api_token, org_name, repo_name, branch='main', domain=None, path='/'):
    url = f'https://api.github.com/repos/{org_name}/{repo_name}/pages'
    data = {
        "cname": domain,
        "source": {
            "branch": branch,
            "path": path
        }
        # 'https_enforced': False,
        # 'protected_domain_state': 'verified'
    }
    print('data', data)
    response = requests.put(url, json=data, headers=getHeaders2(api_token))

    if response.status_code in (200, 201):
        print(f"GitHub Pages configuration updated for repository: {repo_name}")
    else:
        print(f"Failed to update GitHub Pages configuration. Status code: {response.status_code}")