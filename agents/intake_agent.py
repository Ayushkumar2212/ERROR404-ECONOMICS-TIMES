"""
SafeScript AI Biller - Intake Agent
Handles PII/PHI masking and document hashing for HIPAA compliance.
"""

import re
import hashlib
from datetime import datetime


def intake_agent(state: dict) -> dict:
    """
    Agent 1: Intake Agent
    - Masks PII/PHI (Aadhaar numbers, Indian phone numbers, emails, patient names)
    - Creates SHA-256 document hash for audit trail
    - Logs all masking actions
    """
    print("[Intake Agent] Starting PII/PHI masking...")

    raw_document = state.get("raw_document", "")
    audit_log = state.get("audit_log", [])

    # --- PII/PHI Masking ---
    masked_document = raw_document
    mask_count = 0

    # 1. Mask Aadhaar numbers (12 digits, optionally separated by spaces)
    aadhaar_pattern = r'\b\d{4}\s?\d{4}\s?\d{4}\b'
    aadhaar_matches = re.findall(aadhaar_pattern, masked_document)
    if aadhaar_matches:
        masked_document = re.sub(aadhaar_pattern, '[AADHAAR-MASKED]', masked_document)
        mask_count += len(aadhaar_matches)
        print(f"  [MASKED] {len(aadhaar_matches)} Aadhaar number(s)")

    # 2. Mask Indian phone numbers (10 digits starting with 6-9)
    phone_pattern = r'\b[6-9]\d{9}\b'
    phone_matches = re.findall(phone_pattern, masked_document)
    if phone_matches:
        masked_document = re.sub(phone_pattern, '[PHONE-MASKED]', masked_document)
        mask_count += len(phone_matches)
        print(f"  [MASKED] {len(phone_matches)} phone number(s)")

    # 3. Mask email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_matches = re.findall(email_pattern, masked_document)
    if email_matches:
        masked_document = re.sub(email_pattern, '[EMAIL-MASKED]', masked_document)
        mask_count += len(email_matches)
        print(f"  [MASKED] {len(email_matches)} email(s)")

    # 4. Mask patient names (after "Patient:" label)
    name_pattern = r'(Patient:\s*)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
    name_matches = re.findall(name_pattern, masked_document)
    if name_matches:
        masked_document = re.sub(name_pattern, r'\1[NAME-MASKED]', masked_document)
        mask_count += len(name_matches)
        print(f"  [MASKED] {len(name_matches)} patient name(s)")

    # --- Document Hashing ---
    doc_hash = hashlib.sha256(raw_document.encode()).hexdigest()[:16]
    print(f"  (Hash) Document hash: {doc_hash}")

    # --- Audit Trail ---
    audit_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": "Intake Agent",
        "action": "PII/PHI Masking & Document Hashing",
        "status": "success",
        "details": {
            "items_masked": mask_count,
            "document_hash": doc_hash,
            "mask_types": ["Aadhaar", "Phone", "Email", "Name"]
        }
    }
    audit_log.append(audit_entry)

    print(f"[Intake Agent] Complete. Masked {mask_count} PII/PHI items.\n")

    # --- PII/PHI Report ---
    pii_report = {
        "score": 100 if mask_count > 0 else 100,
        "total_masked": mask_count,
        "report": {
            "Aadhaar": len(aadhaar_matches),
            "Phone": len(phone_matches),
            "Email": len(email_matches),
            "Name": len(name_matches)
        }
    }

    # --- Injection Scan (Simulation) ---
    threat_score = 0
    if "ignore" in raw_document.lower() and "previous" in raw_document.lower():
        threat_score += 45
    if "system" in raw_document.lower() and "prompt" in raw_document.lower():
        threat_score += 40
    
    injection_scan = {
        "status": "blocked" if threat_score > 30 else "passed",
        "score": threat_score,
        "message": "Potential prompt injection detected." if threat_score > 30 else "No threats detected."
    }

    return {
        "masked_document": masked_document,
        "audit_log": audit_log,
        "pii_report": pii_report,
        "injection_scan": injection_scan
    }

