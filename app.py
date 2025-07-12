import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Tous les résultats", layout="wide")

# CSS pour le style Excel-like
st.markdown("""
<style>
  table { border-collapse: collapse; width: 100%; margin-bottom: 1rem; }
  td, th { border: 1px solid #ffffff; padding: 4px; }
  .header-blue { background-color: #4F81BD; color: white; font-weight: bold; }
  .header-green { background-color: #C6EFCE; color: black; font-weight: bold; }
  .cell-center { text-align: center; }
</style>
""", unsafe_allow_html=True)

# Données statiques d'exemple
data = {
    "Indicateur 1": [
        {"N°": 1, "Catégories d’acteurs": "Petits exploitants agricoles familiaux", "Score": 1.4},
        {"N°": 2, "Catégories d’acteurs": "Consommateurs", "Score": 1.7},
        {"N°": 3, "Catégories d’acteurs": "Membres ONG", "Score": 2.7},
        {"N°": 4, "Catégories d’acteurs": "Membres OSC", "Score": 2.5},
        {"N°": 5, "Catégories d’acteurs": "Autorités administratives", "Score": 2.0},
        {"N°": 6, "Catégories d’acteurs": "Formation et recherches", "Score": 2.5},
        {"N°": 7, "Catégories d’acteurs": "Acteurs garantie qualité", "Score": 2.5},
    ],
    "Indicateur 2": [
        {"N°": 1, "Catégories d’acteurs": "Petits exploitants agricoles familiaux", "Score": 2.0},
        {"N°": 2, "Catégories d’acteurs": "Consommateurs", "Score": 1.6},
        {"N°": 3, "Catégories d’acteurs": "Membres ONG", "Score": 3.2},
        {"N°": 4, "Catégories d’acteurs": "Membres OSC", "Score": 3.5},
        {"N°": 5, "Catégories d’acteurs": "Autorités administratives", "Score": 3.0},
        {"N°": 6, "Catégories d’acteurs": "Formation et recherches", "Score": 3.0},
        {"N°": 7, "Catégories d’acteurs": "Acteurs garantie qualité", "Score": 3.0},
    ],
    # Ajoutez d'autres indicateurs ici...
}

# Pour chaque indicateur, reproduire le bloc Excel
for indicateur, rows in data.items():
    # Calcul de la moyenne des scores non nuls
    scores = [r['Score'] for r in rows if r['Score'] != 0]
    avg = sum(scores) / len(scores) if scores else 0

    # Construction des lignes de données
    rows_html = ''
    for r in rows:
        # Choix de l'icône selon le score
        if r['Score'] >= 3.0:
            icon = '🟢'
        elif r['Score'] >= 2.0:
            icon = '🟡'
        else:
            icon = '🔴'
        rows_html += f"""
  <tr>
    <td class=\"cell-center\">{r['N°']}</td>
    <td>{r['Catégories d’acteurs']}</td>
    <td class=\"cell-center\">{icon}</td>
    <td class=\"cell-center\">{r['Score']:.1f}</td>
  </tr>
"""

    # Assemblage du bloc complet
    html = f"""
<table>
  <tr>
    <td colspan=\"3\" class=\"header-blue\"></td>
    <td class=\"header-green cell-center\">{avg:.2f}</td>
  </tr>
  <tr>
    <td colspan=\"3\" class=\"header-blue cell-center\">{indicateur}</td>
    <td class=\"header-green\"></td>
  </tr>
  <tr>
    <th class=\"header-green cell-center\">N°</th>
    <th class=\"header-green\">Catégories d’acteurs</th>
    <th class=\"header-green\"></th>
    <th class=\"header-green cell-center\">Score moyen global</th>
  </tr>
{rows_html}</table>
"""

    # Affichage du bloc
    st.markdown(html, unsafe_allow_html=True)
    st.markdown('---')

# Note pour l'utilisateur
st.markdown("*Cette mise en page suit exactement la structure des blocs de l'onglet 'Tous les résultats'.* ")
