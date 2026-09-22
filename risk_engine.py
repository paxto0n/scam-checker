from urllib.parse import urlparse

from checks.blocklist_check import check_blocklist
from checks.domain_age_check import check_domain_age
from checks.https_check import check_https_cert
from checks.lookalike_check import check_lookalike_domain
from checks.tld_check import check_suspicious_tld
from checks.url_pattern_check import check_url_pattern

CHECK_WEIGHTS = {
    "blocklist": 30,
    "lookalike_domain": 25,
    "domain_age": 15,
    "https_cert": 10,
    "url_pattern": 10,
    "suspicious_tld": 10,
}

HIGH_RISK_THRESHOLD = 60
SUSPICIOUS_THRESHOLD = 20


def normalize_url(raw_input):
    raw_input = raw_input.strip()

    if not raw_input.startswith(("http://", "https://")):
        raw_input = "https://" + raw_input

    return raw_input


def calculate_risk(raw_input):
    url = normalize_url(raw_input)
    domain = urlparse(url).hostname or ""

    results = {
        "suspicious_tld": check_suspicious_tld(domain),
        "lookalike_domain": check_lookalike_domain(domain),
        "url_pattern": check_url_pattern(url),
        "domain_age": check_domain_age(domain),
        "https_cert": check_https_cert(url),
        "blocklist": check_blocklist(url),
    }

    score = 0
    red_flags = []
    notes = []

    for name, result in results.items():
        if result["flagged"] is True:
            score += CHECK_WEIGHTS[name]
            red_flags.append(result["reason"])
        elif result["flagged"] is None:
            notes.append(result["reason"])

    if score >= HIGH_RISK_THRESHOLD:
        level = "high"
        verdict = "High Risk - Likely Scam"
    elif score >= SUSPICIOUS_THRESHOLD:
        level = "suspicious"
        verdict = "Suspicious - Proceed with Caution"
    else:
        level = "low"
        verdict = "Low Risk - Likely Legitimate"

    return {
        "url": url,
        "score": score,
        "level": level,
        "verdict": verdict,
        "red_flags": red_flags,
        "notes": notes,
    }
