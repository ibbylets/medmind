import streamlit as st
from groq import Groq
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="MedMind",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
    theme={"base": "light"}
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;0,500;1,300&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --bg:        #faf9f7;
    --surface:   #ffffff;
    --surface2:  #f5f2ee;
    --border:    #e8e2d9;
    --border2:   #d4ccc0;
    --tan:       #c9a882;
    --tan-light: #e8d9c5;
    --tan-dim:   #a8845e;
    --text:      #1a1714;
    --text2:     #4a4440;
    --muted:     #8a7e76;
    --muted2:    #b0a89e;
    --green:     #5a8a6a;
    --red:       #c0504a;
    --surface-hover: #f0ebe4;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"],
.stApp, .main, .block-container {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] > div { padding-top: 1.5rem; }

.logo-wrap { padding: 0 0 1.25rem 0; border-bottom: 1px solid var(--border); margin-bottom: 1.5rem; }
.logo-mark { font-family: 'Fraunces', serif; font-weight: 500; font-size: 1.7rem; letter-spacing: -0.02em; color: var(--text); line-height: 1; }
.logo-mark span { color: var(--tan-dim); }
.logo-sub { font-family: 'DM Mono', monospace; font-size: 0.58rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--muted); margin-top: 5px; }

.nav-label { font-family: 'DM Mono', monospace; font-size: 0.58rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--muted2); margin-bottom: 0.5rem; }

.page-header { padding: 2rem 0 1.5rem 0; border-bottom: 1px solid var(--border); margin-bottom: 2rem; }
.page-eyebrow { font-family: 'DM Mono', monospace; font-size: 0.62rem; letter-spacing: 0.18em; text-transform: uppercase; color: var(--tan-dim); margin-bottom: 0.5rem; }
.page-title { font-family: 'Fraunces', serif; font-weight: 400; font-size: 2.4rem; letter-spacing: -0.03em; color: var(--text); line-height: 1.1; margin: 0; }
.page-desc { font-family: 'Fraunces', serif; font-style: italic; font-weight: 300; font-size: 1rem; color: var(--muted); margin-top: 0.6rem; }

.paper-card { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1.1rem 1.3rem; margin-bottom: 0.75rem; transition: border-color 0.2s, background 0.2s; }
.paper-card:hover { border-color: var(--tan-light); background: var(--surface-hover); }
.paper-num { font-family: 'DM Mono', monospace; font-size: 0.62rem; color: var(--tan-dim); letter-spacing: 0.1em; margin-bottom: 0.3rem; }
.paper-title { font-family: 'DM Sans', sans-serif; font-weight: 600; font-size: 0.95rem; color: var(--text); margin-bottom: 0.5rem; line-height: 1.4; }
.paper-abstract { font-size: 0.85rem; color: var(--text2); line-height: 1.65; margin-bottom: 0.75rem; }
.paper-link { font-family: 'DM Mono', monospace; font-size: 0.62rem; color: var(--tan-dim); text-decoration: none; letter-spacing: 0.05em; }
.paper-link:hover { color: var(--tan); }

.chat-wrap { margin: 0.75rem 0; }
.bubble-meta { font-family: 'DM Mono', monospace; font-size: 0.6rem; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.35rem; color: var(--muted2); }
.bubble-user-meta { text-align: right; color: var(--tan-dim); }
.bubble-user { background: var(--tan-light); border: 1px solid var(--border2); border-radius: 16px 16px 4px 16px; padding: 0.9rem 1.15rem; margin-left: auto; max-width: 75%; font-size: 0.95rem; line-height: 1.65; color: var(--text); }
.bubble-ai { background: var(--surface); border: 1px solid var(--border); border-left: 3px solid var(--tan-light); border-radius: 4px 16px 16px 16px; padding: 0.9rem 1.15rem; max-width: 88%; font-size: 0.95rem; line-height: 1.75; color: var(--text); }

.score-bar { display: flex; align-items: center; gap: 1rem; background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; padding: 0.75rem 1.25rem; margin-bottom: 1rem; }
.score-label { font-family: 'DM Mono', monospace; font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); }
.score-value { font-family: 'Fraunces', serif; font-weight: 500; font-size: 1.2rem; color: var(--green); }
.score-pct { font-family: 'DM Mono', monospace; font-size: 0.75rem; color: var(--muted); }

.topic-card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 2rem; margin-bottom: 1rem; }
.topic-card-title { font-family: 'Fraunces', serif; font-weight: 400; font-size: 1.2rem; color: var(--text); margin-bottom: 1.5rem; letter-spacing: -0.01em; }

