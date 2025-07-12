import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Tous les résultats", layout="wide")

# Styles CSS pour reproduire le look Excel
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
}

# Table de titre global (en-têtes fusionnés)
header = """
<table>
  <tr>
    <td colspan="2" class="header-blue">Dimensions de l'outil AGROECO</td>
    <td colspan="2" class="header-blue cell-center">Indicateurs</td>
    <td colspan="2" class="header-green cell-center">Scores moyens indicateurs non pondérés par les poids des acteurs</td>
    <td colspan="2" class="header-green cell-center">Score moyen global par dimension non pondérée par les poids des acteurs</td>
  </tr>
</table>
"""
st.markdown(header, unsafe_allow_html=True)

# Boucle d'affichage de chaque indicateur
for indicateur, rows in data.items():
    # Bar de titre pour l'indicateur
    st.markdown(f"""
<table>
  <tr>
    <td colspan="2" class="header-blue"></td>
    <td colspan="4" class="header-blue cell-center">{indicateur}</td>
  </tr>
  <tr>
    <th class="header-green cell-center">N°</th>
    <th class="header-green cell-center">Catégories d’acteurs</th>
    <th class="header-green"></th>
    <th class="header-green cell-center">Score moyen non pondéré</th>
  </tr>
""", unsafe_allow_html=True)

    # Lignes de données
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
    <td class="cell-center">{r['N°']}</td>
    <td>{r['Catégories d’acteurs']}</td>
    <td class="cell-center">{icon}</td>
    <td class="cell-center">{r['Score']:.1f}</td>
  </tr>
"""

    # Clôture du tableau
    st.markdown(rows_html + '</table>', unsafe_allow_html=True)

    # Séparateur
    st.markdown('---')

# Instruction pour exécution
st.markdown("*Cette mise en page reproduit la structure de l'onglet Excel.*")
