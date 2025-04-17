from urllib.parse import urlparse
# Extract the domain name from a URL
def extract_domain_name_from_url(url):
    domain_name = None
    if (url):
        # Parse the URL to get the netloc (network location part)
        netloc = urlparse(url).netloc

        # Split the netloc into parts by '.'
        netloc_parts = netloc.split('.')

        # Extract the last two parts for domain and TLD
        # This assumes a standard TLD; does not account for country-code TLDs like '.co.uk'
        domain_name = '.'.join(netloc_parts[-2:])

    return domain_name