import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Outil Statistique Agro-Economie (OSAE)",
    layout="wide"
)

# ----------- CSS GLOBAL : justification & améliorations -----------
st.markdown("""
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<style>
/* Justification tableaux */
.justify-table th, .justify-table td {
    text-align: justify !important;
    text-justify: inter-word !important;
    white-space: pre-line !important;
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    font-size: 1.06em;
    padding: 7px 11px !important;
}
.justify-table th {
    background: #eaf4fb !important;
}
.justify-table {
    width: 100% !important;
    border-collapse: separate !important;
    border-spacing: 0 !important;
    border-radius: 10px !important;
    box-shadow: 0 3px 14px #145da016;
    margin-bottom: 1em;
}
/* Accordion améliorés */
[data-testid="stExpander"] > div > label, div[role="button"][aria-expanded] > span {
    font-size: 1.25em !important;
    font-weight: 800 !important;
    color: #008A63 !important;
    letter-spacing: 0.02em;
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    padding-left: 0.3em;
}
[data-testid="stExpander"] svg {
    color: #008A63 !important;
}
/* Titres dimension */
.dimension-title {
    font-size: 2.15em;
    color: #145DA0;
    font-weight: 900;
    letter-spacing: 0.01em;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0.07em;
}
.indicator-title-acc {
    font-size: 1.18em;
    color: #e47919;
    font-weight: 700;
    margin-top: 1.2em;
    margin-bottom: 0.5em;
    display: flex;
    align-items: center;
    gap: 5px;
}
.score-global-acc {
    background: linear-gradient(95deg, #ECF9F1 65%, #B8D7F5 100%);
    border-radius: 14px;
    box-shadow: 0 2px 13px #b1e7cb2f;
    padding: 1.1em 0.7em 0.8em 0.7em;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 1.2em;
    margin-top: 0.4em;
    max-width: 360px;
    border: 1.5px solid #b1e7cb4b;
}
.score-global-label-acc {
    color: #008A63;
    font-size: 1.13em;
    font-weight: 600;
    text-align: center;
}
.score-global-value-acc {
    font-size: 2.2em;
    color: #222;
    font-weight: bold;
    text-align: center;
    margin-top: 0.22em;
    margin-bottom: 0.3em;
}
.ind-separator-acc {
    border: none;
    height: 2.5px;
    background: linear-gradient(90deg, #145DA0 10%, #FFD200 65%, #fff 100%);
    margin: 1.1em 0 0.7em 0;
    border-radius: 8px;
}
span.material-icons {
    font-size: 1.18em !important;
    vertical-align: -0.19em !important;
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
        "icon": "eco",      # Icône Material
        "color": "#00AB71",
        "indicateurs": [
            {
                "nom": "Indicateur 1",
                "icon": "analytics",
                "scores": [1.44, 1.7, 2.7, 2.5, 2.0, 2.5, None],
            },
            {
                "nom": "Indicateur 2",
                "icon": "show_chart",
                "scores": [2.0, 1.6, 3.2, 3.5, 3.0, 3.0, 3.0],
            },
        ],
    },
    {
        "nom": "Dimension économique",
        "icon": "paid",
        "color": "#E47919",
        "indicateurs": [
            {
                "nom": "Indicateur 3",
                "icon": "bar_chart",
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
    "<div class='dimension-title'><span class='material-icons'>apps</span>Outil Statistique Agro-Economie (OSAE)</div>",
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "📋 Syntèse structurée des résultats", 
    "📝 Résumé", 
    "📊 Graphiques"
])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    score_colname = "Scores moyens Indicateurs non pondérés par les poids des acteurs"

    for i, dimension in enumerate(dimensions):
        all_scores = []
        for ind in dimension["indicateurs"]:
            all_scores += [v for v in ind["scores"] if v is not None]
        score_global_dimension = round(sum(all_scores) / len(all_scores), 2)
        # Couleur d’accompagnement
        color = dimension.get("color", "#145DA0")
        icon = dimension.get("icon", "apps")

        with st.expander(f"<span class='material-icons'>{icon}</span> "
                         f"<span style='color:{color};font-size:1.24em;font-weight:700;'>{dimension['nom']}</span>", 
                         expanded=(i == 0)):
            st.markdown(
                f"""
                <div class="score-global-acc">
                    <div class="score-global-label-acc">
                        <span class="material-icons" style="color:{color};">star_rate</span>
                        Score moyen global<br>par dimension (non pondéré)
                    </div>
                    <div class="score-global-value-acc">{score_global_dimension}</div>
                </div>
                """, unsafe_allow_html=True
            )

            for idx, ind in enumerate(dimension["indicateurs"]):
                ind_icon = ind.get("icon", "info")
                st.markdown(
                    f"""<div class="indicator-title-acc">
                    <span class="material-icons" style="color:{color};">{ind_icon}</span>
                    {ind["nom"]}
                    </div>""",
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
        "<span style='color:gray;font-size:1em'>"
        "<b>Note&nbsp;:</b> Le score moyen global par dimension est la moyenne simple de tous les scores affichés dans la colonne « Scores moyens Indicateurs non pondérés par les poids des acteurs » des indicateurs de cette dimension, sans pondération selon la représentativité des groupes d'acteurs.</span>",
        unsafe_allow_html=True,
    )

with tab2:
    st.markdown(
        "<h2 style='color:#145DA0;'><span class='material-icons' style='vertical-align:-3px;'>description</span> Résumé</h2>"
        "<p style='color:gray;'>Cette page sera prochainement complétée avec un résumé automatique des résultats.</p>",
        unsafe_allow_html=True,
    )

with tab3:
    st.markdown(
        "<h2 style='color:#145DA0;'><span class='material-icons' style='vertical-align:-3px;'>insert_chart</span> Graphiques</h2>"
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
        color: #145DA0;
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
        <span class="material-icons" style="vertical-align:-3px;font-size:1.11em;">copyright</span>
        2025 OSAE — Outil Statistique Agro-Economie | Développé par votre équipe
    </div>
""", unsafe_allow_html=True)
