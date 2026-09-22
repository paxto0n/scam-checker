SUSPICIOUS_TLDS = {
    "xyz", "top", "club", "online", "site", "work",
    "tk", "ml", "ga", "cf", "loan", "click",
}


def check_suspicious_tld(domain):
    tld = domain.rsplit(".", 1)[-1].lower()

    if tld in SUSPICIOUS_TLDS:
        return {
            "flagged": True,
            "reason": f"Domain uses '.{tld}', a TLD commonly abused in phishing sites",
        }

    return {
        "flagged": False,
        "reason": None,
    }
