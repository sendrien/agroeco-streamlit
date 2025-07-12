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

# Navbar CSS
st.markdown("""
<style>
.navbar-osae {
    width: 100vw;
    background: #027368;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    padding: 0 0 0 0.7em;
    margin-bottom: 1.8em;
    position: sticky;
    top: 0;
    z-index: 98;
    box-shadow: 0 2px 20px #02736814;
    height: 60px;
}
.navbar-osae a {
    color: #fff;
    text-decoration: none;
    font-weight: 700;
    font-size: 1.08em;
    letter-spacing: 0.01em;
    padding: 0.3em 1.15em;
    margin-right: 0.5em;
    border-radius: 8px 8px 0 0;
    display: flex;
    align-items: center;
    transition: background 0.25s, color 0.25s;
    height: 60px;
}
.navbar-osae a.active, .navbar-osae a:hover {
    background: #01584e;
    color: #FFD700;
}
@media (max-width: 900px) {
    .navbar-osae { font-size: 1em; height: 52px; }
    .navbar-osae a { padding: 0.1em 0.75em; font-size: 0.97em; }
}
</style>
""", unsafe_allow_html=True)

# Init navigation state
if "navpage" not in st.session_state:
    st.session_state["navpage"] = "Syntèse structurée des résultats"

# Navbar rendering
navbar_html = '<div class="navbar-osae">'
for page in PAGES.keys():
    icon = PAGE_ICONS.get(page, "")
    active = "active" if st.session_state["navpage"] == page else ""
    navbar_html += f'<a href="#" class="{active}" onclick="window.parent.postMessage(\'{page}\', \'*\')">{icon} {page}</a>'
navbar_html += '</div>'
st.markdown(navbar_html, unsafe_allow_html=True)

# JavaScript to update navigation state (hack for Streamlit Cloud & local)
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

# Workaround: read navpage from URL (works on Streamlit Cloud & locally)
import urllib.parse
from urllib.parse import parse_qs

navpage = st.session_state.get("navpage", list(PAGES.keys())[0])
query_string = st.experimental_get_query_params()
if "navpage" in query_string:
    navpage_q = urllib.parse.unquote(query_string["navpage"][0])
    if navpage_q in PAGES:
        navpage = navpage_q
        st.session_state["navpage"] = navpage

# Titre principal
st.markdown(
    "<h1 class='osae-main-title' style='margin-top:0;margin-bottom:0.2em;font-size:2.2rem;color:#034001;'>Outil Statistique Agro-économie (OSAE)</h1>",
    unsafe_allow_html=True,
)

# Affiche la page sélectionnée
PAGES[navpage]()

# Footer (fixe)
st.markdown("""
    <div class="footer">
        © 2025 OSAE — Outil Statistique Agro-Economie | Développé par IT STRATEGIX
    </div>
""", unsafe_allow_html=True)
