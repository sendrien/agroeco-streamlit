import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Outil Statistique Agro-Economie (OSAE)",
    layout="wide"
)

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
    "<h1 style='color:#007C91; font-size:2.7rem; margin-bottom:0.2em;'>Outil Statistique Agro-Economie (OSAE)</h1>",
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📋 Syntèse structurée des résultats", "📝 Résumé", "📊 Graphiques"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    # Style pour le score global, séparateurs, et titres des accordions
    st.markdown("""
        <style>
        /* Accordion Title */
        div[role="button"][aria-expanded] > span {
            font-size: 1.35em !important;
            font-weight: bold !important;
            color: #007C91 !important;
            letter-spacing: 0.01em;
        }
        /* Score global block */
        .score-global-acc {
            background: #F3FAFD;
            border-radius: 16px;
            box-shadow: 0 2px 10px #007c9140;
            padding: 1.1em 0.7em 0.8em 0.7em;
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 1.2em;
            margin-top: 0.4em;
            max-width: 350px;
        }
        .score-global-label-acc {
            color: #007C91;
            font-size: 1em;
            font-weight: 500;
            text-align: center;
        }
        .score-global-value-acc {
            font-size: 2em;
            color: #222;
            font-weight: bold;
            text-align: center;
            margin-top: 0.22em;
            margin-bottom: 0.3em;
        }
        .indicator-title-acc {
            font-size: 1.08em;
            color: #333;
            font-weight: 600;
            margin-top: 1.2em;
            margin-bottom: 0.3em;
        }
        .ind-separator-acc {
            border: none;
            height: 2px;
            background: linear-gradient(90deg, #007C91 18%, #fff 95%);
            margin: 1.2em 0 0.7em 0;
        }
        </style>
    """, unsafe_allow_html=True)

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
                    "Score moyen": [
                        "--" if v is None else v for v in ind["scores"]
                    ],
                }
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                if idx < len(dimension["indicateurs"]) - 1:
                    st.markdown('<hr class="ind-separator-acc">', unsafe_allow_html=True)

    st.markdown(
        "<span style='color:gray;font-size:1em'>"
        "<b>Note&nbsp;:</b> Le score moyen global par dimension est la moyenne simple de tous les scores affichés dans la colonne « Score moyen » des indicateurs de cette dimension, sans pondération selon la représentativité des groupes d'acteurs.</span>",
        unsafe_allow_html=True,
    )

with tab2:
    st.markdown(
        "<h2 style='color:#007C91;'>Résumé</h2>"
        "<p style='color:gray;'>Cette page sera prochainement complétée avec un résumé automatique des résultats.</p>",
        unsafe_allow_html=True,
    )

with tab3:
    st.markdown(
        "<h2 style='color:#007C91;'>Graphiques</h2>"
        "<p style='color:gray;'>Les visualisations graphiques seront bientôt disponibles ici.</p>",
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
        background: #F3FAFD;
        color: #007C91;
        text-align: center;
        padding: 10px 0 7px 0;
        font-size: 1rem;
        box-shadow: 0 -1px 6px #007c9140;
        z-index: 100;
    }
    @media (max-width: 700px) {
        .footer { font-size: 0.93rem; padding: 8px 0 5px 0;}
    }
    </style>
    <div class="footer">
        © 2025 OSAE — Outil Statistique Agro-Economie | Développé par votre équipe
    </div>
""", unsafe_allow_html=True)
