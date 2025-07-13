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
    angles += angles[:1]  # fermer le polygone

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))  # Taille réduite

    colors = plt.cm.tab10.colors

    for idx, (cat, color) in enumerate(zip(categories_labels, colors)):
        values = radar_df.loc[cat].tolist()
        values += values[:1]
        ax.plot(angles, values, label=cat, color=color, linewidth=2)
        ax.fill(angles, values, color=color, alpha=0.12)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_yticks([1, 1.5, 2, 2.5, 3])
    ax.set_yticklabels([str(x) for x in [1, 1.5, 2, 2.5, 3]], fontsize=9)
    ax.set_ylim(0, 3.5)

    plt.title("Note globale des dimensions par catégories d'acteurs", size=11, y=1.07, weight="bold")
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=9, frameon=False)

    st.pyplot(fig)

