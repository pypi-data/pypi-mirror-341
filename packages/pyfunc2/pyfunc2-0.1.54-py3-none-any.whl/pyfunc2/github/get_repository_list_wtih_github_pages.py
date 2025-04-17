import sys
import requests


from pyfunc2.github.getHeaders import getHeaders


def get_repository_list_wtih_github_pages(api_token, org_name, repo_name):
    url = f'https://api.github.com/repos/{org_name}/{repo_name}/pages'
    response = requests.get(url, headers=getHeaders(api_token))

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch GitHub Pages. Status code:", response.status_code)
        print("Response:", response.json())