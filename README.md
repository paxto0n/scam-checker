# Scam Checker

A Flask tool that detects phishing/scam links impersonating Nigerian banks and loan apps — built as a final-year cybersecurity project MVP.

Paste in a URL from a suspicious "bank alert" or "loan approved" message and get back a risk score, a plain-English verdict, and (if it's flagged) a step-by-step guide for what to do next.

## How it works

The URL is run through six independent, weighted checks:

| Check | Type | Weight | What it detects |
| --- | --- | --- | --- |
| Blocklist (VirusTotal) | Online | 30 | URL previously flagged malicious/suspicious by security vendors |
| Lookalike domain | Offline | 25 | A known bank/loan-app brand name embedded in a domain that isn't the real one |
| Domain age (WHOIS) | Online | 15 | Domain registered under 30 days ago |
| HTTPS/certificate | Online | 10 | No HTTPS, or an invalid/expired/mismatched certificate |
| URL pattern | Offline | 10 | Raw IP address host, `@` symbol, excessive hyphens or subdomain depth |
| Suspicious TLD | Offline | 10 | Domain uses a TLD common in phishing (`.xyz`, `.tk`, `.top`, etc.) |

Points from every check that fires are summed into a 0–100 score:

- **≥ 60** → High Risk – Likely Scam
- **20–59** → Suspicious – Proceed with Caution
- **< 20** → Low Risk – Likely Legitimate

Flagged results also show a short triage flow asking whether the user already sent money or shared their BVN/OTP/PIN, and give situation-specific next steps (freezing accounts, contacting the CBN, reporting to the EFCC, etc.).

## Setup

```bash
git clone https://github.com/paxto0n/scam-checker.git
cd scam-checker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root with a [VirusTotal](https://www.virustotal.com/) API key:

```
VIRUSTOTAL_API_KEY=your_key_here
```

## Running

```bash
python app.py
```

Then open `http://127.0.0.1:5000` in a browser.

## Validation

```bash
python tests/run_validation.py
```

Runs the 60-example test set (`tests/test_set.csv`) against the risk engine and reports accuracy/precision/recall. Note: VirusTotal's free tier is rate-limited to 4 requests/minute, so a full run takes 15–20 minutes.

## Project structure

```
scam-checker/
├── app.py              # Flask routes: / (check form) and /guidance (triage)
├── risk_engine.py       # normalize_url(), calculate_risk() — orchestrates all checks
├── guidance.py           # get_guidance() — victim triage step content
├── checks/
│   ├── tld_check.py
│   ├── lookalike_check.py
│   ├── url_pattern_check.py
│   ├── domain_age_check.py
│   ├── https_check.py
│   └── blocklist_check.py
├── templates/            # index.html, guidance.html
├── static/style.css
└── tests/                # test_set.csv, run_validation.py
```

## Limitations

- The validation test set was built around the same attack patterns the checks are designed to catch, and thresholds were tuned on it — the 100% score shows correct implementation, not real-world generalization.
- The brand list covers 9 banks and 4 loan apps, individually verified rather than sourced from an official registry.
- The blocklist check only looks up existing VirusTotal reports; a brand-new, never-submitted scam URL returns "unknown," not "clean."

Full write-up with architecture details, validation methodology, and future work: [Scam Checker Project Write-Up](https://claude.ai/artifact/1tzgEKHNCGPHCoSCX2b6Xy) *(private by default — adjust sharing if you want this link to work for others)*
