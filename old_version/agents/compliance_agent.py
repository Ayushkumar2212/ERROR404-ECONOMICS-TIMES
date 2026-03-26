"""
SafeScript AI Biller - Compliance Agent
Handles auto-approval for high-confidence cases and human escalation for low-confidence cases.
"""

from datetime import datetime


def compliance_agent(state: dict) -> dict:
    """
    Agent 3a: Compliance Agent (Auto-Approval Path)
    Triggered when confidence_score >= 85%.
    - Simulates ICD-10 database validation
    - Simulates insurance rules check
    - Simulates claim completeness check
    - Auto-approves and submits the claim
    """
    print("🛡️ [Compliance Agent] Running compliance checks...")

    audit_log = state.get("audit_log", [])
    medical_codes = state.get("medical_codes", [])
    confidence_score = state.get("confidence_score", 0)

    # Simulate validation checks
    checks = [
        {"check": "ICD-10 Database Validation", "result": "PASS", "details": f"All {len(medical_codes)} code(s) found in ICD-10 database"},
        {"check": "Insurance Rules Compliance", "result": "PASS", "details": "Codes meet payer-specific guidelines"},
        {"check": "Claim Completeness", "result": "PASS", "details": "All required fields present"},
        {"check": "Duplicate Claim Check", "result": "PASS", "details": "No duplicate claims detected"},
    ]

    for check in checks:
        print(f"  ✅ {check['check']}: {check['result']} — {check['details']}")

    # Audit trail
    audit_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": "Compliance Agent",
        "action": "Auto-Approval & Submission",
        "status": "success",
        "details": {
            "confidence_score": confidence_score,
            "validation_checks": checks,
            "final_status": "Auto-Approved & Submitted"
        }
    }
    audit_log.append(audit_entry)

    print(f"🛡️ [Compliance Agent] Claim AUTO-APPROVED & SUBMITTED.\n")

    return {
        "final_status": "Auto-Approved & Submitted",
        "audit_log": audit_log
    }


def human_escalation(state: dict) -> dict:
    """
    Agent 3b: Human Escalation Path
    Triggered when confidence_score < 85%.
    - Logs escalation reasons
    - Simulates notifications (Slack, dashboard)
    - Sets status to pending human review
    """
    print("🛡️ [Human Escalation] Low confidence detected — escalating to human reviewer...")

    audit_log = state.get("audit_log", [])
    confidence_score = state.get("confidence_score", 0)
    reasoning = state.get("reasoning", "")
    medical_codes = state.get("medical_codes", [])

    # Escalation reasons
    escalation_reasons = []
    if confidence_score < 60:
        escalation_reasons.append("Very low confidence score (<60%)")
    if confidence_score < 85:
        escalation_reasons.append(f"Below auto-approval threshold (score: {confidence_score}%)")
    if not medical_codes:
        escalation_reasons.append("No valid ICD-10 codes assigned")

    for reason in escalation_reasons:
        print(f"  ⚠️ Escalation reason: {reason}")

    # Simulate notifications
    notifications = [
        {"channel": "Slack", "status": "Sent", "message": f"🔔 Case requires review — Confidence: {confidence_score}%"},
        {"channel": "Dashboard", "status": "Flagged", "message": "Case added to human review queue"},
        {"channel": "Email", "status": "Queued", "message": "Notification sent to assigned reviewer"},
    ]

    for notif in notifications:
        print(f"  📨 {notif['channel']}: {notif['status']} — {notif['message']}")

    # Audit trail
    audit_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": "Human Escalation",
        "action": "Escalated to Human Review",
        "status": "warning",
        "details": {
            "confidence_score": confidence_score,
            "escalation_reasons": escalation_reasons,
            "notifications": notifications,
            "final_status": "Pending Human Review"
        }
    }
    audit_log.append(audit_entry)

    print(f"🛡️ [Human Escalation] Case ESCALATED. Pending human review.\n")

    return {
        "final_status": "Pending Human Review",
        "audit_log": audit_log
    }
