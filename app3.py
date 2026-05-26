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
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Syne+Mono&family=Lora:ital,wght@0,400;0,500;1,400&display=swap');

:root {
    --bg:       #080c10;
    --surface:  #0e1419;
    --surface2: #141b23;
    --border:   #1e2832;
    --border2:  #263040;
    --cyan:     #00d4ff;
    --cyan-dim: #0099bb;
    --green:    #00ff9d;
    --green-dim:#00bb70;
    --amber:    #ffb300;
    --muted:    #4a6070;
    --muted2:   #6a8090;
    --text:     #d0dde8;
    --text2:    #90aabb;
    --danger:   #ff4060;
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Lora', Georgia, serif;
    background-color: var(--bg);
    color: var(--text);
}

body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] > div { padding-top: 1.5rem; }

.logo-wrap { padding: 0 0 1rem 0; border-bottom: 1px solid var(--border); margin-bottom: 1.5rem; }
.logo-mark { font-family: 'Syne', sans-serif; font-weight: 800; font-size: 1.6rem; letter-spacing: -0.03em; color: var(--text); line-height: 1; }
.logo-mark span { color: var(--cyan); }
.logo-sub { font-family: 'Syne Mono', monospace; font-size: 0.6rem; letter-spacing: 0.2em; text-transform: uppercase; color: var(--muted); margin-top: 4px; }

.nav-label { font-family: 'Syne Mono', monospace; font-size: 0.6rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--muted); margin-bottom: 0.5rem; }

.page-header { padding: 2rem 0 1.5rem 0; border-bottom: 1px solid var(--border); margin-bottom: 2rem; }
.page-eyebrow { font-family: 'Syne Mono', monospace; font-size: 0.65rem; letter-spacing: 0.2em; text-transform: uppercase; color: var(--cyan); margin-bottom: 0.5rem; }
.page-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 2.2rem; letter-spacing: -0.04em; color: var(--text); line-height: 1.1; margin: 0; }
.page-desc { font-family: 'Lora', serif; font-style: italic; font-size: 0.95rem; color: var(--muted2); margin-top: 0.5rem; }

.paper-card { background: var(--surface2); border: 1px solid var(--border); border-radius: 4px; padding: 1rem 1.25rem; margin-bottom: 0.75rem; }
.paper-num { font-family: 'Syne Mono', monospace; font-size: 0.6rem; color: var(--cyan); letter-spacing: 0.1em; margin-bottom: 0.25rem; }
.paper-title { font-family: 'Syne', sans-serif; font-weight: 600; font-size: 0.9rem; color: var(--text); margin-bottom: 0.5rem; line-height: 1.3; }
.paper-abstract { font-size: 0.8rem; color: var(--muted2); line-height: 1.6; margin-bottom: 0.75rem; }
.paper-link { font-family: 'Syne Mono', monospace; font-size: 0.65rem; color: var(--cyan); text-decoration: none; letter-spacing: 0.05em; }

.chat-wrap { margin: 0.5rem 0; }
.bubble-meta { font-family: 'Syne Mono', monospace; font-size: 0.58rem; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.3rem; color: var(--muted); }
.bubble-user-meta { text-align: right; color: var(--cyan-dim); }
.bubble-user { background: linear-gradient(135deg, #0a1e30, #0d2540); border: 1px solid #1a3a5a; border-radius: 12px 12px 2px 12px; padding: 0.85rem 1.1rem; margin-left: auto; max-width: 78%; font-size: 0.92rem; line-height: 1.6; color: var(--text); }
.bubble-ai { background: var(--surface); border: 1px solid var(--border); border-left: 2px solid var(--cyan-dim); border-radius: 2px 12px 12px 12px; padding: 0.85rem 1.1rem; max-width: 88%; font-size: 0.92rem; line-height: 1.7; color: var(--text); }

.score-bar { display: flex; align-items: center; gap: 1rem; background: var(--surface); border: 1px solid var(--border); border-radius: 4px; padding: 0.75rem 1.25rem; margin-bottom: 1rem; }
.score-label { font-family: 'Syne Mono', monospace; font-size: 0.65rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--muted); }
.score-value { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1.1rem; color: var(--green); }
.score-pct { font-family: 'Syne Mono', monospace; font-size: 0.75rem; color: var(--muted2); }

.topic-card { background: var(--surface); border: 1px solid var(--border); border-radius: 4px; padding: 2rem; margin-bottom: 1rem; }
.topic-card-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1.1rem; color: var(--text); margin-bottom: 1.5rem; letter-spacing: -0.02em; }

