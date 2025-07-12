import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tableau AGROECO", layout="wide")
st.title("Tableau synthétique – Indicateurs AGROECO")

# Données statiques inspirées de ta structure
indicateurs = [
    {
        "dimension": "Dimension environnementale",
        "indicateur": "Indicateur 1 : Accès à l’eau",
        "categories": [
            {"N°": 1, "Catégorie d'acteurs": "Petits exploitants agricoles familiaux", "Score moyen": 1.44},
            {"N°": 2, "Catégorie d'acteurs": "Consommateurs", "Score moyen": 1.70},
            {"N°": 3, "Catégorie d'acteurs": "ONG", "Score moyen": 2.70},
            {"N°": 4, "Catégorie d'acteurs": "Société civile", "Score moyen": 2.50},
            {"N°": 5, "Catégorie d'acteurs": "Autorités administratives", "Score moyen": 2.00},
            {"N°": 6, "Catégorie d'acteurs": "Structures de formation/recherche", "Score moyen": 2.50},
            {"N°": 7, "Catégorie d'acteurs": "Systèmes de garantie qualité", "Score moyen": 2.30},
        ],
        "score_global": 2.23
    },
    {
        "dimension": "Dimension environnementale",
        "indicateur": "Indicateur 2 : Conservation des sols",
        "categories": [
            {"N°": 1, "Catégorie d'acteurs": "Petits exploitants agricoles familiaux", "Score moyen": 2.00},
            {"N°": 2, "Catégorie d'acteurs": "Consommateurs", "Score moyen": 1.60},
            {"N°": 3, "Catégorie d'acteurs": "ONG", "Score moyen": 3.20},
            {"N°": 4, "Catégorie d'acteurs": "Société civile", "Score moyen": 2.70},
            {"N°": 5, "Catégorie d'acteurs": "Autorités administratives", "Score moyen": 2.40},
            {"N°": 6, "Catégorie d'acteurs": "Structures de formation/recherche", "Score moyen": 2.80},
            {"N°": 7, "Catégorie d'acteurs": "Systèmes de garantie qualité", "Score moyen": 1.90},
        ],
        "score_global": 2.37
    },
    # Tu peux ajouter ici d'autres indicateurs selon le même modèle…
]

# Affichage du tableau pour chaque indicateur
for bloc in indicateurs:
    st.markdown(f"### {bloc['dimension']} — {bloc['indicateur']}")
    df = pd.DataFrame(bloc["categories"])
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    st.markdown(f"<div style='font-size:18px; margin-top:10px;'><b>Score moyen global pour la dimension :</b> {bloc['score_global']}</div>", unsafe_allow_html=True)
    st.markdown("---")

st.info("Ce tableau reproduit fidèlement la structure de la feuille 'Tous les résultats' avec des données statiques. Tu peux l’adapter selon tes besoins et tes propres valeurs.")
