import streamlit as st
import pandas as pd

# Définition statique de toutes les dimensions, chacune avec ses indicateurs
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
    # Ajoute d'autres dimensions et indicateurs ici si besoin
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
    "<h2 style='color:#007C91; font-size:2.3rem; margin-bottom:0.5em;'>Dimensions de l'outil AGROECO</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h4 style='color:gray; font-weight:400;margin-top:-10px;'>Synthèse structurée des résultats par dimension</h4>",
    unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

for dimension in dimensions:
    # Récupérer tous les scores pour la dimension, pour le calcul du score global
    all_scores = []
    for ind in dimension["indicateurs"]:
        all_scores += [v for v in ind["scores"] if v is not None]
    score_global_dimension = round(sum(all_scores) / len(all_scores), 2)

    # Affichage du nom de la dimension
    st.markdown(
        f"<h3 style='color:#007C91;'>{dimension['nom']}</h3>",
        unsafe_allow_html=True,
    )

    # Encadré latéral du score global
    st.markdown(
        f"""
        <div style='float:right;background:#F3FAFD;border-radius:18px;padding:16px 25px 11px 25px;
        box-shadow:0 3px 12px #007c9140;margin-bottom:25px;'>
            <div style='color:#007C91;font-size:1em;font-weight:bold;'>
                Score moyen global<br>par dimension (non pondéré)
            </div>
            <div style='font-size:2em;color:#222;text-align:center;font-weight:bold;margin-top:3px;'>
                {score_global_dimension}
            </div>
        </div>
        """, unsafe_allow_html=True
    )

    # Pour chaque indicateur de la dimension
    for ind in dimension["indicateurs"]:
        st.markdown(
            f"<div style='font-size:1.1em;font-weight:bold;color:#333;margin-top:44px;'>"
            f"&#x25B6;&nbsp;{ind['nom']}</div>", unsafe_allow_html=True
        )
        # Tableaux sans .highlight_null, mais avec un affichage personnalisé pour None/NaN
        data = {
            "N°": [i + 1 for i in range(7)],
            "Catégories d'acteurs": categories,
            "Score moyen": [
                "--" if v is None else v for v in ind["scores"]
            ],
        }
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    "<span style='color:gray;font-size:1em'>"
    "<b>Note&nbsp;:</b> Le score moyen global par dimension est la moyenne simple de tous les scores affichés dans la colonne « Score moyen » des indicateurs de cette dimension, sans pondération selon la représentativité des groupes d'acteurs.</span>",
    unsafe_allow_html=True,
)
