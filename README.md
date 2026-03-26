# 🏥 SafeScript AI Biller

> **Autonomous Healthcare Coding System** — Multi-Agent Architecture with LangGraph & Claude AI

SafeScript AI Biller is an intelligent medical billing agent that automates ICD-10 code assignment from clinical documentation using a multi-agent pipeline with built-in compliance guardrails.

---

## ✨ Features

| Feature | Description |
|---|---|
| **🤖 Intake Agent** | PII/PHI masking (Aadhaar, phone, email, names) with SHA-256 document hashing |
| **🧠 Coder Agent** | Claude Sonnet 4 powered ICD-10 coding with anti-hallucination guardrails |
| **🛡️ Compliance Agent** | Auto-approval (≥85% confidence) or human escalation (<85%) |
| **🔀 Conditional Routing** | LangGraph StateGraph with confidence-based branching |
| **📋 Audit Trail** | Immutable append-only log with timestamps and agent actions |
| **📊 Streamlit Dashboard** | Real-time metrics, color-coded audit trail, and human override UI |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SafeScript AI Biller                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  📄 Clinical Notes                                              │
│       │                                                         │
│       ▼                                                         │
│  ┌──────────────┐                                               │
│  │ 🤖 Intake    │  PII Masking → SHA-256 Hash → Audit Log      │
│  │    Agent     │                                               │
│  └──────┬───────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────┐                                               │
│  │ 🧠 Coder    │  Claude Sonnet 4 → ICD-10 Codes → Validate   │
│  │    Agent     │  (temperature=0, anti-hallucination)          │
│  └──────┬───────┘                                               │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────┐    ≥ 85%    ┌───────────────────┐             │
│  │  Confidence  │────────────▶│ 🛡️ Compliance     │             │
│  │  Check       │             │    Auto-Approve    │             │
│  └──────┬───────┘             └───────────────────┘             │
│         │                                                       │
│         │  < 85%              ┌───────────────────┐             │
│         └────────────────────▶│ ⚠️ Human Review    │             │
│                               │    Escalation     │             │
│                               └───────────────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

### 3. Run the Test Suite

```bash
python tests/test_workflow.py
```

### 4. Launch the Dashboard

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
safescript-ai-biller/
├── .env.example              # API key template
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── app.py                    # Streamlit dashboard
├── agents/
│   ├── __init__.py
│   ├── intake_agent.py       # PII/PHI masking agent
│   ├── coder_agent.py        # Claude AI coding agent
│   └── compliance_agent.py   # Compliance & escalation agent
├── workflows/
│   ├── __init__.py
│   └── langgraph_workflow.py # LangGraph state graph
└── tests/
    ├── __init__.py
    ├── test_cases.py          # Sample clinical notes
    └── test_workflow.py       # Workflow integration tests
```

---

## 🛡️ Guardrails

- **PII/PHI Masking**: Aadhaar numbers, phone numbers, emails, and patient names are masked before AI processing
- **Anti-Hallucination**: Claude is instructed to never infer, assume laterality, or upgrade symptom codes
- **Temperature 0**: Deterministic AI responses for reproducibility
- **ICD-10 Validation**: Pydantic validator enforces `^[A-Z]\d{2}\.?\d{0,4}[A-Z]?$` format
- **Immutable Audit Trail**: Append-only log with timestamps for compliance
- **Human-in-the-Loop**: Automatic escalation when confidence < 85%

---

## ✅ Track 5 Compliance Checklist

- [x] Multi-agent architecture (3 agents)
- [x] LangGraph StateGraph orchestration
- [x] Claude Sonnet 4 integration
- [x] Conditional routing (confidence-based)
- [x] PII/PHI masking (HIPAA)
- [x] Immutable audit trail
- [x] Anti-hallucination guardrails
- [x] Human-in-the-loop escalation
- [x] Streamlit dashboard
- [x] Pydantic data validation
- [x] ICD-10 code format validation
- [x] Test suite with high/low confidence cases

---

## 🧰 Tech Stack

| Technology | Usage |
|---|---|
| Python 3.8+ | Core runtime |
| LangGraph | Agent orchestration & state management |
| Claude Sonnet 4 | Medical coding AI |
| Streamlit | Dashboard UI |
| Pydantic | Data validation & schema enforcement |
| python-dotenv | Environment configuration |

---

*Built for Track 5 — SafeScript AI Medical Billing Agent*
