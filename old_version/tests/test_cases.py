"""
SafeScript AI Biller - Test Cases
Sample clinical notes for testing high and low confidence scenarios.
"""

# High confidence case: Clear diagnosis with specific details
HIGH_CONFIDENCE_NOTE = """Patient: Rajesh Kumar (Aadhaar: 1234 5678 9012, Phone: 9876543210),
Chief Complaint: Acute bilateral maxillary sinusitis,
Assessment: Acute bilateral maxillary sinusitis,
Plan: Amoxicillin-clavulanate"""

# Low confidence case: Vague symptoms without definitive diagnosis
LOW_CONFIDENCE_NOTE = """Patient: Priya Sharma,
Chief Complaint: Not feeling well,
HPI: headache and congestion,
Assessment: Symptomatic treatment"""
