import base64
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
VT_URL_TEMPLATE = "https://www.virustotal.com/api/v3/urls/{url_id}"


def check_blocklist(url):
    if not API_KEY:
        return {"flagged": None, "reason": "VirusTotal API key not configured"}

    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")

    try:
        response = requests.get(
            VT_URL_TEMPLATE.format(url_id=url_id),
            headers={"x-apikey": API_KEY},
            timeout=10,
        )
    except requests.RequestException:
        return {"flagged": None, "reason": "Could not reach VirusTotal API"}

    if response.status_code == 404:
        return {"flagged": None, "reason": "URL has not been scanned by VirusTotal before"}

    if response.status_code == 401:
        return {"flagged": None, "reason": "VirusTotal API key was rejected"}

    response.raise_for_status()

    stats = response.json()["data"]["attributes"]["last_analysis_stats"]
    bad_votes = stats.get("malicious", 0) + stats.get("suspicious", 0)

    if bad_votes > 0:
        return {
            "flagged": True,
            "reason": f"{bad_votes} security vendor(s) on VirusTotal flagged this URL",
        }

    return {"flagged": False, "reason": None}
