import socket
import ssl
from datetime import datetime
from urllib.parse import urlparse

import certifi


def check_https_cert(url):
    parsed = urlparse(url)

    if parsed.scheme != "https":
        return {"flagged": True, "reason": "Site does not use HTTPS"}

    host = parsed.hostname
    port = parsed.port or 443
    context = ssl.create_default_context(cafile=certifi.where())

    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
    except ssl.SSLCertVerificationError as e:
        return {"flagged": True, "reason": f"HTTPS certificate is invalid: {e.reason}"}
    except (socket.timeout, socket.gaierror, OSError):
        return {"flagged": None, "reason": "Could not connect to check HTTPS certificate"}

    expiry = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
    if expiry < datetime.utcnow():
        return {"flagged": True, "reason": "HTTPS certificate has expired"}

    return {"flagged": False, "reason": None}
