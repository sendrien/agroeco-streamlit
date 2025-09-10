import streamlit as st
from page_resultats import show_page_resultats
from page_resume import show_page_resume
from page_graphiques import show_page_graphiques

# --- Ingestion KoBo ---
import requests
import pandas as pd
import streamlit.components.v1 as components

# ⚠️ Configurer la page AVANT tout rendu
st.set_page_config(page_title="Outil Statistique Agro-Economie (OSAE)", layout="wide")

# --- Masquage GitHub/Fork & "Hosted with Streamlit" (CSS + JS robuste) ---
st.markdown("""
<style>
/* Icônes d’action du header (Fork / GitHub / Share…) */
header [data-testid="stHeaderActionElements"] { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }  /* compat */

/* Badge/Widget en bas à droite ("Hosted with Streamlit", avatar, etc.) */
.stApp [data-testid="stStatusWidget"] { display: none !important; }

/* Anciennes classes (compatibilité versions) */
.stApp .viewerBadge_container__1QSob { display: none !important; }
.stApp .viewerBadge_link__qYCB_      { display: none !important; }

/* Footer et menu par défaut Streamlit */
footer { visibility: hidden !important; }
#MainMenu { visibility: hidden !important; }

/* Filets/décorations éventuels */
.stApp [data-testid="stDecoration"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# JS : retire les éléments même s’ils sont ré-injectés plus tard (MutationObserver)
components.html("""
<script>
(function(){
  function hideAll(){
    const selectors = [
      'header [data-testid="stHeaderActionElements"]',
      'div[data-testid="stToolbar"]',
      'div[data-testid="stStatusWidget"]',
      '.viewerBadge_container__1QSob',
      '.viewerBadge_link__qYCB_',
      'a[aria-label="View source on GitHub"]',
      'button[title="Fork"]'
    ];
    selectors.forEach(sel => {
      document.querySelectorAll(sel).forEach(el => el.style.display = 'none');
    });
    // Masquer tout élément texte résiduel "Hosted with Streamlit" / "Fork"
    const textHiders = document.querySelectorAll('div,section,span,a,button');
    textHiders.forEach(el => {
      const t = (el.innerText || '').trim();
      if (/Hosted with Streamlit/i.test(t) || /^Fork$/i.test(t)) {
        el.style.display = 'none';
      }
    });
  }
  hideAll();
  const obs = new MutationObserver(hideAll);
  obs.observe(document.documentElement, {childList:true, subtree:true});
})();
</script>
""", height=0)

# --- Styles globaux de l'app ---
st.markdown("""
    <style>
    html, body, .stApp { background: #fff !important; }
    .justify-table th, .justify-table td {
        text-align: justify !important;
        text-justify: inter-word !important;
        white-space: pre-line !important;
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        font-size: 1.08em;
        padding: 9px 16px !important;
        color: #032612;
        transition: background 0.5s;
    }
    .justify-table th {
        background: #027368 !important;
        color: #fff;
        font-size: 0.8em;
    }
    .justify-table tr:hover td {
        background: #d7ece9 !important;
        color: #032612 !important;
        transition: background 0.22s;
    }
    .justify-table {
        width: 100% !important;
        border-collapse: separate !important;
        border-spacing: 0 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 18px #5C737322;
        margin-bottom: 1.1em;
        background: transparent;
        transition: box-shadow 0.5s;
    }
    hr {
        border: 1.8px solid #027368 !important;
        opacity: 0.7;
        transition: border 0.5s;
    }
    [data-testid="stExpander"] > div > div {
        color: #011F26 !important;
        font-size: 1.28em !important;
        font-weight: 700 !important;
        transition: color 0.18s, text-decoration 0.18s;
        cursor: pointer !important;
    }
    [data-testid="stExpander"]:hover > div > div {
        color: #027368 !important;
        font-weight: 800 !important;
        text-decoration: underline !important;
        cursor: pointer !important;
    }
    [data-testid="stExpander"] {
        background: #F4F7F6 !important;
        border-radius: 13px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 2px 16px #02736815;
        transition: background 0.5s, box-shadow 0.5s;
    }
    [data-testid="stExpander"] > div, [data-testid="stExpander"] > details {
        background: white !important;
        border-radius: 4px !important;
    }
    .score-global-acc {
        background: #027368;
        border-radius: 4px;
        box-shadow: 0 2px 12px #02736822;
        padding: 0.2em 1.1em 0.2em 1.1em;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 1.2em;
        margin-top: 0.4em;
        max-width: 355px;
        border: 1.2px solid #034001;
        transition: box-shadow 0.5s, background 0.5s;
    }
    .score-global-label-acc {
        color: #fff;
        font-size: 1.13em;
        font-weight: 600;
        text-align: center;
        transition: color 0.4s;
    }
    .score-global-value-acc {
        font-size: 2.12em;
        color: #FFD;
        font-weight: bold;
        text-align: center;
        margin-top: 0.22em;
        margin-bottom: 0.3em;
        transition: color 0.4s;
    }
    .indicator-title-acc {
        font-size: 1.13em;
        color: #027368;
        font-weight: 700;
        margin-top: 1.2em;
        margin-bottom: 0.35em;
        transition: color 0.4s;
    }
    .ind-separator-acc {
        border: none;
        height: 3px;
        background: #027368;
        margin: 1.15em 0 0.7em 0;
        border-radius: 8px;
        opacity: 0.8;
        transition: background 0.5s;
    }
    </style>
""", unsafe_allow_html=True)

# --- Titre
st.markdown("<h1 class='osae-main-title'>Outil Agro Eco</h1>", unsafe_allow_html=True)

# --- Onglets principaux
tab1, tab2, tab3 = st.tabs(["📋 Syntèse structurée des résultats", "📝 Résumé", "📊 Graphiques"])

with tab1:
    show_page_resultats()

with tab2:
    show_page_resume()

with tab3:
    show_page_graphiques()

# --- KoBo fetch (cache 1h) ---
@st.cache_data(ttl=3600)
def fetch_kobo(asset_uid: str, base_url: str = None) -> pd.DataFrame:
    token = st.secrets["KOBO_TOKEN"]
    base = base_url or st.secrets.get("KOBO_API_BASE", "https://kf.kobotoolbox.org")
    url = f"{base}/api/v2/assets/{asset_uid}/data/?format=json"
    r = requests.get(url, headers={"Authorization": f"Token {token}"}, timeout=60)
    r.raise_for_status()
    payload = r.json().get("results", [])
    return pd.json_normalize(payload)

with st.sidebar:
    st.subheader("Données KoBo")
    asset_uid = st.text_input("Asset UID", value="", placeholder="aBCDeFg123...")
    if st.button("🔄 Rafraîchir KoBo"):
        fetch_kobo.clear()  # vide le cache

df_kobo = None
if asset_uid:
    df_kobo = fetch_kobo(asset_uid)

# --- Footer personnalisé ---
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100vw;
        background: #027368;
        color: white;
        text-align: center;
        padding: 10px 0 7px 0;
        font-size: 1rem;
        box-shadow: 0 -1px 6px #02736822;
        z-index: 100;
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    }
    @media (max-width: 700px) {
        .footer { font-size: 0.93rem; padding: 8px 0 5px 0; }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="footer">
        © 2025 OSAE — Outil Statistique Agro-Economie | Développé par votre équipe
    </div>
""", unsafe_allow_html=True)
