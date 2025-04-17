
def getHeaders2(api_token):
    return {
        'Authorization': f'token {api_token}',
        'Accept': 'application/vnd.github.v3+json',
    }