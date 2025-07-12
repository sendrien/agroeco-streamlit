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

# ---------- NAVBAR CSS & HTML ----------
st.markdown("""
<style>
.osae-navbar {
    width: 100vw;
    min-height: 70px;
    background: #027368;
    color: #fff;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: stretch;
    box-shadow: 0 2px 20px #02736819;
    padding: 0 0 0 0;
    margin-bottom: 0.6em;
    border-radius: 0 0 18px 18px;
    position: sticky;
    top: 0;
    z-index: 1000;
}
.osae-navbar .osae-title {
    font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
    font-size: 2.0em;
    font-weight: 800;
    letter-spacing: 0.01em;
    color: #fff;
    padding: 0.7em 1.4em 0.7em 1.1em;
    display: flex;
    align-items: center;
    transition: color 0.25s;
    text-shadow: 0 2px 8px #011F2612;
    user-select: none;
    text-decoration: none;
    border-right: 1.8px solid #01726533;
}
.osae-navbar .osae-tabs {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    padding-right: 1.3em;
}
.osae-navbar .osae-tab {
    color: #fff;
    font-size: 1.08em;
    font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
    font-weight: 600;
    padding: 0.7em 1.15em;
    margin-left: 0.15em;
    border: none;
    background: none;
    outline: none;
    cursor: pointer;
    border-radius: 9px 9px 0 0;
    transition: background 0.2s, color 0.19s, box-shadow 0.3s;
    box-shadow: none;
    display: flex;
    align-items: center;
    gap: 0.45em;
    text-decoration: none;
    position: relative;
}
.osae-navbar .osae-tab.active,
.osae-navbar .osae-tab:focus,
.osae-navbar .osae-tab:hover {
    background: #01584e;
    color: #FFD700 !important;
    outline: none;
    box-shadow: 0 2px 16px #FFD70011;
}
@media (max-width: 900px) {
    .osae-navbar { flex-direction: column; min-height: unset; padding: 0 0 0 0;}
    .osae-navbar .osae-title { font-size: 1.2em; padding: 0.6em 0.9em 0.3em 1em; border-right: none; border-bottom: 1.5px solid #01726533; }
    .osae-navbar .osae-tabs { padding: 0.15em 0.6em 0.6em 0.7em; }
    .osae-navbar .osae-tab { font-size: 1em; padding: 0.4em 0.7em; }
}
</style>
""", unsafe_allow_html=True)

# ---------- NAVBAR LOGIQUE ----------
if "navpage" not in st.session_state:
    st.session_state["navpage"] = list(PAGES.keys())[0]

# Navbar HTML (plus accessible, boutons vrais pour focus clavier)
navbar_html = f'''
<nav class="osae-navbar">
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

# Navigation JS (mémorise l'onglet sélectionné)
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

# Gérer le paramètre navpage (pour navigation "persistante" Streamlit)
import urllib.parse
query_string = st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
navpage = st.session_state.get("navpage", list(PAGES.keys())[0])
if "navpage" in query_string:
    navpage_q = urllib.parse.unquote(query_string["navpage"][0])
    if navpage_q in PAGES:
        navpage = navpage_q
        st.session_state["navpage"] = navpage

# Afficher la page sélectionnée
PAGES[navpage]()

# --- Footer (identique, bien visible, optionnel) ---
st.markdown("""
    <div class="footer">
        © 2025 OSAE — Outil Statistique Agro-Economie | Développé par IT STRATEGIX
    </div>
""", unsafe_allow_html=True)
