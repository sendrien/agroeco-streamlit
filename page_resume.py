import streamlit as st
import pandas as pd
from data_osae import dimensions, categories, effectifs, poids_relatif

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
            cat_scores.append(round(sum(scores) / len(scores), 2) if scores else None)
        data.append(cat_scores)
    return pd.DataFrame(data,
        columns=[dim["nom"].replace("Dimension ", "") for dim in dimensions],
        index=categories
    )

def get_global_scores_by_dimension(dimensions):
    rows = []
    for dim in dimensions:
        scores = [v for indic in dim["indicateurs"] for v in indic["scores"] if v is not None]
        rows.append({"Dimension": dim["nom"].replace("Dimension ", ""),
                     "Score moyen global par dimension (non pondéré)": round(sum(scores) / len(scores), 1) if scores else None})
    return pd.DataFrame(rows)

def get_effectifs_by_categorie_and_dimension(effectifs, dimensions, categories):
    return pd.DataFrame(effectifs,
        columns=[dim["nom"].replace("Dimension ", "") for dim in dimensions],
        index=categories
    )

def get_poids_relatif_df(categories, poids_relatif):
    return pd.DataFrame({"Catégories d'acteurs": categories,
                         "Poids relatif dans le processus de transition (%)": poids_relatif})

def get_total_respondants_by_dimension(effectifs, dimensions):
    df = pd.DataFrame(effectifs,
        columns=[dim["nom"].replace("Dimension ", "") for dim in dimensions],
        index=categories
    )
    return pd.DataFrame({"Dimension": df.columns, "Nombre total de répondants": df.sum(axis=0).values})

def show_page_resume():
    # Bloc 1
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#027368;margin:0 0 8px 0;'>Note globale des dimensions par catégories d'acteurs</h3>", unsafe_allow_html=True)

    radar_df = get_dimension_scores_per_categorie(dimensions, categories)
    st.markdown("""
        <style>
        .radar-justif th, .radar-justif td {
            text-align: justify !important; text-justify: inter-word !important;
            font-family: 'Segoe UI','Roboto','Arial',sans-serif; font-size: 1.05em; padding: 7px 13px !important;
        }
        .radar-justif th { background: #027368 !important; color: #fff; font-size: 0.85em;}
        .radar-justif { width: 100% !important; border-radius: 7px !important; box-shadow: var(--shadow); }
        </style>
    """, unsafe_allow_html=True)
    st.markdown(radar_df.reset_index().to_html(index=False, classes="radar-justif", border=0), unsafe_allow_html=True)
    st.info("Ce tableau alimente le radar plot : chaque ligne = catégorie d’acteurs ; chaque colonne = dimension (moyenne des indicateurs pour cette catégorie).")
    st.markdown("</div>", unsafe_allow_html=True)

    # Bloc 2
    st.markdown("<div class='card' style='margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#027368;margin:0 0 8px 0;'>Score moyen global par dimension (non pondéré)</h3>", unsafe_allow_html=True)
    dim_df = get_global_scores_by_dimension(dimensions)
    st.markdown("""
        <style>
        .dimscore-justif th, .dimscore-justif td {
            text-align: justify !important; text-justify: inter-word !important;
            font-family: 'Segoe UI','Roboto','Arial',sans-serif; font-size: 1.06em; padding: 8px 12px !important;
        }
        .dimscore-justif th { background: #027368 !important; color: #fff; font-size: 0.9em;}
        .dimscore-justif { width: 90% !important; border-radius: 7px !important; box-shadow: var(--shadow); }
        </style>
    """, unsafe_allow_html=True)
    st.markdown(dim_df.to_html(index=False, classes="dimscore-justif", border=0), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Bloc 3
    st.markdown("<div class='card' style='margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#027368;margin:0 0 8px 0;'>Nombre de répondants par catégorie d’acteurs et par dimension</h3>", unsafe_allow_html=True)
    eff_df = get_effectifs_by_categorie_and_dimension(effectifs, dimensions, categories)
    st.markdown("""
        <style>
        .effectif-justif th, .effectif-justif td {
            text-align: justify !important; text-justify: inter-word !important;
            font-family: 'Segoe UI','Roboto','Arial',sans-serif; font-size: 1.06em; padding: 8px 12px !important;
        }
        .effectif-justif th { background: #027368 !important; color: #fff; font-size: 0.9em;}
        .effectif-justif { width: 90% !important; border-radius: 7px !important; box-shadow: var(--shadow); }
        </style>
    """, unsafe_allow_html=True)
    st.markdown(eff_df.reset_index().to_html(index=False, classes="effectif-justif", border=0), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Bloc 4
    st.markdown("<div class='card' style='margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#027368;margin:0 0 8px 0;'>Poids relatif des acteurs dans le processus de transition (en %)</h3>", unsafe_allow_html=True)
    poids_df = get_poids_relatif_df(categories, poids_relatif)
    st.markdown("""
        <style>
        .poidsrel-justif th, .poidsrel-justif td {
            text-align: justify !important; text-justify: inter-word !important;
            font-family: 'Segoe UI','Roboto','Arial',sans-serif; font-size: 1.06em; padding: 8px 12px !important;
        }
        .poidsrel-justif th { background: #027368 !important; color: #fff; font-size: 0.9em;}
        .poidsrel-justif { width: 70% !important; border-radius: 7px !important; box-shadow: var(--shadow); }
        </style>
    """, unsafe_allow_html=True)
    st.markdown(poids_df.to_html(index=False, classes="poidsrel-justif", border=0), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Bloc 5
    st.markdown("<div class='card' style='margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#027368;margin:0 0 8px 0;'>Nombre total de répondants par dimension</h3>", unsafe_allow_html=True)
    total_df = get_total_respondants_by_dimension(effectifs, dimensions)
    st.markdown("""
        <style>
        .totalresp-justif th, .totalresp-justif td {
            text-align: justify !important; text-justify: inter-word !important;
            font-family: 'Segoe UI','Roboto','Arial',sans-serif; font-size: 1.06em; padding: 8px 12px !important;
        }
        .totalresp-justif th { background: #027368 !important; color: #fff; font-size: 0.9em;}
        .totalresp-justif { width: 50% !important; border-radius: 7px !important; box-shadow: var(--shadow); }
        </style>
    """, unsafe_allow_html=True)
    st.markdown(total_df.to_html(index=False, classes="totalresp-justif", border=0), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
