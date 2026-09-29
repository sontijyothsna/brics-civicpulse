# BRICS CivicPulse

**From Citizen Voice to Development Action**

AI-powered civic intelligence that transforms multilingual citizen signals into evidence-backed development priorities for BRICS nations.

**Track:** Innovation – AI for Digital Public Infrastructure & Governance  
**Pilot Focus:** India → scalable across BRICS

---

## Prototype Overview

This Streamlit MVP demonstrates the complete vertical slice:

1. **Multilingual Citizen Gateway** – text + mock voice input, language selector  
2. **AI Request Intelligence** – rule-based extraction of issue, location, category, urgency, affected population + clustering  
3. **National Data Fusion** – citizen signals + infrastructure indices + sample investment plans  
4. **Development Hotspot Engine** – map of demand vs infrastructure gaps  
5. **Policy Recommendation Engine** – ranked evidence cards with priority scores  
6. **Impact Measurement** – before/after trajectory of citizen demand and access scores  

> All citizen reports and impact numbers are **synthetic** for demonstration purposes.

---

## Quick Start (Local)

```bash
# Clone / navigate
cd civicpulse

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
```

Open http://localhost:8501

---

## Project Structure

```
civicpulse/
├── app.py                 # Main Streamlit application
├── requirements.txt
├── README.md
├── data/
│   ├── sample_requests.csv    # 30 synthetic citizen reports
│   ├── infrastructure.csv     # District-level infrastructure scores
│   └── investment_plans.csv   # Sample public investment plans
└── .streamlit/
    └── config.toml            # Theme (optional)
```

---

## Priority Score Formula (Prototype)

```
Priority = 0.30 × Citizen Demand
         + 0.25 × Infrastructure Deficit
         + 0.20 × Population Impact
         + 0.15 × Urgency
         + 0.10 × Investment Gap
```

All factors normalized 0–100.  
**Score is a decision-support indicator only.** Final decisions remain with human policymakers.

---

## Key Innovation – Alignment Layer

```
Citizen Demand
+ Demographic Need
+ Infrastructure Deficit
+ Investment Gap
= Evidence-backed Development Intelligence
```

Traditional grievance systems answer “What are citizens complaining about?”  
CivicPulse answers “Where does citizen demand align with measurable development need and investment gaps?”

---

## Responsible AI & Transparency

- Human-in-the-loop: AI recommends, humans decide  
- Confidence scores shown on every recommendation  
- Data minimization & aggregated dashboards  
- Explicit limitations stated in the Impact page  
- Synthetic data clearly labelled  

---

## Roadmap

| Phase | Scope |
|-------|--------|
| **1 – India Pilot** | EN + HI + 1 regional language, 2–3 districts, core workflow |
| **2 – Multi-State** | More languages & government datasets, state integration |
| **3 – BRICS Scale** | Country-specific data & languages under shared interoperability standards |

---

## Licence & Contact

Prototype created for the BRICS / national innovation challenge.  
Designed as a reusable digital public good concept.

**Tagline:** From Citizen Voice to Development Action
