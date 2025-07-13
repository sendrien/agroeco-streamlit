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

    # DPI élevé + taille adaptée
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True), dpi=140)
    colors = plt.cm.tab10.colors
    linewidth = 2.5

    for idx, (cat, color) in enumerate(zip(categories_labels, colors)):
        values = radar_df.loc[cat].tolist()
        values += values[:1]
        ax.plot(angles, values, label=cat, color=color, linewidth=linewidth)
        ax.fill(angles, values, color=color, alpha=0.09)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=13, fontweight='bold')
    ax.set_yticks([1, 1.5, 2, 2.5, 3])
    ax.set_yticklabels([str(x) for x in [1, 1.5, 2, 2.5, 3]], fontsize=11)
    ax.set_ylim(0, 3.5)
    ax.grid(True, color="grey", linestyle="--", linewidth=0.7, alpha=0.7)
    ax.spines['polar'].set_color('#027368')
    ax.spines['polar'].set_linewidth(1.5)

    # Légende en dehors du radar
    ax.legend(loc='center left', bbox_to_anchor=(1.05, 0.5), fontsize=10, frameon=False)
    plt.tight_layout(pad=2.2)
    st.pyplot(fig)

if __name__ == "__main__" or "streamlit" in __name__:
    show_page_graphiques()
