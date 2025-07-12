import streamlit as st
import pandas as pd

# Données statiques fidèles à la structure
indicateurs = [
    {"nom": "Indicateur 1", "scores": [1.44, 1.7, 2.7, 2.5, 2.0, 2.5, None], "score_global": 2.52},
    {"nom": "Indicateur 2", "scores": [2.0, 1.6, 3.2, 3.5, 3.0, 3.0, 3.0], "score_global": None},
    {"nom": "Indicateur 3", "scores": [1.8, 2.1, 2.9, 3.0, 2.2, 2.8, 3.1], "score_global": None},
]

categories = [
    "Petits exploitants agricoles familiaux",
    "Consommateurs",
    "Membres des Organisations non gouvernementales",
    "Membres des Organisations de la société civile",
    "Autorités administratives régionales et nationales",
    "Membres des structures de formation et de recherche",
    "Membres des systèmes de garantie de la qualité",
]

# Titre principal
st.title("Tableau - Résultats par Indicateur et Catégorie d'acteurs")

# Affichage du tableau selon la structure demandée
for idx, ind in enumerate(indicateurs):
    st.markdown(f"### {ind['nom']}")
    # Construction du DataFrame pour l'indicateur courant
    data = {
        "N°": [i + 1 for i in range(7)],
        "Catégories d'acteurs": categories,
        "Score moyen": ind["scores"],
    }
    df = pd.DataFrame(data)

    # Afficher le score global de la dimension à droite du premier bloc
    if ind["score_global"] is not None:
        cols = st.columns([3, 1])
        with cols[0]:
            st.dataframe(df, use_container_width=True, hide_index=True)
        with cols[1]:
            st.markdown("#### Score moyen global")
            st.metric(label="", value=round(ind["score_global"], 2))
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")

st.info("Structure et disposition du tableau strictement conforme au modèle de la feuille 'Tous les résultats'.")

