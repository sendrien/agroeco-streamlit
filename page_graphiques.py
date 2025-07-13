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
    st.markdown("""
    <style>
    .graph-card {
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 2px 16px #02736819;
        padding: 26px 26px 18px 26px;
        margin-bottom: 2.5em;
        border: 1.3px solid #e4e8ee;
        max-width: 670px;
        margin-left: auto;
        margin-right: auto;
    }
    .graph-title {
        color: #027368;
        font-size: 1.3rem;
        font-weight: 800;
        margin-bottom: 0.75em;
        text-align: center;
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        letter-spacing: 0.5px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.markdown('<div class="graph-title">Radar plot : Note globale des dimensions par catégories d’acteurs</div>', unsafe_allow_html=True)

    radar_df = get_dimension_scores_per_categorie(dimensions, categories)
    labels = radar_df.columns.tolist()
    categories_labels = radar_df.index.tolist()
    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    # Taille réduite et police claire
    fig, ax = plt.subplots(figsize=(5.2, 5.2), subplot_kw=dict(polar=True))
    colors = [
        "#2F92B1", "#F2A83B", "#9E9E9E", "#FFC100", "#4E89A4", "#A6C36F", "#7766E3"
    ]
    for idx, (cat, color) in enumerate(zip(categories_labels, colors)):
        values = radar_df.loc[cat].tolist()
        values += values[:1]
        ax.plot(angles, values, label=cat, color=color, linewidth=2)
        ax.fill(angles, values, color=color, alpha=0.14)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12, fontweight='semibold', color="#282828")
    ax.set_yticks([1, 1.5, 2, 2.5, 3])
    ax.set_yticklabels([str(x) for x in [1, 1.5, 2, 2.5, 3]], fontsize=11)
    ax.set_ylim(0, 3.5)
    ax.spines['polar'].set_color('#027368')
    ax.spines['polar'].set_linewidth(1.2)
    plt.title("", fontsize=10)
    # Légende "carte de visite" moderne
    ax.legend(loc="upper left", bbox_to_anchor=(1.04, 1.02), fontsize=10, frameon=False)
    plt.tight_layout(pad=1.6)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align:center;font-size:1.04em;margin-top:-1em;color:#495;'>"
        "Chaque couleur correspond à une catégorie d’acteurs, score moyen par dimension."
        "</div>", unsafe_allow_html=True
    )

if __name__ == "__main__" or "streamlit" in __name__:
    show_page_graphiques()
