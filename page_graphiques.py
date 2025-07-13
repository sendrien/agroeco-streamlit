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
            "Score": mean
        })
    df = pd.DataFrame(rows)
    return df

def show_page_graphiques():
    # --- RADAR PLOT ---
    st.markdown("<h3 style='color:#027368;'>Radar plot : Note globale des dimensions par catégories d'acteurs</h3>", unsafe_allow_html=True)
    radar_df = get_dimension_scores_per_categorie(dimensions, categories)
    labels = radar_df.columns.tolist()
    categories_labels = radar_df.index.tolist()

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

    # --- BAR CHART "NOTE GLOBALE PAR DIMENSION" ---
    st.markdown("<h3 style='color:#027368; margin-top:2em;'>Note globale par dimension</h3>", unsafe_allow_html=True)
    bar_df = get_global_scores_by_dimension(dimensions)
    # Pour afficher comme sur ton image (de haut en bas), on inverse l'ordre
    bar_df = bar_df.iloc[::-1].reset_index(drop=True)
    couleurs = [
        "#3B9CCC",  # Temporelle
        "#FFD600",  # Territoriale
        "#A5A5A5",  # Politique et sociale
        "#F39C12",  # Economique
        "#2980B9",  # Environnementale
    ]
    fig_bar = go.Figure(go.Bar(
        x=bar_df["Score"],
        y=bar_df["Dimension"],
        orientation="h",
        marker=dict(
            color=couleurs,
            line=dict(color="#ECECEC", width=1.6)
        ),
        text=bar_df["Score"].astype(str).str.replace('.', ','),
        textposition="outside",
        insidetextanchor="end",
        hoverinfo="none"
    ))

    fig_bar.update_layout(
        xaxis=dict(range=[2.35, 2.6], tickvals=[2.4, 2.5, 2.6], tickfont=dict(size=13), showgrid=False, color="white"),
        yaxis=dict(tickfont=dict(size=13), categoryorder="array", categoryarray=bar_df["Dimension"].tolist(), color="white"),
        plot_bgcolor="#232323",  # fond sombre
        paper_bgcolor="#232323",
        bargap=0.25,
        width=400,
        height=250,
        margin=dict(l=75, r=25, t=25, b=40),
        showlegend=False,
    )

    st.plotly_chart(fig_bar, use_container_width=False)

if __name__ == "__main__" or "streamlit" in __name__:
    show_page_graphiques()
