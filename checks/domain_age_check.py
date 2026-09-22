from datetime import datetime

import whois

AGE_THRESHOLD_DAYS = 30


def check_domain_age(domain):
    try:
        record = whois.whois(domain)
        creation_date = record.creation_date
    except Exception:
        return {"flagged": None, "reason": "Could not perform WHOIS lookup for this domain"}

    if isinstance(creation_date, list):
        creation_date = creation_date[0] if creation_date else None

    if creation_date is None:
        return {"flagged": None, "reason": "WHOIS record has no creation date"}

    creation_date = creation_date.replace(tzinfo=None)
    age_days = (datetime.now() - creation_date).days

    if age_days < AGE_THRESHOLD_DAYS:
        return {
            "flagged": True,
            "reason": f"Domain was registered only {age_days} day(s) ago",
        }

    return {"flagged": False, "reason": None}
