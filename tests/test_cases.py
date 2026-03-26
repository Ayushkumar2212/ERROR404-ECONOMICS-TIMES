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

# Emergency Case (Trauma)
EMERGENCY_NOTE = """Patient: Samarth Verma, Phone: 90000 11111,
Chief Complaint: Laceration to right forearm from accidental fall (shattered glass),
HPI: Patient presents with uncontrolled bleeding from a 5cm laceration on proximal forearm.
Physical Exam: Sensation intact distal to wound, 3/5 strength in grip.
Assessment: Deep laceration of right forearm with suspected nerve involvement.
Plan: Wound exploration, debridement and multi-layer suture closure."""

# General Checkup (Chronic)
GENERAL_CHECKUP_NOTE = """Patient: Anjali Gupta, age 62,
Chief Complaint: Follow up for chronic essential hypertension and Type 2 diabetes,
Assessment: Poorly controlled hypertension (155/92) and stable hyperglycemia (A1c: 7.2%).
Plan: Adjust Telmisartan to 80mg daily, continue Metformin 1g BID, scheduled nutritional therapy."""

