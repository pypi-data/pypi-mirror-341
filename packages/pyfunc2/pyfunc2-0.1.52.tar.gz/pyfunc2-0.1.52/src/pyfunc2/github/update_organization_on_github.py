import sys
import requests


from pyfunc2.github.getHeaders import getHeaders


def update_organization_on_github(api_token, org_name, data, url = 'https://api.github.com/user/orgs'):

    print(url)
    print(data)
    # Make the request
    response = requests.patch(url, json=data, headers=getHeaders(api_token))
    #response = requests.patch(url, json=data, headers=getHeaders(api_token))

    # Check the response from GitHub
    if response.status_code == 201:
        print(f'created organization {org_name}.')
    else:
        print('Failed to create organization:', response.content)
