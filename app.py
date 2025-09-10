import streamlit as st
from page_resultats import show_page_resultats
from page_resume import show_page_resume
from page_graphiques import show_page_graphiques

# --- Ingestion KoBo ---
import requests
import pandas as pd
import streamlit.components.v1 as components

# ⚠️ Configurer la page AVANT tout rendu
st.set_page_config(
    page_title="Outil Statistique Agro-Economie (OSAE)",
    page_icon="📊",
    layout="wide"
)

# --- Masquage GitHub/Fork & "Hosted with Streamlit" (CSS + JS robuste) ---
st.markdown("""
<style>
/* ===================== Design System (CSS variables) ===================== */
:root{
  --primary:#027368;        /* Teal OSAE */
  --primary-700:#015e55;
  --accent:#00A389;
  --bg:#F7FAF9;
  --card:#FFFFFF;
  --text:#0F172A;
  --muted:#5C7373;
  --radius:14px;
  --shadow:0 8px 28px rgba(2,115,104,.08);
}

/* ===================== Reset & Layout ===================== */
html, body, .stApp { background: var(--bg) !important; color: var(--text); }
.block-container{ padding-top: 0.6rem; padding-bottom: 5.2rem; max-width: 1280px; }

/* Focus accessible */
*:focus-visible { outline: 3px solid var(--accent) !important; outline-offset: 2px !important; border-radius: 6px; }

/* ===================== Header Streamlit cleanup ===================== */
header [data-testid="stHeaderActionElements"] { display: none !important; }
div[data-testid="stToolbar"]{ display:none !important; }
.stApp [data-testid="stStatusWidget"]{ display:none !important; }
.stApp .viewerBadge_container__1QSob, .stApp .viewerBadge_link__qYCB_{ display:none !important; }
footer, #MainMenu{ visibility:hidden !important; }
.stApp [data-testid="stDecoration"]{ display:none !important; }

/* ===================== Topbar de l'app ===================== */
.app-topbar{
  position: sticky; top: 0; z-index: 20;
  background: linear-gradient( to right, #ffffff 0%, #ffffff 40%, #f1fbf8 100% );
  border-bottom: 1px solid #e8f2ef;
  padding: 10px 18px 8px 18px; margin: 0 -16px 14px -16px;
}
.app-topbar .brand{ display:flex; gap:14px; align-items:center; }
.app-topbar .logo{
  display:inline-flex; align-items:center; justify-content:center;
  width:40px; height:40px; border-radius:12px;
  background: var(--primary); color:#fff; font-weight:800; letter-spacing:.5px;
  box-shadow: var(--shadow);
}
.app-topbar h1{
  font-size: 1.35rem; line-height:1.2; margin:0; color:#0d2a27;
}
.app-topbar p{
  margin:2px 0 0 0; font-size:.92rem; color:var(--muted);
}

/* ===================== Sidebar ===================== */
section[data-testid="stSidebar"] { background: #FFFFFF; border-right:1px solid #eef4f3; }
.sidebar-card{
  background:#fff; border:1px solid #e7f0ee; border-radius: var(--radius);
  padding: 14px 12px; box-shadow: var(--shadow); margin-top:6px;
}
.stTextInput>div>div>input{
  border:1.6px solid #d8ebe7 !important; border-radius:10px !important; background:#fff !important;
}
.stTextInput>div>div>input:focus{ border-color: var(--primary) !important; }
.stButton>button{
  background: var(--primary); color:#fff; border:0; border-radius:10px;
  padding: 8px 14px; font-weight:600; box-shadow: var(--shadow);
}
.stButton>button:hover{ background: var(--primary-700); transform: translateY(-1px); }
.stButton>button:active{ transform: translateY(0); }

/* ===================== Tabs stylés ===================== */
.stTabs [role="tablist"]{ gap: 6px; border-bottom: 1px solid #e6f1ef; padding-bottom: 4px; }
.stTabs [role="tab"]{
  border:1px solid transparent; padding:10px 14px; border-radius:12px 12px 0 0;
  color:#305a56; background:#f3fbf9; font-weight:600;
}
.stTabs [aria-selected="true"]{
  background:#ffffff; border-color:#e6f1ef; color:#093a36;
  box-shadow: 0 -2px 0 0 var(--primary) inset;
}

/* ===================== Cards & titres ===================== */
.card{
  background: var(--card); border:1px solid #e7f0ee; border-radius: var(--radius);
  padding: 14px; box-shadow: var(--shadow);
}
.h-section{
  display:flex; align-items:center; gap:10px; margin:16px 0 8px 0;
}
.h-section .pill{
  width:8px; height:24px; border-radius:99px; background: var(--primary);
}
.h-section h2{ margin:0; font-size:1.15rem; color:#0d2a27; }

/* ===================== Tables/Expanders (votre style conservé, raffiné) ===================== */
.justify-table th, .justify-table td {
    text-align: justify !important; text-justify: inter-word !important; white-space: pre-line !important;
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif; font-size: 1.06em; padding: 9px 16px !important; color: #032612;
}
.justify-table th { background: var(--primary) !important; color: #fff; font-size: 0.82em; }
.justify-table tr:hover td { background: #eaf6f3 !important; color: #032612 !important; transition: background 0.22s; }
.justify-table { width: 100% !important; border-collapse: separate !important; border-spacing: 0 !important; border-radius: 12px !important; box-shadow: var(--shadow); margin-bottom: 1.1em; background: transparent; }
hr { border: 1.8px solid var(--primary) !important; opacity: 0.7; }
[data-testid="stExpander"] { background: #F4F7F6 !important; border-radius: 13px !important; margin-bottom: 14px !important; box-shadow: 0 2px 16px #02736815; }
[data-testid="stExpander"] > div, [data-testid="stExpander"] > details { background: white !important; border-radius: 4px !important; }

/* Score chip */
.score-global-acc{
  background: var(--primary); border-radius: 10px; color:#fff;
  display:flex; flex-direction:column; align-items:center; gap:6px;
  padding: 10px 16px; max-width: 360px; border: 1.2px solid #034001; box-shadow: var(--shadow);
}
.score-global-label-acc{ font-size:1.04em; font-weight:600; }
.score-global-value-acc{ font-size:2em; font-weight:800; color:#fffae6; }

/* Footer custom */
.footer {
  position: fixed; left: 0; bottom: 0; width: 100vw; background: var(--primary); color: white;
  text-align: center; padding: 10px 0 7px 0; font-size: .98rem; box-shadow: 0 -1px 6px #02736822; z-index: 100;
}
@media (max-width: 700px) { .footer { font-size: .92rem; padding: 8px 0 5px 0; } }
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
    selectors.forEach(sel => document.querySelectorAll(sel).forEach(el => el.style.display = 'none'));
    document.querySelectorAll('div,section,span,a,button').forEach(el=>{
      const t=(el.innerText||'').trim(); if(/Hosted with Streamlit/i.test(t)||/^Fork$/i.test(t)){ el.style.display='none'; }
    });
  }
  hideAll();
  new MutationObserver(hideAll).observe(document.documentElement,{childList:true,subtree:true});
})();
</script>
""", height=0)

