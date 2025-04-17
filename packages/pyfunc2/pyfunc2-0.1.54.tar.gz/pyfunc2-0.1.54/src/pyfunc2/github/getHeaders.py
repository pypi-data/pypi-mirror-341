def getHeaders(api_token):
    return {
        'Authorization': f'Bearer {api_token}',
        'Accept': 'application/vnd.github.v+json',
        'X-GitHub-Api-Version': '2022-11-28',
    }