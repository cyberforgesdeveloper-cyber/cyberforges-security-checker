import dns.resolver
from urllib.parse import urlparse

def check_dns(domain: str):
    if "://" in domain:
        domain = urlparse(domain).hostname or domain

    result = {
        "check": "DNS Records",
        "status": "FAIL",
        "details": "",
        "score_weight": 15
    }

    try:
        # A record check karne ki koshish
        answers = dns.resolver.resolve(domain, 'A')
        if answers:
            result["status"] = "PASS"
            result["details"] = "DNS A records found successfully."
    except Exception as e:
        result["status"] = "FAIL"
        result["details"] = f"DNS resolution failed: {str(e)}"

    return result