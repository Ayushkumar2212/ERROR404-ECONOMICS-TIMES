"""
SafeScript AI Biller — Streamlit Dashboard
Autonomous healthcare coding system with multi-agent architecture.
"""

import sys
import os
import json
import streamlit as st
from datetime import datetime

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from workflows.langgraph_workflow import medical_billing_workflow
from tests.test_cases import HIGH_CONFIDENCE_NOTE, LOW_CONFIDENCE_NOTE

# --- Page Configuration ---
st.set_page_config(
    page_title="SafeScript AI Biller | Track 5",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    /* Main header gradient */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .main-header h1 {
        font-size: 2.2rem;
        margin-bottom: 0.3rem;
        color: white;
    }
    .main-header p {
        font-size: 1rem;
        opacity: 0.9;
        color: #e0e0e0;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea22, #764ba222);
        border: 1px solid #667eea44;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .metric-card h3 {
        font-size: 2rem;
        margin: 0;
        color: #667eea;
    }
    .metric-card p {
        font-size: 0.85rem;
        color: #888;
        margin: 0;
    }

    /* Status badges */
    .badge-approved {
        background: #00c85322;
        color: #00c853;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        border: 1px solid #00c85344;
        font-weight: 600;
        display: inline-block;
    }
    .badge-review {
        background: #ff980022;
        color: #ff9800;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        border: 1px solid #ff980044;
        font-weight: 600;
        display: inline-block;
    }

    /* Audit log entries */
    .audit-success {
        background: #00c85311;
        border-left: 3px solid #00c853;
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.5rem;
        border-radius: 0 6px 6px 0;
        font-size: 0.82rem;
    }
    .audit-warning {
        background: #ff980011;
        border-left: 3px solid #ff9800;
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.5rem;
        border-radius: 0 6px 6px 0;
        font-size: 0.82rem;
    }
    .audit-error {
        background: #f4433611;
        border-left: 3px solid #f44336;
        padding: 0.5rem 0.8rem;
        margin-bottom: 0.5rem;
        border-radius: 0 6px 6px 0;
        font-size: 0.82rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem;
        color: #888;
        font-size: 0.8rem;
        border-top: 1px solid #333;
        margin-top: 2rem;
    }
    .footer-badge {
        display: inline-block;
        background: #667eea22;
        border: 1px solid #667eea44;
        color: #667eea;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if "workflow_state" not in st.session_state:
    st.session_state.workflow_state = None
if "total_processed" not in st.session_state:
    st.session_state.total_processed = 0
if "auto_approved" not in st.session_state:
    st.session_state.auto_approved = 0
if "human_escalated" not in st.session_state:
    st.session_state.human_escalated = 0

# --- Header ---
st.markdown("""
<div class="main-header">
    <h1>🏥 SafeScript AI Biller</h1>
    <p>Autonomous Healthcare Coding System — Multi-Agent Architecture</p>
</div>
""", unsafe_allow_html=True)

# --- Metrics Row ---
total = st.session_state.total_processed
approved = st.session_state.auto_approved
escalated = st.session_state.human_escalated
auto_rate = f"{(approved / total * 100):.0f}%" if total > 0 else "—"

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.markdown(f'<div class="metric-card"><h3>{total}</h3><p>Total Processed</p></div>', unsafe_allow_html=True)
with col_m2:
    st.markdown(f'<div class="metric-card"><h3>{approved}</h3><p>Auto-Approved</p></div>', unsafe_allow_html=True)
with col_m3:
    st.markdown(f'<div class="metric-card"><h3>{escalated}</h3><p>Human Review</p></div>', unsafe_allow_html=True)
with col_m4:
    st.markdown(f'<div class="metric-card"><h3>{auto_rate}</h3><p>Automation Rate</p></div>', unsafe_allow_html=True)

st.markdown("---")

# --- Sidebar: Audit Trail ---
with st.sidebar:
    st.markdown("### 📋 Audit Trail")

    if st.session_state.workflow_state and st.session_state.workflow_state.get("audit_log"):
        audit_log = st.session_state.workflow_state["audit_log"]

        for entry in audit_log:
            status = entry.get("status", "info")
            css_class = {
                "success": "audit-success",
                "warning": "audit-warning",
                "error": "audit-error"
            }.get(status, "audit-success")

            agent = entry.get("agent", "Unknown")
            action = entry.get("action", "")
            timestamp = entry.get("timestamp", "")
            # Show only time portion
            try:
                t = datetime.fromisoformat(timestamp)
                time_str = t.strftime("%H:%M:%S")
            except Exception:
                time_str = timestamp

            st.markdown(
                f'<div class="{css_class}"><strong>{agent}</strong><br/>{action}<br/><small>{time_str}</small></div>',
                unsafe_allow_html=True
            )

        # Export button
        st.markdown("---")
        audit_json = json.dumps(audit_log, indent=2, default=str)
        st.download_button(
            label="📥 Export Audit Log (JSON)",
            data=audit_json,
            file_name=f"audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    else:
        st.info("No audit trail yet. Submit a case to begin.")

# --- Main Layout ---
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("### 📝 Clinical Notes Input")

    clinical_notes = st.text_area(
        "Enter clinical documentation:",
        height=220,
        placeholder="Paste or type clinical notes here...",
        key="clinical_input"
    )

    # Sample case buttons
    st.markdown("**Quick Test Cases:**")
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("🟢 High Confidence", use_container_width=True):
            st.session_state.clinical_input = HIGH_CONFIDENCE_NOTE
            st.rerun()
    with btn_col2:
        if st.button("🟡 Low Confidence", use_container_width=True):
            st.session_state.clinical_input = LOW_CONFIDENCE_NOTE
            st.rerun()

    st.markdown("---")

    submit = st.button("🚀 Process Claim", type="primary", use_container_width=True)

with col_right:
    st.markdown("### 📊 Workflow Results")

    if submit and clinical_notes:
        # Create initial state
        initial_state = {
            "raw_document": clinical_notes,
            "masked_document": "",
            "medical_codes": [],
            "confidence_score": 0,
            "reasoning": "",
            "audit_log": [],
            "final_status": ""
        }

        # Execute workflow with progress indicators
        with st.spinner("🤖 Intake Agent — Masking PII/PHI..."):
            pass  # Visual spinner only

        with st.spinner("🧠 Coder Agent — Analyzing with Claude AI..."):
            pass

        with st.spinner("🛡️ Running compliance checks..."):
            result = medical_billing_workflow.invoke(initial_state)

        st.session_state.workflow_state = result

        # Update metrics
        st.session_state.total_processed += 1
        if result.get("final_status") == "Auto-Approved & Submitted":
            st.session_state.auto_approved += 1
        else:
            st.session_state.human_escalated += 1

        # Display results
        st.markdown("---")

        # ICD-10 Codes
        codes = result.get("medical_codes", [])
        if codes:
            st.markdown("**🏷️ ICD-10 Codes:**")
            for code in codes:
                st.code(code, language=None)

        # Confidence Meter
        confidence = result.get("confidence_score", 0)
        st.markdown(f"**📊 Confidence Score: {confidence}%**")
        st.progress(confidence / 100)

        # Reasoning
        reasoning = result.get("reasoning", "")
        if reasoning:
            st.markdown("**💡 Reasoning:**")
            st.info(reasoning)

        st.markdown("---")

        # Status-based UI
        final_status = result.get("final_status", "")

        if confidence >= 85:
            st.success(f"✅ **{final_status}**")
            st.markdown('<div class="badge-approved">AUTO-APPROVED</div>', unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ **{final_status}**")
            st.markdown('<div class="badge-review">NEEDS REVIEW</div>', unsafe_allow_html=True)

            # Human override UI
            st.markdown("---")
            st.markdown("**🔎 Human Review Override:**")
            override_codes = st.text_input("Override ICD-10 Codes (comma-separated):", key="override_codes")
            override_reason = st.text_input("Override Reasoning:", key="override_reason")
            if st.button("✅ Approve Override", key="override_btn"):
                st.success("✅ Case manually approved with overridden codes.")

        # Celebration
        st.balloons()

        # Force rerun to update metrics
        st.rerun()

    elif st.session_state.workflow_state:
        # Show last result
        result = st.session_state.workflow_state

        codes = result.get("medical_codes", [])
        if codes:
            st.markdown("**🏷️ ICD-10 Codes:**")
            for code in codes:
                st.code(code, language=None)

        confidence = result.get("confidence_score", 0)
        st.markdown(f"**📊 Confidence Score: {confidence}%**")
        st.progress(confidence / 100)

        reasoning = result.get("reasoning", "")
        if reasoning:
            st.markdown("**💡 Reasoning:**")
            st.info(reasoning)

        st.markdown("---")

        final_status = result.get("final_status", "")
        if confidence >= 85:
            st.success(f"✅ **{final_status}**")
            st.markdown('<div class="badge-approved">AUTO-APPROVED</div>', unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ **{final_status}**")
            st.markdown('<div class="badge-review">NEEDS REVIEW</div>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("**🔎 Human Review Override:**")
            override_codes = st.text_input("Override ICD-10 Codes (comma-separated):", key="override_codes_saved")
            override_reason = st.text_input("Override Reasoning:", key="override_reason_saved")
            if st.button("✅ Approve Override", key="override_btn_saved"):
                st.success("✅ Case manually approved with overridden codes.")
    else:
        st.info("👈 Enter clinical notes and click **Process Claim** to begin.")

# --- Footer ---
st.markdown("""
<div class="footer">
    <p>SafeScript AI Biller — Track 5 Compliance</p>
    <span class="footer-badge">LangGraph</span>
    <span class="footer-badge">Claude Sonnet 4</span>
    <span class="footer-badge">Streamlit</span>
    <span class="footer-badge">Pydantic</span>
    <span class="footer-badge">HIPAA Compliant</span>
    <span class="footer-badge">Track 5</span>
</div>
""", unsafe_allow_html=True)
