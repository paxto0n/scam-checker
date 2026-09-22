CONTACT_BANK_STEP = (
    "Contact your bank immediately through an official channel (the number on the "
    "back of your card, or their verified app/website) — never a number from the "
    "suspicious message itself."
)
PRESERVE_EVIDENCE_STEP = (
    "Preserve evidence: screenshots of the message, the URL, and any transaction "
    "alerts. Don't delete anything."
)
NEVER_ASK_STEP = (
    "Remember: a real bank will never ask for your PIN, OTP, or full card details "
    "over phone or text."
)

MONEY_SENT_STEPS = [
    "Give your bank the transaction reference number, date/time, and amount so "
    "they can attempt a reversal or open a dispute.",
    "If your bank does not resolve it, escalate to the CBN's Consumer Protection "
    "Department: cpd@cbn.gov.ng or contactcbn@cbn.gov.ng, or call +234 700 2255226.",
]

INFO_SHARED_STEPS = [
    "Call your bank immediately to freeze your account and deactivate mobile/USSD "
    "banking.",
    "Change passwords and PINs on anything tied to that phone number or email.",
    "Your BVN links to every Nigerian bank you have an account with, not just this "
    "one — consider alerting your other banks too.",
    "Watch for loan apps or accounts opened in your name without your knowledge.",
]

REPORTING_STEPS = [
    "Report the scam to the EFCC: efcc.gov.ng, info@efcc.gov.ng, or their Eagle "
    "Eye App.",
    "Or report to the Nigeria Police Force's National Cybercrime Centre: "
    "nccc.npf.gov.ng.",
]


def get_guidance(money_sent, info_shared):
    if not money_sent and not info_shared:
        return {
            "summary": (
                "Good news — since you haven't sent money or shared sensitive "
                "information, you're not currently at risk from this specific scam."
            ),
            "steps": [
                "Do not click any links or respond further.",
                "Block the sender or number.",
            ]
            + REPORTING_STEPS,
        }

    steps = [CONTACT_BANK_STEP]

    if money_sent:
        steps += MONEY_SENT_STEPS

    if info_shared:
        steps += INFO_SHARED_STEPS

    steps += [PRESERVE_EVIDENCE_STEP, NEVER_ASK_STEP]
    steps += REPORTING_STEPS

    return {
        "summary": "Act quickly — here's what to do right now.",
        "steps": steps,
    }
