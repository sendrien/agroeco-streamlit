import streamlit as st
import pandas as pd

# --- À importer ou synchroniser avec page_resultats.py ! ---
dimensions = [
    {
        "nom": "Dimension environnementale",
        "indicateurs": [
            {"nom": "Indicateur 1", "scores": [1.44, 1.7, 2.7, 2.5, 2.0, 2.5, None]},
            {"nom": "Indicateur 2", "scores": [2.0, 1.6, 3.2, 3.5, 3.0, 3.0, 3.0]},
        ],
    },
    {
        "nom": "Dimension économique",
        "indicateurs": [
            {"nom": "Indicateur 3", "scores": [1.8, 2.1, 2.9, 3.0, 2.2, 2.8, 3.1]},
        ],
    },
    {
        "nom": "Dimension territoriale",
        "indicateurs": [
            {"nom": "Indicateur 4", "scores": [2.2, 1.9, 2.5, 3.0, 2.8, 2.3, 2.7]},
            {"nom": "Indicateur 5", "scores": [2.0, 2.4, 2.7, 2.8, 2.5, 2.1, 2.6]},
        ],
    },
    {
        "nom": "Dimension politique et sociale",
        "indicateurs": [
            {"nom": "Indicateur 6", "scores": [1.7, 1.9, 2.3, 2.7, 2.4, 2.0, 2.8]},
            {"nom": "Indicateur 7", "scores": [2.5, 2.6, 2.9, 3.0, 2.9, 2.7, 3.1]},
        ],
    },
    {
        "nom": "Dimension temporelle",
        "indicateurs": [
            {"nom": "Indicateur 8", "scores": [2.0, 2.2, 2.3, 2.6, 2.1, 2.5, 2.2]},
        ],
    },
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

def get_dimension_scores_per_categorie(dimensions, categories):
    data = []
    for i, cat in enumerate(categories):
        cat_scores = []
        for dim in dimensions:
            scores = []
            for indic in dim["indicateurs"]:
                if i < len(indic["scores"]):
                    v = indic["scores"][i]
                    if v is not None:
                        scores.append(v)
            # Moyenne des indicateurs de la dimension pour la catégorie
            if scores:
                mean_score = round(sum(scores) / len(scores), 2)
            else:
                mean_score = None
            cat_scores.append(mean_score)
        data.append(cat_scores)
    # Construire le DataFrame
    df = pd.DataFrame(
        data,
        columns=[dim["nom"].replace("Dimension ", "") for dim in dimensions],
        index=categories
    )
    return df

def show_page_resume():
    st.markdown("<h2 style='color:#027368;'>Résumé – Tableau pour radar</h2>", unsafe_allow_html=True)

    radar_df = get_dimension_scores_per_categorie(dimensions, categories)

    # Affichage justifié
    st.markdown("""
        <style>
        .radar-justif th, .radar-justif td {
            text-align: justify !important;
            text-justify: inter-word !important;
            font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
            font-size: 1.05em;
            padding: 7px 13px !important;
        }
        .radar-justif th { background: #027368 !important; color: #fff; font-size: 0.85em;}
        .radar-justif { width: 100% !important; border-radius: 7px !important; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(
        radar_df.reset_index().to_html(index=False, classes="radar-justif", border=0), 
        unsafe_allow_html=True
    )

    st.info("Ce tableau est structuré pour permettre la génération du radar plot : chaque ligne = une catégorie d’acteurs, chaque colonne = une dimension (moyenne de ses indicateurs pour la catégorie).")
