import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data_osae import dimensions

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

def show_bar_chart_score_by_dimension():
    df = get_global_scores_by_dimension(dimensions)
    # Tri pour l'affichage (de haut en bas, comme l'image)
    df = df.iloc[::-1].reset_index(drop=True)
    couleurs = [
        "#2980B9",  # Bleu
        "#F39C12",  # Orange
        "#A5A5A5",  # Gris
        "#FFD600",  # Jaune
        "#3B9CCC",  # Bleu clair
    ]

    fig = go.Figure(go.Bar(
        x=df["Score"],
        y=df["Dimension"],
        orientation="h",
        marker=dict(
            color=couleurs,
            line=dict(color="#ECECEC", width=1.6)
        ),
        text=df["Score"].astype(str).str.replace('.', ','),
        textposition="outside",
        insidetextanchor="end",
        hoverinfo="none"
    ))

    fig.update_layout(
        title="Note globale par dimension",
        title_font=dict(size=18, family="Arial", color="#222", bold=True),
        xaxis=dict(range=[2.35, 2.6], tickvals=[2.4, 2.5, 2.6], tickfont=dict(size=13), showgrid=False),
        yaxis=dict(tickfont=dict(size=14), categoryorder="array", categoryarray=df["Dimension"].tolist()),
        plot_bgcolor="#222",
        paper_bgcolor="#222",
        bargap=0.25,
        width=410,
        height=260,
        margin=dict(l=100, r=40, t=50, b=40),
        showlegend=False,
    )

    # Couleur du texte du titre et axes (blanc, pour fond sombre)
    fig.update_layout(
        title_font_color="white",
        xaxis_color="white",
        yaxis_color="white",
    )

    st.plotly_chart(fig, use_container_width=False)

# Pour afficher le graphique sur ta page
if __name__ == "__main__" or "streamlit" in __name__:
    show_bar_chart_score_by_dimension()
