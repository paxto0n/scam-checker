KNOWN_BRANDS = {
    "gtbank": "gtbank.com",
    "zenithbank": "zenithbank.com",
    "accessbank": "accessbankplc.com",
    "uba": "ubagroup.com",
    "fidelitybank": "fidelitybank.ng",
    "firstbank": "firstbanknigeria.com",
    "fcmb": "fcmb.com",
    "unionbank": "unionbankng.com",
    "wemabank": "wemabank.com",
    "fairmoney": "fairmoney.io",
    "getcarbon": "getcarbon.co",
    "branch": "branch.co",
    "renmoney": "renmoney.com",
}


def check_lookalike_domain(domain):
    domain = domain.lower()
    if domain.startswith("www."):
        domain = domain[4:]

    for brand, official in KNOWN_BRANDS.items():
        if brand not in domain:
            continue

        is_official = domain == official or domain.endswith("." + official)
        if is_official:
            continue

        return {
            "flagged": True,
            "reason": f"Domain contains '{brand}' but is not {official}",
        }

    return {
        "flagged": False,
        "reason": None,
    }
