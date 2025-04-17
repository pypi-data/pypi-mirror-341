# Extract the subdomain name from a URL
def get_subdomain_from_url(url):
    return url.split('/')[0]