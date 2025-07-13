import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_osae import dimensions, categories

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

def show_page_graphiques():
    st.markdown("<h3 style='color:#027368;'>Radar plot : Note globale des dimensions par catégories d'acteurs</h3>", unsafe_allow_html=True)

    radar_df = get_dimension_scores_per_categorie(dimensions, categories)
    labels = radar_df.columns.tolist()
    categories_labels = radar_df.index.tolist()
    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(2.8, 2.8), subplot_kw=dict(polar=True))  # Taille réduite

    colors = plt.cm.tab10.colors
    for idx, (cat, color) in enumerate(zip(categories_labels, colors)):
        values = radar_df.loc[cat].tolist()
        values += values[:1]
        ax.plot(angles, values, label=cat, color=color, linewidth=1.3)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_yticks([1, 1.5, 2, 2.5, 3])
    ax.set_yticklabels([str(x) for x in [1, 1.5, 2, 2.5, 3]], fontsize=7)
    ax.set_ylim(0, 3.5)

    # Pas de titre sur le graphique
    # Légende compacte en bas du graphique
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.20), fontsize=7, frameon=False, ncol=1)

    st.pyplot(fig)

# Utilisation dans la page
if __name__ == "__main__" or "streamlit" in __name__:
    show_page_graphiques()
