import dns.resolver
from urllib.parse import urlparse

def check_email_security(domain: str):
    if "://" in domain:
        domain = urlparse(domain).hostname or domain

    spf_status = "FAIL"
    dmarc_status = "FAIL"
    details = []

    # SPF Check (TXT record containing v=spf1)
    try:
        txt_records = dns.resolver.resolve(domain, 'TXT')
        for record in txt_records:
            text = str(record)
            if "v=spf1" in text:
                spf_status = "PASS"
                details.append("SPF record found.")
                break
        if spf_status == "FAIL":
            details.append("SPF record missing.")
    except Exception:
        details.append("Could not fetch SPF record.")

    # DMARC Check (_dmarc.domain TXT record)
    try:
        dmarc_domain = f"_dmarc.{domain}"
        dmarc_records = dns.resolver.resolve(dmarc_domain, 'TXT')
        for record in dmarc_records:
            text = str(record)
            if "v=DMARC1" in text:
                dmarc_status = "PASS"
                details.append("DMARC record found.")
                break
        if dmarc_status == "FAIL":
            details.append("DMARC record missing.")
    except Exception:
        details.append("DMARC record missing or not configured.")

    # Combined status for scoring
    overall_status = "PASS" if (spf_status == "PASS" and dmarc_status == "PASS") else ("WARNING" if (spf_status == "PASS" or dmarc_status == "PASS") else "FAIL")

    return {
        "check": "Email Security (SPF & DMARC)",
        "status": overall_status,
        "details": " | ".join(details),
        "score_weight": 25
    }