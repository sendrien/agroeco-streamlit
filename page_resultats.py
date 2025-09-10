import streamlit as st
import pandas as pd
from data_osae import dimensions, categories, score_colname

def df_to_justified_html(df):
    return df.to_html(index=False, classes="justify-table", border=0, escape=False)

def show_page_resultats():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    for i, dimension in enumerate(dimensions):
        all_scores = [v for ind in dimension["indicateurs"] for v in ind["scores"] if v is not None]
        score_global_dimension = round(sum(all_scores) / len(all_scores), 2) if all_scores else None

        with st.expander(f"{dimension['nom']}", expanded=(i == 0)):
            st.markdown(
                f"""
                <div class="score-global-acc">
                    <div class="score-global-label-acc">
                        Score moyen global<br>par dimension (non pondéré)
                    </div>
                    <div class="score-global-value-acc">{score_global_dimension if score_global_dimension is not None else '--'}</div>
                </div>
                """, unsafe_allow_html=True
            )

            for idx, ind in enumerate(dimension["indicateurs"]):
                st.markdown(f"<div class='h-section'><span class='pill'></span><h2 style='font-size:1.02rem;margin:0'>{ind['nom']}</h2></div>", unsafe_allow_html=True)
                data = {
                    "N°": [i + 1 for i in range(7)],
                    "Catégories d'acteurs": categories,
                    score_colname: ["--" if v is None else v for v in ind["scores"]],
                }
                df = pd.DataFrame(data)
                st.markdown(df_to_justified_html(df), unsafe_allow_html=True)
                if idx < len(dimension["indicateurs"]) - 1:
                    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown(
        "<div style='color:#5C7373;font-size:.98em;margin-top:8px'><b>Note&nbsp;:</b> "
        "Le score moyen global par dimension est la moyenne simple de tous les scores affichés dans la colonne "
        "« Scores moyens Indicateurs non pondérés par les poids des acteurs », sans pondération selon la représentativité des groupes d'acteurs.</div>",
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)
