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
            "y": 1.10,
            "x": 1.1,
            "xanchor": "right",
            "yanchor": "top",
            "buttons": [{
                "label": "Animer",
                "method": "animate",
                "args": [None, {"frame": {"duration": 600, "redraw": True},
                                "fromcurrent": True, "transition": {"duration": 200}}]
            }]
        }]
    )
    return fig

def bar_chart_anim(radar_df, dim_labels, cat_labels):
    couleurs = [
        "#3B9CCC", "#F39C12", "#13B14A", "#FFD600", "#A5A5A5", "#2980B9", "#DE3163"
    ]
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
            xaxis=dict(range=[min(radar_df.min())-0.1, max(radar_df.max())+0.1], showgrid=False, color="#222", title=""),
            yaxis=dict(tickfont=dict(size=13), color="#222", title=""),
            width=480, height=280, margin=dict(l=90, r=40, t=50, b=40),
            plot_bgcolor="#fff", paper_bgcolor="#fff", showlegend=False,
            updatemenus=[{
                "type": "buttons",
                "showactive": False,
                "y": 1.16,
                "x": 1.12,
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
                            x=0.0, y=1.18, showarrow=False,
                            xanchor="left", yanchor="top",
                            text=f"<span style='font-size: 18px; font-weight: 600; color: {couleurs[i%len(couleurs)]}'>{cat_labels[i]}</span>",
                        )
                    ]
                )
            )
            for i in range(len(cat_labels))
        ]
    )

    # Titre de la catégorie (au-dessus du graphique, sans chevauchement, bien lisible)
    fig.update_layout(
        annotations=[
            dict(
                xref="paper", yref="paper",
                x=0.0, y=1.18, showarrow=False,
                xanchor="left", yanchor="top",
                text=f"<span style='font-size: 18px; font-weight: 600; color: {couleurs[cat_idx%len(couleurs)]}'>{cat_labels[cat_idx]}</span>",
            )
        ]
    )
    return fig


def show_page_graphiques():
    st.markdown("<h3 style='color:#027368;'>Radar plot : Note globale des dimensions par catégories d'acteurs</h3>", unsafe_allow_html=True)
    radar_df = get_dimension_scores_per_categorie(dimensions, categories)
    labels = radar_df.columns.tolist()
    categories_labels = radar_df.index.tolist()

    # 1. RADAR PLOT ANIMÉ
    radar_fig = radar_plot(radar_df, labels, categories_labels)
    st.plotly_chart(radar_fig, use_container_width=True)

    # 2. BAR CHART ANIMÉ
    st.markdown("<h3 style='color:#027368; margin-top:2em;'>Bar chart : Note globale des dimensions par catégories d'acteurs</h3>", unsafe_allow_html=True)
    bar_fig = bar_chart_anim(radar_df, labels, categories_labels)
    st.plotly_chart(bar_fig, use_container_width=False)

if __name__ == "__main__" or "streamlit" in __name__:
    show_page_graphiques()