.stat-pill { display: inline-flex; align-items: center; gap: 0.4rem; background: var(--surface2); border: 1px solid var(--border); border-radius: 20px; padding: 0.3rem 0.85rem; font-family: 'DM Mono', monospace; font-size: 0.62rem; color: var(--muted); letter-spacing: 0.04em; }
.stat-pill-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--green); animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

.stButton > button { background: var(--tan) !important; color: #fff !important; border: none !important; border-radius: 6px !important; font-family: 'DM Sans', sans-serif !important; font-weight: 500 !important; font-size: 0.88rem !important; padding: 0.5rem 1.4rem !important; transition: all 0.15s !important; }
.stButton > button:hover { background: var(--tan-dim) !important; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea { background: var(--surface) !important; border: 1px solid var(--border2) !important; border-radius: 6px !important; color: var(--text) !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.95rem !important; padding: 0.65rem 1rem !important; }
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus { border-color: var(--tan) !important; box-shadow: 0 0 0 2px var(--tan-light) !important; }

.stSelectbox > div > div { background: var(--surface) !important; border: 1px solid var(--border2) !important; border-radius: 6px !important; color: var(--text) !important; font-size: 0.95rem !important; }

/* Radio buttons — full label visible */
.stRadio > div { gap: 0.4rem !important; }
.stRadio > div > label {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    padding: 0.55rem 1rem !important;
    cursor: pointer !important;
    transition: all 0.15s !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    color: var(--text2) !important;
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
}
.stRadio > div > label:hover { border-color: var(--tan) !important; color: var(--text) !important; }
.stRadio > div > label > div { display: flex !important; align-items: center !important; gap: 0.5rem !important; }
/* Show the radio label text */
.stRadio [data-testid="stMarkdownContainer"] p { 
    font-size: 0.88rem !important; 
    color: var(--text2) !important;
    display: inline !important;
}

[data-testid="stExpander"] { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; }

hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }
#MainMenu, footer { visibility: hidden; }
header { visibility: visible; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }

label { color: var(--muted) !important; font-family: 'DM Mono', monospace !important; font-size: 0.7rem !important; letter-spacing: 0.08em !important; }
p, li, div { font-size: 0.95rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state defaults ──────────────────────────────────────
for key, default in {
    "api_key": "",
    "mode": "🔬 Research Companion",
    "research_messages": [],
    "tutor_messages": [],
    "pubmed_results": [],
    "tutor_topic": "",
    "tutor_phase": "idle",
    "quiz_score": [0, 0],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Helper functions ────────────────────────────────────────────
def chat(messages, system):
    client = Groq(api_key=st.session_state["api_key"])
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system}] + messages,
        max_tokens=2048,
    )
    return response.choices[0].message.content

def search_pubmed(query, n=5):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    search = requests.get(f"{base}esearch.fcgi", params={"db":"pubmed","term":query,"retmax":n,"retmode":"json"}).json()
    ids = search["esearchresult"]["idlist"]
    if not ids:
        return []
    fetch = requests.get(f"{base}efetch.fcgi", params={"db":"pubmed","id":",".join(ids),"retmode":"xml","rettype":"abstract"})
    results = []
    import xml.etree.ElementTree as ET
    root = ET.fromstring(fetch.text)
    for article in root.findall(".//PubmedArticle"):
        try:
            pmid = article.findtext(".//PMID", "")
            title = article.findtext(".//ArticleTitle", "No title")
            abstract = article.findtext(".//AbstractText", "No abstract available.")
            year = article.findtext(".//PubDate/Year", "n.d.")
            results.append({"pmid": pmid, "title": title, "abstract": abstract, "year": year})
        except Exception:
            continue
    return results

# ── Sidebar ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="logo-wrap"><div class="logo-mark">Med<span>Mind</span></div><div class="logo-sub">Clinical Intelligence</div></div>', unsafe_allow_html=True)

    api_input = st.text_input("GROQ API KEY", type="password", placeholder="gsk_...", value=st.session_state["api_key"])
    if api_input:
        st.session_state["api_key"] = api_input

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="nav-label">Navigation</div>', unsafe_allow_html=True)
    mode = st.radio(
        "nav",
        ["🔬 Research Companion", "🎓 Medical Tutor"],
        label_visibility="collapsed",
        format_func=lambda x: x
    )
    st.session_state["mode"] = mode

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="stat-pill">
        <div class="stat-pill-dot"></div>
        llama-3.3-70b · groq
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    if st.button("Clear Session"):
        for k in ["research_messages", "tutor_messages", "pubmed_results"]:
            st.session_state[k] = []
        st.session_state["tutor_topic"] = ""
        st.session_state["tutor_phase"] = "idle"
        st.session_state["quiz_score"] = [0, 0]
        st.rerun()

