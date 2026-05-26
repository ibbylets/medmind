import streamlit as st
from groq import Groq
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MedMind",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg:        #0d1117;
    --surface:   #161b22;
    --border:    #21262d;
    --accent:    #58a6ff;
    --accent2:   #3fb950;
    --muted:     #8b949e;
    --text:      #e6edf3;
    --danger:    #f85149;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--surface);
    border-right: 1px solid var(--border);
}

/* Cards */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.card-accent {
    border-left: 3px solid var(--accent);
}

.card-green {
    border-left: 3px solid var(--accent2);
}

/* Mode badge */
.mode-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-family: 'DM Mono', monospace;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.badge-research { background: #1f3a5f; color: var(--accent); border: 1px solid #2d5a8e; }
.badge-tutor    { background: #1a3a2a; color: var(--accent2); border: 1px solid #2d6b3e; }

/* Headings */
h1, h2, h3 { font-family: 'DM Serif Display', serif; }

.app-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    letter-spacing: -0.02em;
    color: var(--text);
    margin: 0;
}

.app-sub {
    font-size: 0.8rem;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Chat bubbles */
.bubble-user {
    background: #1f3a5f;
    border: 1px solid #2d5a8e;
    border-radius: 12px 12px 2px 12px;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0;
    max-width: 80%;
    margin-left: auto;
}

.bubble-ai {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px 12px 12px 2px;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0;
    max-width: 90%;
}

/* Research result sections */
.section-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    margin-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.25rem;
}

/* Buttons */
.stButton > button {
    background: var(--accent) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    padding: 0.4rem 1.2rem !important;
    transition: opacity 0.2s !important;
}

.stButton > button:hover { opacity: 0.85 !important; }

/* Text inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Select box */
.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* Spinner */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* Divider */
hr { border-color: var(--border) !important; }

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Groq client ───────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    api_key = st.session_state.get("api_key") or os.getenv("GROQ_API_KEY", "")
    if api_key:
        return Groq(api_key=api_key)
    return None

def chat(messages: list[dict], system: str, stream: bool = True):
    client = get_client()
    if not client:
        st.error("No API key. Add it in the sidebar.")
        return ""
    all_messages = [{"role": "system", "content": system}] + messages
    if stream:
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=all_messages,
                temperature=0.7,
                max_tokens=2048,
                stream=True,
            )
        return response
    else:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=all_messages,
            temperature=0.6,
            max_tokens=2048,
        )
        return response.choices[0].message.content

# ── PubMed helper ─────────────────────────────────────────────────────────────
def search_pubmed(query: str, max_results: int = 5) -> list[dict]:
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    try:
        # Step 1: get IDs
        search_url = f"{base}esearch.fcgi?db=pubmed&term={requests.utils.quote(query)}&retmax={max_results}&retmode=json&sort=relevance"
        ids = requests.get(search_url, timeout=8).json()["esearchresult"]["idlist"]
        if not ids:
            return []

        # Step 2: fetch abstracts in XML-style summary
        fetch_url = f"{base}esummary.fcgi?db=pubmed&id={','.join(ids)}&retmode=json"
        data = requests.get(fetch_url, timeout=10).json()
        result = data.get("result", {})

        articles = []
        for uid in ids:
            paper = result.get(uid, {})
            title = paper.get("title", "No title")
            year = paper.get("pubdate", "n.d.")[:4]
            authors = ", ".join([a["name"] for a in paper.get("authors", [])[:3]])

            # Step 3: fetch abstract separately
            abs_url = f"{base}efetch.fcgi?db=pubmed&id={uid}&rettype=abstract&retmode=text"
            abstract = requests.get(abs_url, timeout=8).text.strip()
            abstract = abstract[:1500] if abstract else "No abstract available."

            articles.append({"pmid": uid, "title": title, "abstract": abstract, "year": year, "authors": authors})

        return articles
    except Exception as e:
        st.warning(f"PubMed error: {e}")
        return []

