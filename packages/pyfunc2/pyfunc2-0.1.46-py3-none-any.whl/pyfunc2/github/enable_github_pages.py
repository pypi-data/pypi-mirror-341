import sys
import requests


from pyfunc2.github.getHeaders import getHeaders




def enable_github_pages(api_token, org_name, repo_name, branch='main', domain=None, path='/'):
    url = f'https://api.github.com/repos/{org_name}/{repo_name}/pages'
    data = {
        'source': {
            'branch': branch,
            'path': path
        },
        'cname': domain
    }
    response = requests.post(url, json=data, headers=getHeaders(api_token))

    if response.status_code == 201:
        print(f"GitHub Pages enabled for {repo_name} with branch '{branch}'.")
        if domain:
            print("Custom domain set to:", domain)
    else:
        print("Failed to enable GitHub Pages. Status code:", response.status_code)
        print("Response:", response.json())