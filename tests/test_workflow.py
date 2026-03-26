"""
SafeScript AI Biller - Workflow Tests
Runs both high and low confidence test cases through the full LangGraph workflow.
"""

import sys
import os

# Ensure parent directory is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflows.langgraph_workflow import medical_billing_workflow
from tests.test_cases import HIGH_CONFIDENCE_NOTE, LOW_CONFIDENCE_NOTE


def run_test(test_name: str, clinical_note: str):
    """Run a single test case through the workflow."""
    print("=" * 70)
    print(f"TEST: {test_name}")
    print("=" * 70)

    initial_state = {
        "raw_document": clinical_note,
        "masked_document": "",
        "medical_codes": [],
        "confidence_score": 0,
        "reasoning": "",
        "audit_log": [],
        "final_status": ""
    }

    # Invoke the workflow
    result = medical_billing_workflow.invoke(initial_state)

    # Display results
    print("\n" + "-" * 40)
    print("RESULTS:")
    print("-" * 40)
    print(f"  Final Status   : {result.get('final_status', 'N/A')}")
    print(f"  Medical Codes  : {result.get('medical_codes', [])}")
    print(f"  Confidence     : {result.get('confidence_score', 0)}%")
    print(f"  Reasoning      : {result.get('reasoning', 'N/A')}")
    print(f"  Audit Entries  : {len(result.get('audit_log', []))}")
    print("-" * 40 + "\n")

    return result


if __name__ == "__main__":
    print("\nSafeScript AI Biller - Workflow Test Suite\n")

    # Test 1: High Confidence
    result_high = run_test("HIGH CONFIDENCE CASE", HIGH_CONFIDENCE_NOTE)

    # Test 2: Low Confidence
    result_low = run_test("LOW CONFIDENCE CASE", LOW_CONFIDENCE_NOTE)

    # Summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"  High Confidence → Status: {result_high.get('final_status', 'N/A')}")
    print(f"  Low Confidence  → Status: {result_low.get('final_status', 'N/A')}")
    print("=" * 70)
    print("\nAll tests executed successfully!")
