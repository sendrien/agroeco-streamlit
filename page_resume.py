import streamlit as st
import pandas as pd
from data_osae import dimensions, categories  # ← Données importées du fichier central

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

def get_global_scores_by_dimension(dimensions):
    rows = []
    for dim in dimensions:
        scores = []
        for indic in dim["indicateurs"]:
            scores += [v for v in indic["scores"] if v is not None]
        if scores:
            mean = round(sum(scores) / len(scores), 1)
        else:
            mean = None
        rows.append({
            "Dimension": dim["nom"].replace("Dimension ", ""),
            "Score moyen global par dimension (non pondéré)": mean
        })
    df = pd.DataFrame(rows)
    return df

def show_page_resume():
    st.markdown("<h3 style='color:#027368;'>Note globale des dimensions par catégories d'acteurs</h3>", unsafe_allow_html=True)

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

    # --- Tableau score moyen global par dimension (non pondéré)
    st.markdown("<h3 style='color:#027368; margin-top:2em;'>Score moyen global par dimension (non pondéré)</h3>", unsafe_allow_html=True)

    dim_df = get_global_scores_by_dimension(dimensions)

    st.markdown("""
        <style>
        .dimscore-justif th, .dimscore-justif td {
            text-align: justify !important;
            text-justify: inter-word !important;
            font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
            font-size: 1.08em;
            padding: 8px 12px !important;
        }
        .dimscore-justif th { background: #027368 !important; color: #fff; font-size: 0.93em;}
        .dimscore-justif { width: 90% !important; border-radius: 7px !important; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(
        dim_df.to_html(index=False, classes="dimscore-justif", border=0),
        unsafe_allow_html=True
    )
