import sys
import requests
import json


from pyfunc2.github.getHeaders import getHeaders
from pyfunc2.github.get_owner_json import get_owner_json


def create_organization_on_github(api_token, org_name, file_path="owner/name.json", url = "https://api.github.com/user/orgs"):
    data = get_owner_json(file_path)
    if not org_name:
        print("Error: org_name cannot be empty.")
        return None

    # Update the 'name' value with the provided org_name
    data['name'] = org_name
    print(data)
    if data:
        print(url)

        # Make the request
        response = requests.patch(url, json=data, headers=getHeaders(api_token))

        # Check the response from GitHub
        if response.status_code == 201:
            print(f'created organization {org_name}.')
        else:
            print('Failed to create organization:', response.content)