.stat-pill { display: inline-flex; align-items: center; gap: 0.4rem; background: var(--surface2); border: 1px solid var(--border); border-radius: 2px; padding: 0.25rem 0.75rem; font-family: 'Syne Mono', monospace; font-size: 0.65rem; color: var(--muted2); letter-spacing: 0.05em; }
.stat-pill-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--green); animation: pulse 2s infinite; }

@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

.stButton > button { background: transparent !important; color: var(--cyan) !important; border: 1px solid var(--cyan-dim) !important; border-radius: 2px !important; font-family: 'Syne', sans-serif !important; font-weight: 600 !important; font-size: 0.8rem !important; letter-spacing: 0.05em !important; padding: 0.45rem 1.25rem !important; transition: all 0.15s !important; }
.stButton > button:hover { background: var(--cyan) !important; color: #000 !important; }

.stTextInput > div > div > input, .stTextArea > div > div > textarea { background: var(--surface) !important; border: 1px solid var(--border2) !important; border-radius: 2px !important; color: var(--text) !important; font-family: 'Lora', serif !important; font-size: 0.9rem !important; padding: 0.6rem 0.9rem !important; }
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus { border-color: var(--cyan-dim) !important; box-shadow: 0 0 0 1px var(--cyan-dim) !important; }

.stSelectbox > div > div { background: var(--surface) !important; border: 1px solid var(--border2) !important; border-radius: 2px !important; color: var(--text) !important; }

.stRadio > div { gap: 0.5rem !important; }
.stRadio > div > label { background: var(--surface2) !important; border: 1px solid var(--border) !important; border-radius: 2px !important; padding: 0.5rem 1rem !important; cursor: pointer !important; transition: all 0.15s !important; font-family: 'Syne', sans-serif !important; font-size: 0.82rem !important; color: var(--text2) !important; }
.stRadio > div > label:hover { border-color: var(--cyan-dim) !important; color: var(--text) !important; }

[data-testid="stExpander"] { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: 4px !important; }

hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }
#MainMenu, footer { visibility: hidden; }
header { visibility: visible; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }
label { color: var(--muted2) !important; font-family: 'Syne Mono', monospace !important; font-size: 0.7rem !important; letter-spacing: 0.1em !important; }
</style>
""", unsafe_allow_html=True)

def get_client():
    api_key = st.session_state.get("api_key") or os.getenv("GROQ_API_KEY", "")
    if api_key:
        return Groq(api_key=api_key)
    return None

def chat(messages: list[dict], system: str):
    client = get_client()
    if not client:
        st.error("No API key found. Add it in the sidebar.")
        return ""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system}] + messages,
            temperature=0.65,
            max_tokens=2048,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"API error: {e}")
        return ""

def search_pubmed(query: str, max_results: int = 5) -> list[dict]:
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    try:
        ids = requests.get(
            f"{base}esearch.fcgi?db=pubmed&term={requests.utils.quote(query)}&retmax={max_results}&retmode=json&sort=relevance",
            timeout=8
        ).json()["esearchresult"]["idlist"]
        if not ids:
            return []
        summary = requests.get(
            f"{base}esummary.fcgi?db=pubmed&id={','.join(ids)}&retmode=json",
            timeout=10
        ).json().get("result", {})
        articles = []
        for uid in ids:
            p = summary.get(uid, {})
            title = p.get("title", "No title")
            year  = p.get("pubdate", "n.d.")[:4]
            abs_r = requests.get(
                f"{base}efetch.fcgi?db=pubmed&id={uid}&rettype=abstract&retmode=text",
                timeout=8
            ).text.strip()
            abstract = abs_r[:1500] if abs_r else "No abstract available."
            articles.append({"pmid": uid, "title": title, "abstract": abstract, "year": year})
        return articles
    except Exception as e:
        st.warning(f"PubMed error: {e}")
        return []

defaults = {
    "mode": "Research Companion",
    "research_messages": [],
    "tutor_messages": [],
    "tutor_topic": "",
    "tutor_phase": "idle",
    "quiz_score": [0, 0],
    "pubmed_results": [],
    "api_key": os.getenv("GROQ_API_KEY", ""),
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

with st.sidebar:
    st.markdown("""
    <div class="logo-wrap">
        <div class="logo-mark">Med<span>Mind</span></div>
        <div class="logo-sub">AI Medical Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    api_input = st.text_input("GROQ API KEY", type="password", placeholder="gsk_...", value=st.session_state["api_key"])
    if api_input:
        st.session_state["api_key"] = api_input

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="nav-label">Navigation</div>', unsafe_allow_html=True)
    mode = st.radio("nav", ["🔬 Research Companion", "🎓 Medical Tutor"], label_visibility="collapsed")
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
        for k in ["research_messages","tutor_messages","pubmed_results"]:
            st.session_state[k] = []
        st.session_state["tutor_topic"] = ""
        st.session_state["tutor_phase"] = "idle"
        st.session_state["quiz_score"] = [0, 0]
        st.rerun()

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
                    response = chat([{"role":"user","content":f"Analyze these papers on: {query}\n\n{abstracts}"}], system)
                st.session_state["research_messages"] = [
                    {"role":"user","content":f"Search: {query}"},
                    {"role":"assistant","content":response},
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
                st.session_state["research_messages"].append({"role":"user","content":followup})
                history = [{"role":m["role"],"content":m["content"]} for m in st.session_state["research_messages"]]
                with st.spinner("Thinking..."):
                    response = chat(history, system)
                st.session_state["research_messages"].append({"role":"assistant","content":response})
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
                        init = chat([{"role":"user","content":f"Teach me about {topic}"}], system)
                    st.session_state["tutor_messages"] = [{"role":"assistant","content":init,"system":system}]
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
                        init = chat([{"role":"user","content":f"Quiz me on {topic}"}], system)
                    st.session_state["tutor_messages"] = [{"role":"assistant","content":init,"system":system}]
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        topic = st.session_state["tutor_topic"]
        phase = st.session_state["tutor_phase"]
        col1, col2 = st.columns([5,1])
        with col1:
            icon = "📖" if phase == "teaching" else "📝"
            mode_label = "Teaching Session" if phase == "teaching" else "Quiz Mode"
            st.markdown(f'<div style="font-family:Syne,sans-serif;font-weight:700;font-size:1.1rem;color:var(--text);">{icon} {topic} <span style="font-weight:400;color:var(--muted2);font-size:0.85rem;">— {mode_label}</span></div>', unsafe_allow_html=True)
        with col2:
            if st.button("← Back"):
                st.session_state["tutor_phase"] = "idle"
                st.session_state["tutor_messages"] = []
                st.rerun()

        if phase == "quizzing":
            correct, total = st.session_state["quiz_score"]
            pct = int(correct/total*100) if total > 0 else 0
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
                    st.session_state["quiz_score"] = [sc[0], sc[1]+1]
                st.session_state["tutor_messages"].append({"role":"user","content":user_input})
                system = st.session_state["tutor_messages"][0].get("system","You are a medical tutor.")
                history = [{"role":m["role"],"content":m["content"]} for m in st.session_state["tutor_messages"]]
                with st.spinner("..."):
                    response = chat(history, system)
                if phase == "quizzing" and ("✅" in response or "correct" in response.lower()):
                    sc = st.session_state["quiz_score"]
                    st.session_state["quiz_score"] = [sc[0]+1, sc[1]]
                st.session_state["tutor_messages"].append({"role":"assistant","content":response})
                st.rerun()