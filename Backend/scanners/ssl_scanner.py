import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime

def check_ssl(domain: str):
    # Domain format clean karna
    if not domain.startswith("http"):
        domain_url = f"https://{domain}"
    else:
        domain_url = domain
        
    parsed_url = urlparse(domain_url)
    hostname = parsed_url.hostname or domain

    result = {
        "check": "SSL / HTTPS Certificate",
        "status": "FAIL",
        "details": "",
        "score_weight": 25
    }

    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # Expiration date check
                not_after = cert.get('notAfter')
                if not_after:
                    expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                    if expiry_date > datetime.utcnow():
                        result["status"] = "PASS"
                        result["details"] = f"SSL Certificate is valid and expires on {not_after}"
                    else:
                        result["status"] = "FAIL"
                        result["details"] = "SSL Certificate has expired."
                else:
                    result["status"] = "PASS"
                    result["details"] = "HTTPS is active and secure."
    except Exception as e:
        result["status"] = "FAIL"
        result["details"] = f"SSL/HTTPS connection failed: {str(e)}"

    return result