# --- Topbar & titre
st.markdown("""
<div class="app-topbar">
  <div class="brand">
    <div class="logo">OS</div>
    <div>
      <h1>Outil Agro Eco</h1>
      <p>Tableau de bord agro-écologie · KoBo ↔ analyses ↔ visualisations</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# --- Onglets principaux
tab1, tab2, tab3 = st.tabs(["📋 Synthèse structurée des résultats", "📝 Résumé", "📊 Graphiques"])

with tab1:
    st.markdown('<div class="h-section"><span class="pill"></span><h2>Synthèse détaillée</h2></div>', unsafe_allow_html=True)
    show_page_resultats()

with tab2:
    st.markdown('<div class="h-section"><span class="pill"></span><h2>Tableaux récapitulatifs</h2></div>', unsafe_allow_html=True)
    show_page_resume()

with tab3:
    st.markdown('<div class="h-section"><span class="pill"></span><h2>Visualisations interactives</h2></div>', unsafe_allow_html=True)
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

# --- Sidebar / KoBo ---
with st.sidebar:
    st.markdown("### Données KoBo")
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    asset_uid = st.text_input("Asset UID", value="", placeholder="aBCDeFg123...")
    col_a, col_b = st.columns([1,1])
    with col_a:
        if st.button("🔄 Rafraîchir KoBo"):
            fetch_kobo.clear()  # vide le cache
    with col_b:
        st.write("")  # espace réservé à d’autres actions si besoin
    st.markdown("</div>", unsafe_allow_html=True)

df_kobo = None
if asset_uid:
    with st.spinner("Récupération des données KoBo…"):
        df_kobo = fetch_kobo(asset_uid)

# --- Footer personnalisé ---
st.markdown("""
    <div class="footer">
        © 2025 OSAE — Outil Statistique Agro-Economie · Design accessible et réactif
    </div>
""", unsafe_allow_html=True)