# ── Session state init ────────────────────────────────────────────────────────
for key, default in {
    "mode": "Research Companion",
    "research_messages": [],
    "tutor_messages": [],
    "tutor_topic": "",
    "tutor_phase": "idle",  # idle | teaching | quizzing
    "quiz_score": [0, 0],
    "pubmed_results": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="app-title">MedMind</p>', unsafe_allow_html=True)
    st.markdown('<p class="app-sub">AI Medical Intelligence</p>', unsafe_allow_html=True)
    st.markdown("---")

    api_key_input = st.text_input("Groq API Key", type="password", placeholder="gsk_...", value=os.getenv("GROQ_API_KEY", ""))
    if api_key_input:
        st.session_state["api_key"] = api_key_input

    st.markdown("---")
    mode = st.radio("Mode", ["🔬 Research Companion", "🎓 Medical Tutor"], label_visibility="collapsed")
    st.session_state["mode"] = mode

    st.markdown("---")
    st.markdown('<p style="font-size:0.75rem; color: var(--muted); font-family: DM Mono, monospace;">Model: llama-3.3-70b-versatile</p>', unsafe_allow_html=True)

    if st.button("🗑 Clear session"):
        st.session_state["research_messages"] = []
        st.session_state["tutor_messages"] = []
        st.session_state["tutor_topic"] = ""
        st.session_state["tutor_phase"] = "idle"
        st.session_state["quiz_score"] = [0, 0]
        st.session_state["pubmed_results"] = []
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  MODE 1 — RESEARCH COMPANION
# ══════════════════════════════════════════════════════════════════════════════
if "Research" in st.session_state["mode"]:
    st.markdown('<span class="mode-badge badge-research">🔬 Research Companion</span>', unsafe_allow_html=True)
    st.markdown("## Research a Medical Topic")
    st.markdown("Search PubMed for real papers, then have an in-depth AI conversation about the findings.")

    col1, col2 = st.columns([3, 1])
    with col1:
        research_query = st.text_input("Search query", placeholder="e.g. GLP-1 agonists type 2 diabetes cardiovascular outcomes")
    with col2:
        n_results = st.selectbox("Papers", [3, 5, 8], index=1)

    if st.button("Search PubMed →"):
        if research_query:
            with st.spinner("Searching PubMed..."):
                results = search_pubmed(research_query, n_results)
                st.session_state["pubmed_results"] = results
                st.session_state["research_messages"] = []

            if results:
                # Auto-summarize with AI
                abstracts_text = "\n\n".join([
                    f"[{i+1}] {r['title']} ({r['year']})\n{r['abstract']}"
                    for i, r in enumerate(results)
                ])
                system = """You are a medical research expert. You will be given PubMed abstracts.
                Your job:
                1. Give a concise overview of what these papers collectively show
                2. Highlight key findings and consensus
                3. Identify research gaps or conflicting results
                4. Suggest 3 follow-up research questions
                Be precise, cite paper numbers [1], [2] etc. Use markdown formatting."""

                init_msg = [{"role": "user", "content": f"Summarize and analyze these papers about: {research_query}\n\n{abstracts_text}"}]
                response = chat(init_msg, system, stream=False)
                st.session_state["research_messages"] = [
                    {"role": "user", "content": f"Search: {research_query}"},
                    {"role": "assistant", "content": response},
                ]

    # Show papers
    if st.session_state["pubmed_results"]:
        with st.expander(f"📄 {len(st.session_state['pubmed_results'])} papers found", expanded=False):
            for i, paper in enumerate(st.session_state["pubmed_results"]):
                st.markdown(f"""
                <div class="card">
                    <div class="section-title">Paper {i+1} · PMID {paper['pmid']} · {paper['year']}</div>
                    <strong>{paper['title']}</strong>
                    <p style="font-size:0.85rem; color: var(--muted); margin-top:0.5rem;">{paper['abstract'][:400]}...</p>
                    <a href="https://pubmed.ncbi.nlm.nih.gov/{paper['pmid']}/" target="_blank" style="color: var(--accent); font-size:0.8rem;">View on PubMed →</a>
                </div>
                """, unsafe_allow_html=True)

    # Chat history
    for msg in st.session_state["research_messages"]:
        if msg["role"] == "user":
            st.markdown(f'<div class="bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bubble-ai">{msg["content"]}</div>', unsafe_allow_html=True)

    # Follow-up chat
    if st.session_state["research_messages"]:
        st.markdown("---")
        follow_up = st.text_input("Ask a follow-up question about these papers...", key="research_followup")
        if st.button("Ask →", key="research_ask"):
            if follow_up:
                abstracts_text = "\n\n".join([
                    f"[{i+1}] {r['title']} ({r['year']})\n{r['abstract']}"
                    for i, r in enumerate(st.session_state["pubmed_results"])
                ])
                system = f"""You are a medical research expert. The user has searched PubMed for papers.
                Here are the papers in context:\n\n{abstracts_text}\n\n
                Answer questions precisely, cite paper numbers [1][2] etc., and be evidence-based."""

                st.session_state["research_messages"].append({"role": "user", "content": follow_up})
                history = [m for m in st.session_state["research_messages"] if m["role"] in ["user", "assistant"]]
                response = chat(history, system, stream=False)
                st.session_state["research_messages"].append({"role": "assistant", "content": response})
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  MODE 2 — MEDICAL TUTOR
# ══════════════════════════════════════════════════════════════════════════════
elif "Tutor" in st.session_state["mode"]:
    st.markdown('<span class="mode-badge badge-tutor">🎓 Medical Tutor</span>', unsafe_allow_html=True)
    st.markdown("## Medical Tutor")
    st.markdown("Learn any medical topic through Socratic dialogue, then test yourself with board-style questions.")

    # Topic picker
    if st.session_state["tutor_phase"] == "idle":
        st.markdown('<div class="card card-green">', unsafe_allow_html=True)
        topic = st.text_input("What do you want to learn?", placeholder="e.g. Diabetic ketoacidosis, Acute MI, Pharmacokinetics...")
        level = st.selectbox("Your level", ["Medical student (Year 1-2)", "Medical student (Year 3-4)", "Resident", "Attending / Review"])

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 Start Teaching Session"):
                if topic:
                    st.session_state["tutor_topic"] = topic
                    st.session_state["tutor_phase"] = "teaching"
                    system = f"""You are an expert medical educator using the Socratic method.
                    Topic: {topic}. Student level: {level}.
                    
                    Start with a brief engaging overview (2-3 sentences), then ask ONE probing question to assess baseline knowledge.
                    Keep responses focused and conversational. Use clinical examples.
                    Don't overwhelm — teach one concept at a time, asking questions to check understanding before moving on.
                    Format key terms in **bold**."""

                    init = chat([{"role": "user", "content": f"Teach me about {topic}"}], system, stream=False)
                    st.session_state["tutor_messages"] = [{"role": "assistant", "content": init, "system": system, "level": level}]
                    st.rerun()

        with col2:
            if st.button("📝 Jump to Quiz"):
                if topic:
                    st.session_state["tutor_topic"] = topic
                    st.session_state["tutor_phase"] = "quizzing"
                    st.session_state["quiz_score"] = [0, 0]
                    system = f"""You are a medical board exam question generator.
                    Topic: {topic}. Level: {level}.
                    Generate ONE USMLE-style question at a time in this exact format:

                    **Question:** [clinical vignette or direct question]
                    
                    **A)** [option]
                    **B)** [option]
                    **C)** [option]
                    **D)** [option]
                    **E)** [option]

                    Wait for the user's answer before revealing the correct answer and explanation.
                    When they answer, give: ✅ or ❌, the correct answer, and a clear explanation.
                    Then generate the next question."""

                    init = chat([{"role": "user", "content": f"Quiz me on {topic}"}], system, stream=False)
                    st.session_state["tutor_messages"] = [{"role": "assistant", "content": init, "system": system, "level": level}]
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Active session
    else:
        topic = st.session_state["tutor_topic"]
        phase = st.session_state["tutor_phase"]

        col1, col2 = st.columns([4, 1])
        with col1:
            icon = "📖" if phase == "teaching" else "📝"
            st.markdown(f"**{icon} {topic}** — {'Teaching Session' if phase == 'teaching' else 'Quiz Mode'}")
        with col2:
            if st.button("← Back"):
                st.session_state["tutor_phase"] = "idle"
                st.session_state["tutor_messages"] = []
                st.rerun()

        if phase == "quizzing":
            score = st.session_state["quiz_score"]
            correct, total = score
            pct = int(correct / total * 100) if total > 0 else 0
            st.markdown(f'<div class="card" style="padding:0.75rem 1rem;">'
                       f'<span style="font-family: DM Mono, monospace; font-size:0.8rem; color: var(--muted);">Score: </span>'
                       f'<span style="font-weight:600; color: var(--accent2);">{correct}/{total}</span>'
                       f'<span style="font-family: DM Mono, monospace; font-size:0.75rem; color: var(--muted);"> ({pct}%)</span>'
                       f'</div>', unsafe_allow_html=True)

        # Message history
        for msg in st.session_state["tutor_messages"]:
            if msg["role"] == "user":
                st.markdown(f'<div class="bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bubble-ai">{msg["content"]}</div>', unsafe_allow_html=True)

        # Input
        placeholder = "Your answer..." if phase == "quizzing" else "Your response..."
        user_input = st.text_input("", placeholder=placeholder, key="tutor_input")

        if st.button("Send →", key="tutor_send"):
            if user_input:
                # Track quiz score
                if phase == "quizzing":
                    score = st.session_state["quiz_score"]
                    st.session_state["quiz_score"] = [score[0], score[1] + 1]

                st.session_state["tutor_messages"].append({"role": "user", "content": user_input})

                system = st.session_state["tutor_messages"][0].get("system", "You are a medical tutor.")
                history = [{"role": m["role"], "content": m["content"]} for m in st.session_state["tutor_messages"]]
                response = chat(history, system, stream=False)

                # Check for correct answer in quiz
                if phase == "quizzing" and ("✅" in response or "correct" in response.lower()):
                    score = st.session_state["quiz_score"]
                    st.session_state["quiz_score"] = [score[0] + 1, score[1]]

                st.session_state["tutor_messages"].append({"role": "assistant", "content": response})
                st.rerun()
