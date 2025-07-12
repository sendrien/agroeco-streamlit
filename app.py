import streamlit as st
import pandas as pd

# Définition statique des données (Exemple Dimension ENVIRONNEMENTALE)
dimension = "Dimension environnementale"
indicateurs = [
    {"nom": "Indicateur 1", "scores": [1.44, 1.7, 2.7, 2.5, 2.0, 2.5, None]},
    {"nom": "Indicateur 2", "scores": [2.0, 1.6, 3.2, 3.5, 3.0, 3.0, 3.0]},
    {"nom": "Indicateur 3", "scores": [1.8, 2.1, 2.9, 3.0, 2.2, 2.8, 3.1]},
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

# Calcul du score moyen global (non pondéré) pour la dimension (sur l'ensemble des scores des 3 indicateurs)
all_scores = []
for ind in indicateurs:
    all_scores += [v for v in ind["scores"] if v is not None]
score_global_dimension = round(sum(all_scores) / len(all_scores), 2)

st.markdown(
    "<h2 style='color:#007C91; font-size:2.3rem; margin-bottom:0.5em;'>Dimensions de l'outil AGROECO</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    f"<h4 style='color:gray; font-weight:400;margin-top:-10px;'>Synthèse structurée de la <span style='color:#007C91'>{dimension}</span></h4>",
    unsafe_allow_html=True,
)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Bloc latéral pour le score moyen global par dimension
st.markdown(
    f"""
    <div style='float:right;background:#F3FAFD;border-radius:18px;padding:18px 30px 15px 30px;
    box-shadow:0 3px 12px #007c9140;margin-bottom:25px;'>
        <div style='color:#007C91;font-size:1.1em;font-weight:bold;'>
            Score moyen global par dimension (non pondéré)
        </div>
        <div style='font-size:2.2em;color:#222;text-align:center;font-weight:bold;margin-top:4px;'>
            {score_global_dimension}
        </div>
    </div>
    """, unsafe_allow_html=True
)

# Pour chaque indicateur, affichage stylé
for idx, ind in enumerate(indicateurs):
    st.markdown(
        f"<div style='font-size:1.2em;font-weight:bold;color:#007C91;margin-top:55px;'>"
        f"&#x25B6;&nbsp;{ind['nom']}</div>", unsafe_allow_html=True
    )
    data = {
        "N°": [i + 1 for i in range(7)],
        "Catégories d'acteurs": categories,
        "Score moyen": ind["scores"],
    }
    df = pd.DataFrame(data)
    st.dataframe(
        df.style
        .highlight_null(null_color='#F8D7DA')
        .format({'Score moyen': '{:.2f}'})
        .set_properties(**{'background-color': '#F3FAFD'}, subset=pd.IndexSlice[:, ['Score moyen']]),
        use_container_width=True,
        hide_index=True
    )

st.markdown("<hr style='margin-top:3em;'>", unsafe_allow_html=True)
st.markdown(
    "<span style='color:gray;font-size:1em'>"
    "<b>Note&nbsp;:</b> Le score moyen global par dimension est la moyenne simple de tous les scores affichés dans la colonne « Score moyen », sans pondération selon la représentativité des groupes d'acteurs.</span>",
    unsafe_allow_html=True,
)
