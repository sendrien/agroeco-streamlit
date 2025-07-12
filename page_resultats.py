import streamlit as st
import pandas as pd

def df_to_justified_html(df):
    html = df.to_html(
        index=False,
        classes="justify-table",
        border=0,
        escape=False
    )
    return html

def show_page_resultats():
    st.markdown("""
    <style>
    html, body, .stApp { background: #fff !important; }
    .justify-table th, .justify-table td {
        text-align: justify !important;
        text-justify: inter-word !important;
        white-space: pre-line !important;
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        font-size: 1.08em;
        padding: 9px 16px !important;
        color: #032612;
        transition: background 0.5s;
    }
    .justify-table th {
        background: #027368 !important;
        color: #fff;
        font-size: 0.8em;
    }
    .justify-table tr:hover td {
        background: #d7ece9 !important;
        color: #032612 !important;
        transition: background 0.22s;
    }
    .justify-table {
        width: 100% !important;
        border-collapse: separate !important;
        border-spacing: 0 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 18px #5C737322;
        margin-bottom: 1.1em;
        background: transparent;
        transition: box-shadow 0.5s;
    }
    hr {
        border: 1.8px solid #027368 !important;
        opacity: 0.7;
        transition: border 0.5s;
    }
    [data-testid="stExpander"] > div > div {
        color: #011F26 !important;
        font-size: 1.28em !important;
        font-weight: 700 !important;
        transition: color 0.18s, text-decoration 0.18s;
        cursor: pointer !important;
    }
    [data-testid="stExpander"]:hover > div > div {
        color: #027368 !important;
        font-weight: 800 !important;
        text-decoration: underline !important;
        cursor: pointer !important;
    }
    [data-testid="stExpander"] {
        background: #F4F7F6 !important;
        border-radius: 13px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 2px 16px #02736815;
        transition: background 0.5s, box-shadow 0.5s;
    }
    [data-testid="stExpander"] > div, [data-testid="stExpander"] > details {
        background: white !important;
        border-radius: 4px !important;
    }
    .score-global-acc {
        background: #027368;
        border-radius: 4px;
        box-shadow: 0 2px 12px #02736822;
        padding: 0.2em 1.1em 0.2em 1.1em;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 1.2em;
        margin-top: 0.4em;
        max-width: 355px;
        border: 1.2px solid #034001;
        transition: box-shadow 0.5s, background 0.5s;
    }
    .score-global-label-acc {
        color: #fff;
        font-size: 1.13em;
        font-weight: 600;
        text-align: center;
        transition: color 0.4s;
    }
    .score-global-value-acc {
        font-size: 2.12em;
        color: #FFD;
        font-weight: bold;
        text-align: center;
        margin-top: 0.22em;
        margin-bottom: 0.3em;
        transition: color 0.4s;
    }
    .indicator-title-acc {
        font-size: 1.13em;
        color: #027368;
        font-weight: 700;
        margin-top: 1.2em;
        margin-bottom: 0.35em;
        transition: color 0.4s;
    }
    .ind-separator-acc {
        border: none;
        height: 3px;
        background: #027368;
        margin: 1.15em 0 0.7em 0;
        border-radius: 8px;
        opacity: 0.8;
        transition: background 0.5s;
    }
    h1, .osae-main-title {
        color: #011F26 !important;
        font-size: 2.3rem !important;
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif !important;
        font-weight: 900 !important;
        letter-spacing: 0.01em !important;
        margin-bottom: 0.1em !important;
        margin-top: 0.15em !important;
        text-shadow: 0 3px 8px #011F2611;
        transition: color 0.4s, text-shadow 0.6s;
    }
    h2 {
        color: #5C7373 !important;
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        transition: color 0.4s;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100vw;
        min-height: 60px;
        background: #027368;
        color: #fff;
        text-align: center;
        padding: 18px 0 14px 0;
        font-size: 1.18rem;
        font-weight: 600;
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        box-shadow: 0 -2px 12px #011F2650;
        letter-spacing: 0.01em;
        z-index: 100;
        transition: background 0.6s, color 0.5s;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    @media (max-width: 700px) {
        .footer { font-size: 1rem; padding: 12px 0 10px 0;}
    }
    </style>
    """, unsafe_allow_html=True)

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

