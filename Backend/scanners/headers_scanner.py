import requests

def check_security_headers(domain: str):
    if not domain.startswith("http"):
        target_url = f"https://{domain}"
    else:
        target_url = domain

    result = {
        "check": "Security Headers",
        "status": "FAIL",
        "details": "",
        "score_weight": 25
    }

    try:
        response = requests.get(target_url, timeout=5, allow_redirects=True)
        headers = response.headers
        
        missing_headers = []
        recommended_headers = ['Strict-Transport-Security', 'X-Frame-Options', 'X-Content-Type-Options']
        
        for h in recommended_headers:
            if h not in headers:
                missing_headers.append(h)

        if len(missing_headers) == 0:
            result["status"] = "PASS"
            result["details"] = "All core security headers are present."
        else:
            result["status"] = "WARNING"
            result["details"] = f"Missing recommended headers: {', '.join(missing_headers)}"
            
    except Exception as e:
        result["status"] = "FAIL"
        result["details"] = f"Could not fetch headers: {str(e)}"

    return result