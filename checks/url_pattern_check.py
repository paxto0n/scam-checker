import re
from urllib.parse import urlparse

IP_HOST_PATTERN = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")


def check_url_pattern(url):
    parsed = urlparse(url)
    host = parsed.hostname or ""

    if IP_HOST_PATTERN.match(host):
        return {
            "flagged": True,
            "reason": "URL uses a raw IP address instead of a domain name",
        }

    if "@" in parsed.netloc:
        return {
            "flagged": True,
            "reason": "URL contains '@', which can hide the real destination domain",
        }

    if host.count("-") >= 3:
        return {
            "flagged": True,
            "reason": "Domain contains an unusually high number of hyphens",
        }

    if host.count(".") >= 4:
        return {
            "flagged": True,
            "reason": "URL has an unusually deep subdomain structure",
        }

    return {
        "flagged": False,
        "reason": None,
    }
