import streamlit as st
from page_resultats import show_page_resultats
from page_resume import show_page_resume
from page_graphiques import show_page_graphiques

st.set_page_config(page_title="Outil Statistique Agro-Economie (OSAE)", layout="wide")

PAGES = {
    "Syntèse structurée des résultats": show_page_resultats,
    "Résumé": show_page_resume,
    "Graphiques": show_page_graphiques,
}
PAGE_ICONS = {
    "Syntèse structurée des résultats": "📋",
    "Résumé": "📝",
    "Graphiques": "📊",
}

# NAVBAR CSS & HTML moderne, sans padding/marge extérieure
st.markdown("""
<style>
body, .stApp { background: #F6F8F7 !important; padding: 0 !important; }
.osae-navbar {
    width: 100vw;
    height: 74px;
    background: #027368;
    color: #fff;
    display: flex;
    justify-content: space-between;
    align-items: stretch;
    box-shadow: 0 3px 16px #02736821;
    padding: 0 0.7em 0 0.3em;
    margin: 0 0 1.2em 0;
    border-radius: 0;
    position: fixed;
    left: 0; top: 0;
    z-index: 999;
}
.osae-navbar .osae-title {
    font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
    font-size: 2.05em;
    font-weight: 800;
    color: #fff;
    padding: 0 1.2em;
    display: flex;
    align-items: center;
    text-shadow: 0 2px 8px #011F2612;
    user-select: none;
    text-decoration: none;
    border-right: 2px solid #01938355;
    letter-spacing: 0.01em;
}
.osae-navbar .osae-tabs {
    display: flex;
    align-items: center;
    gap: 0.2em;
    padding-right: 1.2em;
    height: 100%;
}
.osae-navbar .osae-tab {
    color: #fff;
    font-size: 1.08em;
    font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
    font-weight: 600;
    padding: 0 1.25em;
    margin-left: 0.25em;
    border: none;
    background: none;
    outline: none;
    cursor: pointer;
    border-radius: 0 0 7px 7px;
    display: flex;
    align-items: center;
    gap: 0.45em;
    height: 74px;
    box-shadow: none;
    text-decoration: none;
    position: relative;
    transition: background 0.2s, color 0.16s, box-shadow 0.3s;
}
.osae-navbar .osae-tab.active,
.osae-navbar .osae-tab:focus,
.osae-navbar .osae-tab:hover {
    background: #016055;
    color: #FFD700 !important;
    outline: none;
    box-shadow: 0 5px 16px #FFD7000A;
}
@media (max-width: 900px) {
    .osae-navbar { flex-direction: column; height: unset; }
    .osae-navbar .osae-title { font-size: 1.13em; padding: 0.45em 0.7em 0.2em 0.9em; border-right: none; border-bottom: 1.5px solid #01938355;}
    .osae-navbar .osae-tabs { padding: 0.1em 0.2em 0.5em 0.6em; }
    .osae-navbar .osae-tab { font-size: 0.98em; height: 46px; padding: 0 0.7em;}
}
.stApp { padding-top: 88px !important; }
</style>
""", unsafe_allow_html=True)

if "navpage" not in st.session_state:
    st.session_state["navpage"] = list(PAGES.keys())[0]

navbar_html = f'''
<nav class="osae-navbar" role="navigation" aria-label="Navigation principale">
    <div class="osae-title" tabindex="0">
        Outil Statistique Agro-économie (OSAE)
    </div>
    <div class="osae-tabs">
'''

for page in PAGES.keys():
    icon = PAGE_ICONS.get(page, "")
    active = "active" if st.session_state["navpage"] == page else ""
    navbar_html += (
        f'<button class="osae-tab {active}" tabindex="0" '
        f'onclick="window.parent.postMessage(\'{page}\', \'*\')">'
        f'{icon}&nbsp;{page}</button>'
    )
navbar_html += '</div></nav>'
st.markdown(navbar_html, unsafe_allow_html=True)

# JS navigation persistante
st.markdown("""
<script>
window.addEventListener('message', (event) => {
    if (event.data && typeof event.data === "string") {
        window.location.search = '?navpage=' + encodeURIComponent(event.data)
    }
});
window.onload = () => {
    const params = new URLSearchParams(window.location.search);
    const p = params.get('navpage');
    if(p) {
        window.parent.postMessage(p, '*');
    }
}
</script>
""", unsafe_allow_html=True)

import urllib.parse
query_string = st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
navpage = st.session_state.get("navpage", list(PAGES.keys())[0])
if "navpage" in query_string:
    navpage_q = urllib.parse.unquote(query_string["navpage"][0])
    if navpage_q in PAGES:
        navpage = navpage_q
        st.session_state["navpage"] = navpage

# --- Affiche la page courante ---
PAGES[navpage]()

# --- Footer ---
st.markdown("""
    <div class="footer" style="background:#027368;color:#fff;font-size:1rem;font-family:Segoe UI,Roboto,Arial,sans-serif;text-align:center;letter-spacing:0.01em;padding:13px 0 10px 0;margin:0;box-shadow:0 -2px 12px #02736833;">
        © 2025 OSAE — Outil Statistique Agro-Economie | Développé par IT STRATEGIX
    </div>
""", unsafe_allow_html=True)
