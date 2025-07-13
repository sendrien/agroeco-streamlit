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
    st.markdown("<h3 style='color:#027368;'>Barres animées : Note globale des dimensions par catégories d'acteurs</h3>", unsafe_allow_html=True)
    radar_df = get_dimension_scores_per_categorie(dimensions, categories)
    dim_labels = radar_df.columns.tolist()
    cat_labels = radar_df.index.tolist()
    couleurs = [
        "#3B9CCC", "#F39C12", "#13B14A", "#FFD600", "#A5A5A5", "#2980B9", "#DE3163"
    ]

    # Initial (première catégorie)
    cat_idx = 0
    scores = radar_df.iloc[cat_idx].values
    fig = go.Figure(
        data=[go.Bar(
            x=scores,
            y=dim_labels,
            orientation="h",
            marker=dict(color=couleurs[:len(dim_labels)], line=dict(color="#ECECEC", width=1.2)),
            text=[str(v).replace('.', ',') if v is not None else '' for v in scores],
            textposition="outside",
            insidetextanchor="end",
            hoverinfo="none"
        )],
        layout=go.Layout(
            xaxis=dict(range=[min(radar_df.min())-0.1, max(radar_df.max())+0.1], showgrid=False, color="#222"),
            yaxis=dict(tickfont=dict(size=13), color="#222"),
            width=450, height=290, margin=dict(l=90, r=30, t=20, b=40),
            plot_bgcolor="#fff", paper_bgcolor="#fff", showlegend=False,
            updatemenus=[{
                "type": "buttons",
                "showactive": False,
                "y": 1.13,
                "x": 1.16,
                "xanchor": "right",
                "yanchor": "top",
                "buttons": [{
                    "label": "Animer",
                    "method": "animate",
                    "args": [None, {
                        "frame": {"duration": 900, "redraw": True},
                        "fromcurrent": True, "transition": {"duration": 350}
                    }],
                }]
            }]
        ),
        frames=[
            go.Frame(
                data=[go.Bar(
                    x=radar_df.iloc[i].values,
                    y=dim_labels,
                    orientation="h",
                    marker=dict(color=couleurs[:len(dim_labels)], line=dict(color="#ECECEC", width=1.2)),
                    text=[str(v).replace('.', ',') if v is not None else '' for v in radar_df.iloc[i].values],
                    textposition="outside",
                    insidetextanchor="end",
                    hoverinfo="none"
                )],
                name=cat_labels[i],
                layout=go.Layout(
                    annotations=[
                        dict(
                            xref="paper", yref="paper",
                            x=1.15, y=0.97, showarrow=False,
                            text=f"<b>{cat_labels[i]}</b>", font=dict(size=17, color=couleurs[i%len(couleurs)])
                        )
                    ]
                )
            )
            for i in range(len(cat_labels))
        ]
    )

    # Affiche la catégorie courante à droite (comme dans le slide)
    fig.update_layout(
        annotations=[
            dict(
                xref="paper", yref="paper",
                x=1.15, y=0.97, showarrow=False,
                text=f"<b>{cat_labels[cat_idx]}</b>", font=dict(size=17, color=couleurs[cat_idx%len(couleurs)])
            )
        ]
    )

    st.plotly_chart(fig, use_container_width=False)

if __name__ == "__main__" or "streamlit" in __name__:
    show_page_graphiques()