# ── Main content ────────────────────────────────────────────────
if "Research" in st.session_state["mode"]:
    st.markdown("""
    <div class="page-header">
        <div class="page-eyebrow">Mode 01 — PubMed + AI Analysis</div>
        <div class="page-title">Research Companion</div>
        <div class="page-desc">Search real papers, get AI synthesis, ask follow-up questions grounded in evidence.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input("SEARCH QUERY", placeholder="e.g. GLP-1 agonists cardiovascular outcomes type 2 diabetes")
    with col2:
        n = st.selectbox("PAPERS", [3, 5, 8], index=1)

    if st.button("Search PubMed →"):
        if query:
            with st.spinner("Searching PubMed..."):
                results = search_pubmed(query, n)
                st.session_state["pubmed_results"] = results
                st.session_state["research_messages"] = []
            if results:
                abstracts = "\n\n".join([f"[{i+1}] {r['title']} ({r['year']})\n{r['abstract']}" for i, r in enumerate(results)])
                system = """You are a senior medical research analyst. Given PubMed abstracts:
1. Write a sharp overview of what the papers collectively demonstrate (2-3 sentences)
2. List key findings with paper citations [1][2] etc.
3. Note any conflicts or gaps in the evidence
4. Propose 3 specific follow-up research questions
Be precise and evidence-based. Use markdown formatting."""
                with st.spinner("Analyzing papers with AI..."):
                    response = chat([{"role": "user", "content": f"Analyze these papers on: {query}\n\n{abstracts}"}], system)
                st.session_state["research_messages"] = [
                    {"role": "user", "content": f"Search: {query}"},
                    {"role": "assistant", "content": response},
                ]
                st.rerun()
        else:
            st.warning("Enter a search query first.")

    if st.session_state["pubmed_results"]:
        with st.expander(f"📄 {len(st.session_state['pubmed_results'])} papers retrieved"):
            for i, p in enumerate(st.session_state["pubmed_results"]):
                st.markdown(f"""
                <div class="paper-card">
                    <div class="paper-num">PAPER {i+1:02d} · PMID {p['pmid']} · {p['year']}</div>
                    <div class="paper-title">{p['title']}</div>
                    <div class="paper-abstract">{p['abstract'][:350]}...</div>
                    <a class="paper-link" href="https://pubmed.ncbi.nlm.nih.gov/{p['pmid']}/" target="_blank">VIEW ON PUBMED →</a>
                </div>
                """, unsafe_allow_html=True)

    if st.session_state["research_messages"]:
        now = datetime.now().strftime("%H:%M")
        for msg in st.session_state["research_messages"]:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-wrap"><div class="bubble-meta bubble-user-meta">YOU · {now}</div><div class="bubble-user">{msg["content"]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-wrap"><div class="bubble-meta">MEDMIND · {now}</div><div class="bubble-ai">{msg["content"]}</div></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        followup = st.text_input("FOLLOW-UP QUESTION", placeholder="Ask anything about these papers...", key="fu")
        if st.button("Ask →", key="ask_btn"):
            if followup:
                abstracts = "\n\n".join([f"[{i+1}] {r['title']} ({r['year']})\n{r['abstract']}" for i, r in enumerate(st.session_state["pubmed_results"])])
                system = f"You are a medical research expert. Context papers:\n\n{abstracts}\n\nAnswer precisely, cite [1][2] etc."
                st.session_state["research_messages"].append({"role": "user", "content": followup})
                history = [{"role": m["role"], "content": m["content"]} for m in st.session_state["research_messages"]]
                with st.spinner("Thinking..."):
                    response = chat(history, system)
                st.session_state["research_messages"].append({"role": "assistant", "content": response})
                st.rerun()

elif "Tutor" in st.session_state["mode"]:
    st.markdown("""
    <div class="page-header">
        <div class="page-eyebrow">Mode 02 — Socratic Learning + Board Prep</div>
        <div class="page-title">Medical Tutor</div>
        <div class="page-desc">Learn through Socratic dialogue. Quiz yourself with USMLE-style questions.</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state["tutor_phase"] == "idle":
        st.markdown('<div class="topic-card">', unsafe_allow_html=True)
        st.markdown('<div class="topic-card-title">Choose a topic to begin</div>', unsafe_allow_html=True)
        topic = st.text_input("TOPIC", placeholder="e.g. Diabetic ketoacidosis, Acute MI, Sepsis management...")
        level = st.selectbox("YOUR LEVEL", ["Medical Student (Year 1–2)", "Medical Student (Year 3–4)", "Resident", "Attending / Review"])
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 Start Teaching"):
                if topic:
                    st.session_state["tutor_topic"] = topic
                    st.session_state["tutor_phase"] = "teaching"
                    system = f"""You are a brilliant medical educator using Socratic method.
Topic: {topic}. Level: {level}.
Start with a 2-sentence engaging overview, then ask ONE probing question to gauge baseline knowledge.
Teach one concept at a time. Use clinical vignettes. Bold key terms. Never overwhelm."""
                    with st.spinner("Starting session..."):
                        init = chat([{"role": "user", "content": f"Teach me about {topic}"}], system)
                    st.session_state["tutor_messages"] = [{"role": "assistant", "content": init, "system": system}]
                    st.rerun()
        with col2:
            if st.button("📝 Start Quiz"):
                if topic:
                    st.session_state["tutor_topic"] = topic
                    st.session_state["tutor_phase"] = "quizzing"
                    st.session_state["quiz_score"] = [0, 0]
                    system = f"""You are a USMLE question writer. Topic: {topic}. Level: {level}.
Generate ONE clinical vignette question at a time.
Format EXACTLY:
**Question:** [vignette]
**A)** ... **B)** ... **C)** ... **D)** ... **E)** ...
Wait for the answer. Then give ✅ or ❌, correct answer, and clear explanation. Then next question."""
                    with st.spinner("Generating first question..."):
                        init = chat([{"role": "user", "content": f"Quiz me on {topic}"}], system)
                    st.session_state["tutor_messages"] = [{"role": "assistant", "content": init, "system": system}]
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        topic = st.session_state["tutor_topic"]
        phase = st.session_state["tutor_phase"]
        col1, col2 = st.columns([5, 1])
        with col1:
            icon = "📖" if phase == "teaching" else "📝"
            mode_label = "Teaching Session" if phase == "teaching" else "Quiz Mode"
            st.markdown(f'<div style="font-family:DM Sans,sans-serif;font-weight:700;font-size:1.1rem;color:var(--text);">{icon} {topic} <span style="font-weight:400;color:var(--muted2);font-size:0.85rem;">— {mode_label}</span></div>', unsafe_allow_html=True)
        with col2:
            if st.button("← Back"):
                st.session_state["tutor_phase"] = "idle"
                st.session_state["tutor_messages"] = []
                st.rerun()

        if phase == "quizzing":
            correct, total = st.session_state["quiz_score"]
            pct = int(correct / total * 100) if total > 0 else 0
            st.markdown(f'<div class="score-bar"><div class="score-label">Score</div><div class="score-value">{correct}/{total}</div><div class="score-pct">{pct}% correct</div></div>', unsafe_allow_html=True)

        now = datetime.now().strftime("%H:%M")
        for msg in st.session_state["tutor_messages"]:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-wrap"><div class="bubble-meta bubble-user-meta">YOU · {now}</div><div class="bubble-user">{msg["content"]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-wrap"><div class="bubble-meta">MEDMIND · {now}</div><div class="bubble-ai">{msg["content"]}</div></div>', unsafe_allow_html=True)

        placeholder = "Type your answer (A/B/C/D/E)..." if phase == "quizzing" else "Your response..."
        user_input = st.text_input("YOUR RESPONSE", placeholder=placeholder, key="tutor_in")
        if st.button("Send →", key="tutor_send"):
            if user_input:
                if phase == "quizzing":
                    sc = st.session_state["quiz_score"]
                    st.session_state["quiz_score"] = [sc[0], sc[1] + 1]
                st.session_state["tutor_messages"].append({"role": "user", "content": user_input})
                system = st.session_state["tutor_messages"][0].get("system", "You are a medical tutor.")
                history = [{"role": m["role"], "content": m["content"]} for m in st.session_state["tutor_messages"]]
                with st.spinner("..."):
                    response = chat(history, system)
                if phase == "quizzing" and ("✅" in response or "correct" in response.lower()):
                    sc = st.session_state["quiz_score"]
                    st.session_state["quiz_score"] = [sc[0] + 1, sc[1]]
                st.session_state["tutor_messages"].append({"role": "assistant", "content": response})
                st.rerun()