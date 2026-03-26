"""
SafeScript AI Biller - Coder Agent
Uses Claude Sonnet 4 for ICD-10 medical coding with anti-hallucination guardrails.
"""

import os
import re
import sys
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv

load_dotenv()


# --- Pydantic Schema ---
class MedicalCodingOutput(BaseModel):
    """Structured output for medical coding results."""
    codes: List[str] = Field(description="List of ICD-10 codes assigned")
    confidence_score: int = Field(ge=0, le=100, description="Confidence score 0-100")
    reasoning: str = Field(max_length=300, description="Clinical reasoning for code assignment")

    @field_validator("codes", mode="before")
    @classmethod
    def validate_icd10_codes(cls, v):
        """Validate that all codes match ICD-10 format."""
        icd10_pattern = re.compile(r'^[A-Z]\d{2}\.?\d{0,4}[A-Z]?$')
        validated = []
        for code in v:
            code = code.strip()
            if icd10_pattern.match(code):
                validated.append(code)
            else:
                print(f"  ⚠️ Invalid ICD-10 code format rejected: {code}")
        return validated


# --- System Prompt ---
MEDICAL_CODER_PROMPT = """You are an AAPC-certified medical coder. Your task is to assign ICD-10 codes to clinical documentation with strict guardrails.

## CONFIDENCE SCORING RULES:
- **High confidence (>85%)**: Clear diagnosis, anatomical location, and laterality are documented.
- **Low confidence (<85%)**: Vague terms like "not feeling well", missing anatomical details, only symptoms documented without a definitive diagnosis.

## ANTI-HALLUCINATION RULES (CRITICAL):
1. NEVER infer a diagnosis that is not explicitly stated in the documentation.
2. NEVER assume laterality (left/right) unless explicitly documented.
3. NEVER upgrade a symptom code to a definitive diagnosis code.
4. If documentation is vague, assign SYMPTOM codes only with LOW confidence.
5. When in doubt, code conservatively and flag for human review.

## EXAMPLES:

### Example 1 - High Confidence:
Clinical Note: "Acute bilateral maxillary sinusitis"
Output:
- codes: ["J01.00"]
- confidence_score: 95
- reasoning: "Clear diagnosis of acute bilateral maxillary sinusitis with anatomical specificity. Assigned J01.00 (Acute maxillary sinusitis, unspecified)."

### Example 2 - Low Confidence:
Clinical Note: "Headache and congestion"
Output:
- codes: ["R51.9", "R09.81"]
- confidence_score: 60
- reasoning: "Only symptoms documented without definitive diagnosis. Assigned symptom codes: R51.9 (Headache, unspecified) and R09.81 (Nasal congestion). Flagged for human review."

## OUTPUT FORMAT:
You MUST respond with ONLY a valid JSON object (no markdown, no extra text) with these exact fields:
{
    "codes": ["<ICD-10 code(s)>"],
    "confidence_score": <0-100>,
    "reasoning": "<brief clinical reasoning, max 300 characters>"
}
"""


def coder_agent(state: dict) -> dict:
    """
    Agent 2: Coder Agent
    - Uses Claude Sonnet 4 to assign ICD-10 codes
    - Validates output with Pydantic schema
    - Implements anti-hallucination guardrails
    """
    print("🧠 [Coder Agent] Analyzing clinical documentation...")

    masked_document = state.get("masked_document", "")
    audit_log = state.get("audit_log", [])

    try:
        from langchain_anthropic import ChatAnthropic

        # Initialize Claude Sonnet 4
        llm = ChatAnthropic(
            model="claude-sonnet-4-20250514",
            temperature=0,
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

        # Build the prompt
        messages = [
            ("system", MEDICAL_CODER_PROMPT),
            ("human", f"Assign ICD-10 codes to the following clinical documentation:\n\n{masked_document}")
        ]

        print("  🔄 Calling Claude Sonnet 4...")
        response = llm.invoke(messages)
        raw_output = response.content.strip()
        print(f"  📋 Raw AI response: {raw_output[:200]}...")

        # Parse JSON response
        import json
        # Handle potential markdown wrapping
        if raw_output.startswith("```"):
            raw_output = re.sub(r'^```(?:json)?\s*', '', raw_output)
            raw_output = re.sub(r'\s*```$', '', raw_output)

        parsed = json.loads(raw_output)

        # Validate with Pydantic
        coding_result = MedicalCodingOutput(**parsed)

        medical_codes = coding_result.codes
        confidence_score = coding_result.confidence_score
        reasoning = coding_result.reasoning

        print(f"  ✅ Codes: {medical_codes}")
        print(f"  📊 Confidence: {confidence_score}%")
        print(f"  💡 Reasoning: {reasoning}")

        # Audit trail
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": "Coder Agent",
            "action": "ICD-10 Code Assignment",
            "status": "success" if confidence_score >= 85 else "warning",
            "details": {
                "codes": medical_codes,
                "confidence_score": confidence_score,
                "reasoning": reasoning,
                "model": "claude-sonnet-4-20250514"
            }
        }
        audit_log.append(audit_entry)

        print(f"🧠 [Coder Agent] Complete.\n")

        return {
            "medical_codes": medical_codes,
            "confidence_score": confidence_score,
            "reasoning": reasoning,
            "audit_log": audit_log
        }

    except Exception as e:
        print(f"  ❌ Coder Agent Error: {str(e)}")

        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": "Coder Agent",
            "action": "ICD-10 Code Assignment",
            "status": "error",
            "details": {"error": str(e)}
        }
        audit_log.append(error_entry)

        return {
            "medical_codes": [],
            "confidence_score": 0,
            "reasoning": f"Error during coding: {str(e)}",
            "audit_log": audit_log
        }
