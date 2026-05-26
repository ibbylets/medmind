# 🧬 MedMind

AI-powered medical learning and research tool built with Groq + Streamlit.

## Features

### 🔬 Research Companion
- Search real PubMed papers by topic
- AI summarizes findings, highlights consensus, and identifies research gaps
- Follow-up Q&A grounded in the actual papers
- Direct links to PubMed articles

### 🎓 Medical Tutor
- Socratic teaching sessions on any medical topic
- Choose your level (MS1–MS4, Resident, Attending)
- USMLE-style quiz mode with score tracking
- Instant feedback and explanations

## Setup

```bash
# 1. Clone / download this folder

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Groq API key
cp .env.example .env
# Edit .env and paste your key

# 4. Run
streamlit run app.py
```

Or paste your API key directly in the sidebar — no .env needed.

## Model
Uses `llama-3.3-70b-versatile` via Groq for fast, high-quality medical responses.

## Notes
- PubMed search uses the free NCBI E-utilities API (no key needed)
- This is an educational tool, not a substitute for clinical judgment
