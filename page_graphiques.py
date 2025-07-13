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

    # --- Radar plot animé ---
    fig = go.Figure()

    for idx, cat in enumerate(categories_labels):
        values = radar_df.loc[cat].tolist()
        values += values[:1]
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=labels + [labels[0]],
            mode='lines+markers',
            name=cat,
            line=dict(width=3),
            opacity=0.85,
            marker=dict(size=5),
            visible=False if idx > 0 else True
        ))

    frames = [
        go.Frame(
            data=[go.Scatterpolar(
                r=radar_df.loc[categories_labels[j]].tolist() + [radar_df.loc[categories_labels[j]].tolist()[0]],
                theta=labels + [labels[0]],
                mode='lines+markers',
                name=categories_labels[j],
                line=dict(width=3),
                marker=dict(size=5),
                opacity=0.85,
                visible=True if j <= i else False
            ) for j in range(len(categories_labels))]
        )
        for i in range(len(categories_labels))
    ]

    fig.frames = frames

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 3.5], showticklabels=True, tickfont_size=13),
            angularaxis=dict(tickfont=dict(size=15)),
        ),
        showlegend=True,
        legend=dict(x=1.05, y=0.5, font=dict(size=12)),
        width=630, height=520, margin=dict(l=30, r=200, t=20, b=20),
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "y": 1.10,
            "x": 1.1,
            "xanchor": "right",
            "yanchor": "top",
            "buttons": [{
                "label": "Animer",
                "method": "animate",
                "args": [None, {"frame": {"duration": 600, "redraw": True},
                                "fromcurrent": True, "transition": {"duration": 200}}],
            }]
        }]
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- Bar chart moderne groupé ---
    st.markdown("<h3 style='color:#027368; margin-top:2em;'>Bar chart : Note globale des dimensions par catégories d'acteurs</h3>", unsafe_allow_html=True)
    bar_df = radar_df.copy()
    bar_fig = go.Figure()

    colors = ['#2980B9', '#F39C12', '#27AE60', '#C0392B', '#8E44AD']

    for i, dim in enumerate(bar_df.columns):
        bar_fig.add_trace(go.Bar(
            x=bar_df.index,
            y=bar_df[dim],
            name=dim,
            marker_color=colors[i % len(colors)],
            text=bar_df[dim],
            textposition='auto'
        ))

    bar_fig.update_layout(
        barmode='group',
        xaxis_title="Catégories d'acteurs",
        yaxis_title="Note (moyenne sur la dimension)",
        legend_title="Dimensions",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        width=710, height=400,
        margin=dict(l=10, r=10, t=20, b=40),
        font=dict(size=13),
        plot_bgcolor="#FAFAFA"
    )

    st.plotly_chart(bar_fig, use_container_width=True)

if __name__ == "__main__" or "streamlit" in __name__:
    show_page_graphiques()
