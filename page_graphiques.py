import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
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
    colors = [
        "#4e79a7", "#f28e2b", "#e15759", "#76b7b2", 
        "#59a14f", "#edc948", "#b07aa1"
    ]

    # Animation : apparition progressive des courbes
    frames = []
    data_init = []
    for i, cat in enumerate(categories_labels):
        values = radar_df.loc[cat].tolist() + [radar_df.loc[cat].tolist()[0]]
        trace = go.Scatterpolar(
            r=values,
            theta=labels + [labels[0]],
            mode='lines+markers',
            name=cat,
            line=dict(width=3, color=colors[i % len(colors)]),
            marker=dict(size=7),
            opacity=0.9 if i == 0 else 0,  # Seule la première courbe affichée au début
        )
        data_init.append(trace)

    for k in range(1, len(categories_labels)+1):
        data = []
        for i, cat in enumerate(categories_labels):
            values = radar_df.loc[cat].tolist() + [radar_df.loc[cat].tolist()[0]]
            data.append(go.Scatterpolar(
                r=values,
                theta=labels + [labels[0]],
                mode='lines+markers',
                name=cat,
                line=dict(width=3, color=colors[i % len(colors)]),
                marker=dict(size=7),
                opacity=0.9 if i < k else 0  # On affiche progressivement
            ))
        frames.append(go.Frame(data=data, name=str(k)))

    fig = go.Figure(
        data=data_init,
        frames=frames
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 3.5], showticklabels=True, tickfont_size=13),
            angularaxis=dict(tickfont=dict(size=16), rotation=80, direction='clockwise'),
        ),
        showlegend=True,
        legend=dict(x=1.05, y=0.5, font=dict(size=12), borderwidth=0, orientation='v'),
        width=680,
        height=520,
        margin=dict(l=30, r=180, t=20, b=20),
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "y": 1.1,
            "x": 1.13,
            "xanchor": "right",
            "yanchor": "top",
            "buttons": [{
                "label": "Animer",
                "method": "animate",
                "args": [None, {"frame": {"duration": 700, "redraw": True},
                                "fromcurrent": True, "transition": {"duration": 250}}],
            }]
        }]
    )
    st.plotly_chart(fig, use_container_width=False)

if __name__ == "__main__" or "streamlit" in __name__:
    show_page_graphiques()
