from urllib.parse import urlparse
import requests


TRUSTED_DOMAINS = [
    "walmart.com",
    "amazon.com",
    "target.com",
    "bestbuy.com",
    "flipkart.com",
    "myntra.com",
    "ajio.com",
]

RETAIL_KEYWORDS = ["product", "item", "dp", "ip", "p", "buy", "shop"]


def is_valid_url_format(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ["http", "https"], result.netloc])
    except Exception:
        return False


def is_trusted_domain(url: str) -> bool:
    domain = urlparse(url).netloc.replace("www.", "").lower()
    return any(trusted in domain for trusted in TRUSTED_DOMAINS)


def contains_retail_keywords(url: str) -> bool:
    path = urlparse(url).path.lower()
    return any(keyword in path for keyword in RETAIL_KEYWORDS)


def check_url_status_code(url: str) -> (bool, str):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True, "URL is accessible"
        else:
            return False, f"Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, f"Request failed: {str(e)}"


def validate_retail_url(url: str) -> (bool, str):
    if not is_valid_url_format(url):
        return False, "Malformed URL"

    if not is_trusted_domain(url):
        return False, "Untrusted  retail domain"

    if not contains_retail_keywords(url):
        return False, "URL does not appear to be verified product page"

    status_ok, status_msg = check_url_status_code(url)
    if not status_ok:
        return False, status_msg

    return True, "Valid and trustworthy retail link"
