import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Outil Statistique Agro-Economie (OSAE)",
    layout="wide"
)

# CSS GLOBAL palette OSAE
st.markdown("""
<style>
/* Tableau justifié palette OSAE */
.justify-table th, .justify-table td {
    text-align: justify !important;
    text-justify: inter-word !important;
    white-space: pre-line !important;
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    font-size: 1.07em;
    padding: 7px 12px !important;
    color: #032612;
}
.justify-table th {
    background: #E5EFE7 !important;
    color: #027368;
    font-size: 1.12em;
}
.justify-table {
    width: 100% !important;
    border-collapse: separate !important;
    border-spacing: 0 !important;
    border-radius: 9px !important;
    box-shadow: 0 2px 10px #5C737344;
    margin-bottom: 1.1em;
    background: #fff;
}
/* Accordéons & titres palette */
div[role="button"][aria-expanded] > span {
    font-size: 1.25em !important;
    font-weight: 900 !important;
    color: #011F26 !important;
    letter-spacing: 0.01em;
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
}
.score-global-acc {
    background: #E5EFE7;
    border-radius: 14px;
    box-shadow: 0 2px 13px #02736812;
    padding: 1.1em 0.7em 0.8em 0.7em;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 1.2em;
    margin-top: 0.4em;
    max-width: 355px;
    border: 1.4px solid #027368;
}
.score-global-label-acc {
    color: #027368;
    font-size: 1.11em;
    font-weight: 600;
    text-align: center;
}
.score-global-value-acc {
    font-size: 2.12em;
    color: #032612;
    font-weight: bold;
    text-align: center;
    margin-top: 0.22em;
    margin-bottom: 0.3em;
}
.indicator-title-acc {
    font-size: 1.13em;
    color: #034001;
    font-weight: 700;
    margin-top: 1.2em;
    margin-bottom: 0.35em;
}
.ind-separator-acc {
    border: none;
    height: 2.5px;
    background: #027368;
    margin: 1.2em 0 0.7em 0;
    border-radius: 7px;
}
/* Titres principaux */
h1, .osae-main-title {
    color: #011F26 !important;
    font-size: 2.2rem !important;
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
    font-weight: 900 !important;
}
hr {
    border: 1.5px solid #027368 !important;
}
.stTabs [data-baseweb="tab-list"] {
    border-bottom: 2.5px solid #027368 !important;
}
.stTabs [data-baseweb="tab"] {
    color: #5C7373 !important;
    font-weight: 600;
    font-size: 1.07em;
}
.stTabs [aria-selected="true"] {
    color: #011F26 !important;
    border-bottom: 3px solid #027368 !important;
}
</style>
""", unsafe_allow_html=True)

def df_to_justified_html(df):
    html = df.to_html(
        index=False,
        classes="justify-table",
        border=0,
        escape=False
    )
    return html

dimensions = [
    {
        "nom": "Dimension environnementale",
        "indicateurs": [
            {
                "nom": "Indicateur 1",
                "scores": [1.44, 1.7, 2.7, 2.5, 2.0, 2.5, None],
            },
            {
                "nom": "Indicateur 2",
                "scores": [2.0, 1.6, 3.2, 3.5, 3.0, 3.0, 3.0],
            },
        ],
    },
    {
        "nom": "Dimension économique",
        "indicateurs": [
            {
                "nom": "Indicateur 3",
                "scores": [1.8, 2.1, 2.9, 3.0, 2.2, 2.8, 3.1],
            }
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

st.markdown(
    "<h1 class='osae-main-title'>Outil Statistique Agro-Economie (OSAE)</h1>",
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📋 Syntèse structurée des résultats", "📝 Résumé", "📊 Graphiques"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <style>
        /* Accordéons palette OSAE */
        div[role="button"][aria-expanded] > span {
            font-size: 1.38em !important;
            font-weight: 900 !important;
            color: #011F26 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    score_colname = "Scores moyens Indicateurs non pondérés par les poids des acteurs"

    for i, dimension in enumerate(dimensions):
        all_scores = []
        for ind in dimension["indicateurs"]:
            all_scores += [v for v in ind["scores"] if v is not None]
        score_global_dimension = round(sum(all_scores) / len(all_scores), 2)

        with st.expander(f"{dimension['nom']}", expanded=(i == 0)):
            st.markdown(
                f"""
                <div class="score-global-acc">
                    <div class="score-global-label-acc">
                        Score moyen global<br>par dimension (non pondéré)
                    </div>
                    <div class="score-global-value-acc">{score_global_dimension}</div>
                </div>
                """, unsafe_allow_html=True
            )

            for idx, ind in enumerate(dimension["indicateurs"]):
                st.markdown(
                    f'<div class="indicator-title-acc">&#x25B6;&nbsp;{ind["nom"]}</div>',
                    unsafe_allow_html=True
                )
                data = {
                    "N°": [i + 1 for i in range(7)],
                    "Catégories d'acteurs": categories,
                    score_colname: [
                        "--" if v is None else v for v in ind["scores"]
                    ],
                }
                df = pd.DataFrame(data)
                html = df_to_justified_html(df)
                st.markdown(html, unsafe_allow_html=True)
                if idx < len(dimension["indicateurs"]) - 1:
                    st.markdown('<hr class="ind-separator-acc">', unsafe_allow_html=True)

    st.markdown(
        "<span style='color:#5C7373;font-size:1em'>"
        "<b>Note&nbsp;:</b> Le score moyen global par dimension est la moyenne simple de tous les scores affichés dans la colonne « Scores moyens Indicateurs non pondérés par les poids des acteurs » des indicateurs de cette dimension, sans pondération selon la représentativité des groupes d'acteurs.</span>",
        unsafe_allow_html=True,
    )

with tab2:
    st.markdown(
        "<h2 style='color:#011F26;'>Résumé</h2>"
        "<p style='color:#5C7373;'>Cette page sera prochainement complétée avec un résumé automatique des résultats.</p>",
        unsafe_allow_html=True,
    )

with tab3:
    st.markdown(
        "<h2 style='color:#011F26;'>Graphiques</h2>"
        "<p style='color:#5C7373;'>Les visualisations graphiques seront bientôt disponibles ici.</p>",
        unsafe_allow_html=True,
    )

# --- FOOTER ---
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100vw;
        background: #E5EFE7;
        color: #027368;
        text-align: center;
        padding: 10px 0 7px 0;
        font-size: 1rem;
        box-shadow: 0 -1px 6px #02736822;
        z-index: 100;
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    }
    @media (max-width: 700px) {
        .footer { font-size: 0.93rem; padding: 8px 0 5px 0;}
    }
    </style>
    <div class="footer">
        © 2025 OSAE — Outil Statistique Agro-Economie | Développé par votre équipe
    </div>
""", unsafe_allow_html=True)
