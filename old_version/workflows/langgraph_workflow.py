"""
SafeScript AI Biller - LangGraph Workflow
Defines the multi-agent state graph with conditional routing based on confidence scores.
"""

import sys
import os
from typing import TypedDict, List, Any

from langgraph.graph import StateGraph, END

# Ensure parent directory is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.intake_agent import intake_agent
from agents.coder_agent import coder_agent
from agents.compliance_agent import compliance_agent, human_escalation


# --- State Definition ---
class PatientState(TypedDict):
    raw_document: str
    masked_document: str
    medical_codes: List[str]
    confidence_score: int
    reasoning: str
    audit_log: List[Any]
    final_status: str


# --- Conditional Routing ---
def check_confidence(state: dict) -> str:
    """Route based on confidence score threshold."""
    confidence = state.get("confidence_score", 0)
    if confidence >= 85:
        print(f"📊 [Router] Confidence {confidence}% >= 85% → Auto-Approval Path")
        return "continue_to_compliance"
    else:
        print(f"📊 [Router] Confidence {confidence}% < 85% → Human Escalation Path")
        return "escalate_to_human"


# --- Build the StateGraph ---
workflow = StateGraph(PatientState)

# Add nodes
workflow.add_node("Intake", intake_agent)
workflow.add_node("Coder", coder_agent)
workflow.add_node("Compliance", compliance_agent)
workflow.add_node("Human_Review", human_escalation)

# Define edges
workflow.set_entry_point("Intake")
workflow.add_edge("Intake", "Coder")

# Conditional routing from Coder based on confidence score
workflow.add_conditional_edges(
    "Coder",
    check_confidence,
    {
        "continue_to_compliance": "Compliance",
        "escalate_to_human": "Human_Review"
    }
)

# Both paths end
workflow.add_edge("Compliance", END)
workflow.add_edge("Human_Review", END)

# Compile the workflow
medical_billing_workflow = workflow.compile()

print("✅ LangGraph Workflow compiled successfully!")
