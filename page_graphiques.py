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

def radar_plot(radar_df, labels, categories_labels):
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
            visible=False if idx > 0 else True  # Premier visible au début
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
            "y": 1.13,
            "x": 1,
            "xanchor": "left",
            "yanchor": "top",
            "buttons": [{
                "label": "Dessiner",
                "method": "animate",
                "args": [None, {"frame": {"duration": 600, "redraw": True},
                                "fromcurrent": True, "transition": {"duration": 200}}]
            }],
            "bgcolor": "#fff",
            "bordercolor": "#027368",
            "borderwidth": 1.8,
            "font": {"color": "#027368", "size": 15}
        }]
    )
    return fig

def bar_chart_anim(radar_df, dim_labels, cat_labels, cat_idx=0):
    couleurs = [
        "#3B9CCC", "#F39C12", "#13B14A", "#FFD600", "#A5A5A5"
    ]
    bar_height = 0.65

    # Prendre la catégorie sélectionnée (cat_idx)
    scores = radar_df.iloc[cat_idx].values

    fig = go.Figure(
        data=[go.Bar(
            x=[None]*len(scores),
            y=dim_labels,
            orientation="h",
            marker=dict(
                color=couleurs,
                line=dict(color="#ECECEC", width=1.2)
            ),
            text=[""]*len(scores),
            textposition="outside",
            insidetextanchor="end",
            hoverinfo="none",
            width=[bar_height]*len(dim_labels)
        )],
        layout=go.Layout(
            xaxis=dict(range=[0, 3.2], showgrid=True, gridcolor="#eee", dtick=0.5, tickfont=dict(size=15)),
            yaxis=dict(tickfont=dict(size=18), color="#222"),
            height=410,
            margin=dict(l=110, r=60, t=60, b=60),
            plot_bgcolor="#fff", paper_bgcolor="#fff", showlegend=False,
            updatemenus=[{
                "type": "buttons",
                "showactive": False,
                "y": 1.25,
                "x": 0.9,
                "xanchor": "left",
                "yanchor": "top",
                "buttons": [{
                    "label": "Dessiner",
                    "method": "animate",
                    "args": [None, {
                        "frame": {"duration": 600, "redraw": True},
                        "fromcurrent": True, "transition": {"duration": 200}
                    }],
                }],
                "bgcolor": "#fff",
                "bordercolor": "#027368",
                "borderwidth": 1.8,
                "font": {"color": "#027368", "size": 15}
            }]
        )
    )

    # Frames : on ajoute les barres une à une
    frames = []
    for k in range(1, len(scores)+1):
        frame_scores = list(scores[:k]) + [None]*(len(scores)-k)
        frame_text = [str(v).replace('.', ',') if v is not None else '' for v in frame_scores]
        frames.append(go.Frame(
            data=[go.Bar(
                x=frame_scores,
                y=dim_labels,
                orientation="h",
                marker=dict(
                    color=couleurs,
                    line=dict(color="#ECECEC", width=1.2)
                ),
                text=frame_text,
                textposition="outside",
                insidetextanchor="end",
                hoverinfo="none",
                width=[bar_height]*len(dim_labels)
            )]
        ))
    fig.frames = frames

    # PAS d’annotation titre de catégorie au-dessus !
    fig.update_layout(annotations=[])
    return fig

def show_page_graphiques():
    st.markdown("<h3 style='color:#027368;'>Radar plot : Note globale des dimensions par catégories d'acteurs</h3>", unsafe_allow_html=True)
    radar_df = get_dimension_scores_per_categorie(dimensions, categories)
    labels = radar_df.columns.tolist()
    categories_labels = radar_df.index.tolist()

    # === Supprimer "Petits exploitants agricoles familiaux" ===
    categorie_a_supprimer = "Petits exploitants agricoles familiaux"
    if categorie_a_supprimer in radar_df.index:
        radar_df = radar_df.drop(categorie_a_supprimer)
        categories_labels = [cat for cat in categories_labels if cat != categorie_a_supprimer]

    # Config bar d'outils Plotly : supprime tous les boutons inutiles
    config = {
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': [
            'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d',
            'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 'hoverCompareCartesian',
            'zoom3d', 'pan3d', 'resetCameraDefault3d', 'resetCameraLastSave3d',
            'hoverClosest3d', 'orbitRotation', 'tableRotation', 'toggleSpikelines',
            'sendDataToCloud', 'toggleHover', 'resetViews', 'resetViewMapbox',
            'zoomInGeo', 'zoomOutGeo', 'resetGeo', 'hoverClosestGeo',
            'editInChartStudio'
        ],
        'modeBarButtonsToAdd': ['toImage', 'fullscreen'],
    }

    # 1. RADAR PLOT ANIMÉ (garde toutes les catégories, ou adapte si besoin)
    radar_fig = radar_plot(radar_df, labels, categories_labels)
    st.plotly_chart(radar_fig, use_container_width=True, config=config)

    # 2. BAR CHART ANIMÉ (par défaut sur la première catégorie restante, SANS titre)
    st.markdown("<h3 style='color:#027368; margin-top:2em;'>Bar chart : Note globale des dimensions par catégories d'acteurs</h3>", unsafe_allow_html=True)
    bar_fig = bar_chart_anim(radar_df, labels, categories_labels, cat_idx=0)
    st.plotly_chart(bar_fig, use_container_width=True, config=config)

if __name__ == "__main__" or "streamlit" in __name__:
    show_page_graphiques()
