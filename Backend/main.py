from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from scanners.ssl_scanner import check_ssl
from scanners.headers_scanner import check_security_headers
from scanners.dns_scanner import check_dns
from scanners.email_security_scanner import check_email_security

# Database imports (ScanRecord, LeadRecord aur init_db)
from database import SessionLocal, init_db, ScanRecord, LeadRecord

app = FastAPI(title="CyberForges Security Checker API")

# Server start hote hi database tables create ho jayengi
init_db()

# Frontend se requests allow karne ke liye CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "CyberForges Security Checker Backend is Running!"}

# 1. Scan Endpoint
@app.post("/api/scan")
def scan_domain(data: dict):
    domain = data.get("domain", "")
    if not domain:
        return {"error": "Domain is required"}

    # Run all security scanners
    ssl_result = check_ssl(domain)
    headers_result = check_security_headers(domain)
    dns_result = check_dns(domain)
    email_result = check_email_security(domain)
    
    checks = [ssl_result, headers_result, dns_result, email_result]
    
    # Calculate score out of 100 based on weights
    total_weight = sum(c["score_weight"] for c in checks)
    earned_score = 0
    
    for check in checks:
        if check["status"] == "PASS":
            earned_score += check["score_weight"]
        elif check["status"] == "WARNING":
            earned_score += int(check["score_weight"] / 2)

    final_score = int((earned_score / total_weight) * 100)

    # Database mein Scan save karna
    try:
        db = SessionLocal()
        db_scan = ScanRecord(domain=domain, total_score=final_score)
        db.add(db_scan)
        db.commit()
        db.close()
    except Exception as e:
        print(f"Database save error: {e}")

    return {
        "domain": domain,
        "total_score": final_score,
        "results": checks
    }

# 2. Lead Generation Endpoint
@app.post("/api/lead")
def save_lead(data: dict):
    name = data.get("name", "")
    company = data.get("company", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    domain = data.get("domain", "")

    if not email or not domain:
        return {"error": "Email and Domain are required"}

    try:
        db = SessionLocal()
        new_lead = LeadRecord(
            name=name,
            company=company,
            email=email,
            phone=phone,
            domain=domain
        )
        db.add(new_lead)
        db.commit()
        db.close()
        return {"status": "success", "message": "Lead saved successfully!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 3. Admin Panel Data Endpoint
@app.get("/api/admin/leads")
def get_leads():
    try:
        db = SessionLocal()
        leads = db.query(LeadRecord).all()
        scans = db.query(ScanRecord).all()
        db.close()
        
        return {
            "status": "success",
            "leads": [{"id": l.id, "name": l.name, "company": l.company, "email": l.email, "phone": l.phone, "domain": l.domain, "created_at": str(l.created_at)} for l in leads],
            "scans": [{"id": s.id, "domain": s.domain, "total_score": s.total_score, "created_at": str(s.created_at)} for s in scans]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 4. PDF Report Generation Endpoint
@app.post("/api/download-pdf")
def generate_pdf(data: dict):
    domain = data.get("domain", "example.com")
    score = data.get("score", 0)
    
    pdf_filename = f"CyberForges_Security_Report_{domain.replace('.', '_')}.pdf"
    pdf_path = os.path.join(os.getcwd(), pdf_filename)
    
    try:
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Header Branding
        c.setFillColorRGB(0.02, 0.08, 0.16)
        c.rect(0, height - 100, width, 100, fill=1, stroke=0)
        
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(50, height - 50, "CyberForges Security Report")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 70, "Professional Website Vulnerability & Compliance Assessment")

        # Report Content
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 150, f"Target Domain: {domain}")
        
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 180, f"Overall Security Score: {score} / 100")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 210, "This document certifies the automated security check performed by CyberForges.")
        
        # Footer
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawString(50, 50, "Generated securely by CyberForges Security Engine | Contact: support@cyberforges.com")

        c.save()

        return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_filename)
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)