import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_osae import dimensions, categories, effectifs, poids_relatif

# -- Utilitaires pour dataframes (déjà vus précédemment)
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
            if scores:
                mean_score = round(sum(scores) / len(scores), 2)
            else:
                mean_score = None
            cat_scores.append(mean_score)
        data.append(cat_scores)
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

def get_effectifs_by_categorie_and_dimension(effectifs, dimensions, categories):
    df = pd.DataFrame(
        effectifs,
        columns=[dim["nom"].replace("Dimension ", "") for dim in dimensions],
        index=categories
    )
    return df

def get_poids_relatif_df(categories, poids_relatif):
    df = pd.DataFrame({
        "Catégories d'acteurs": categories,
        "Poids relatif dans le processus de transition (%)": poids_relatif
    })
    return df

# -- Modern Style
st.markdown("""
    <style>
    .modern-card {
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 2px 12px #02736815;
        padding: 28px 22px 24px 22px;
        margin-bottom: 22px;
        border: 1.4px solid #e5eef0;
    }
    .modern-title {
        color: #027368;
        font-size: 1.17rem;
        font-weight: 800;
        margin-bottom: 0.3em;
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    }
    .modern-caption {
        color: #666;
        font-size: 0.98em;
        margin-bottom: 0.9em;
        margin-top: -0.45em;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='color:#011F26;margin-bottom:0.2em;font-size:2rem;'>Visualisations synthétiques</h2>", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom:1.4em;color:#027368;font-size:1.08em;'>Explorez ci-dessous les scores, volumes et répartitions sous forme graphique. Passez la souris sur les graphiques pour lire les valeurs.</div>", unsafe_allow_html=True)

# -- 1er graphique : Radar plot
radar_df = get_dimension_scores_per_categorie(dimensions, categories)
labels = radar_df.columns.tolist()
categories_labels = radar_df.index.tolist()
N = len(labels)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]

fig1, ax1 = plt.subplots(figsize=(4.5, 4.5), subplot_kw=dict(polar=True))
colors = plt.cm.tab10.colors

for idx, (cat, color) in enumerate(zip(categories_labels, colors)):
    values = radar_df.loc[cat].tolist()
    values += values[:1]
    ax1.plot(angles, values, label=cat, color=color, linewidth=2)
    ax1.fill(angles, values, color=color, alpha=0.11)
ax1.set_xticks(angles[:-1])
ax1.set_xticklabels(labels, fontsize=9)
ax1.set_yticks([1, 1.5, 2, 2.5, 3])
ax1.set_yticklabels([str(x) for x in [1, 1.5, 2, 2.5, 3]], fontsize=8)
ax1.set_ylim(0, 3.5)
ax1.spines['polar'].set_color('#027368')
ax1.spines['polar'].set_linewidth(1.4)
ax1.legend(loc="upper left", bbox_to_anchor=(1.15, 1.1), fontsize=8, frameon=False)
plt.title("", fontsize=10)

# -- 2e graphique : Barres Score global par dimension
dim_df = get_global_scores_by_dimension(dimensions)
fig2, ax2 = plt.subplots(figsize=(4.5, 3.1))
ax2.barh(dim_df["Dimension"], dim_df["Score moyen global par dimension (non pondéré)"], color="#027368cc")
for i, (score, y) in enumerate(zip(dim_df["Score moyen global par dimension (non pondéré)"], range(len(dim_df)))):
    ax2.text(score + 0.03, y, str(score), va='center', color="#222", fontweight="bold", fontsize=11)
ax2.set_xlim(2.3, 2.7)
ax2.set_xlabel("Score moyen global (non pondéré)", fontsize=10)
ax2.set_ylabel("")
ax2.grid(axis="x", linestyle=":", alpha=0.2)
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)

# --- Mise en page en deux colonnes modernes
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<div class="modern-title">Radar : Note globale des dimensions par catégories d’acteurs</div>', unsafe_allow_html=True)
    st.markdown('<div class="modern-caption">Chaque couleur représente une catégorie d’acteurs. Ce graphique synthétise leur évaluation moyenne pour chaque dimension.</div>', unsafe_allow_html=True)
    st.pyplot(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="modern-card">', unsafe_allow_html=True)
    st.markdown('<div class="modern-title">Score moyen global par dimension</div>', unsafe_allow_html=True)
    st.markdown('<div class="modern-caption">Barre horizontale pour chaque dimension. Ce score moyen n’est pas pondéré par la taille des groupes d’acteurs.</div>', unsafe_allow_html=True)
    st.pyplot(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -- Ajoute ici d'autres graphiques sous forme de "modern-card" dans des colonnes, lignes, etc.
# -- Exemples :
#     - Effectifs par dimension
#     - Poids relatif (pie chart)
#     - Etc.

