import streamlit as st
from page_resultats import show_page_resultats
from page_resume import show_page_resume
from page_graphiques import show_page_graphiques

st.set_page_config(page_title="Outil Statistique Agro-Economie (OSAE)", layout="wide")

# Onglets principaux
tab1, tab2, tab3 = st.tabs(["📋 Syntèse structurée des résultats", "📝 Résumé", "📊 Graphiques"])

with tab1:
    show_page_resultats()

with tab2:
    show_page_resume()

with tab3:
    show_page_graphiques()
