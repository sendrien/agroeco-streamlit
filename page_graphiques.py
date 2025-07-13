import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from data_osae import dimensions, categories, effectifs  # ← ajoute effectifs

# Génération palette
def get_palette(n):
    from plotly.colors import qualitative
    base = qualitative.Plotly + qualitative.Dark24 + qualitative.Light24
    if n <= len(base):
        return base[:n]
    import random
    return ['#' + ''.join(random.choices('0123456789ABCDEF', k=6)) for _ in range(n)]

def get_dimension_scores_per_categorie(dimensions, categories):
    data = []
    for i, cat in enumerate(categories):
        cat_scores = []
        for dim in dimensions:
            vals = [v for indic in dim["indicateurs"] 
                    for v in ([indic["scores"][i]] if i < len(indic["scores"]) else [None]) 
                    if v is not None]
            cat_scores.append(round(sum(vals)/len(vals),2) if vals else None)
        data.append(cat_scores)
    return pd.DataFrame(data,
                        columns=[dim["nom"].replace("Dimension ", "") for dim in dimensions],
                        index=categories)

def radar_plot(radar_df):
    labels = radar_df.columns.tolist()
    cat_labels = radar_df.index.tolist()
    palette = get_palette(len(cat_labels))
    fig = go.Figure()
    for idx, cat in enumerate(cat_labels):
        vals = radar_df.loc[cat].tolist() + [radar_df.loc[cat].iloc[0]]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=labels + [labels[0]],
            mode='lines+markers',
            name=cat,
            line=dict(color=palette[idx], width=3),
            marker=dict(color=palette[idx], size=5),
            visible=False if idx > 0 else True
        ))
    frames = [
        go.Frame(data=[
            go.Scatterpolar(
                r=radar_df.loc[cat].tolist() + [radar_df.loc[cat].iloc[0]],
                theta=labels + [labels[0]],
                line=dict(color=palette[j], width=3),
                marker=dict(color=palette[j], size=5),
                mode='lines+markers',
                name=cat
            )
        ], name=cat)
        for j, cat in enumerate(cat_labels)
    ]
    fig.frames = frames
    fig.update_layout(
        polar=dict(radialaxis=dict(range=[0,3.5]), angularaxis=dict(tickfont_size=13)),
        width=500, height=480,
        updatemenus=[dict(type="buttons", showactive=False,
                           buttons=[dict(label="Dessiner", method="animate", args=[None])])]
    )
    return fig

def bar_anim(df, title):
    dim = df.columns.tolist()
    cats = df.index.tolist()
    palette = get_palette(len(dim))
    fig = go.Figure(
        data=[go.Bar(x=[None]*len(dim), y=dim, orientation='h', marker=dict(color=palette))],
        frames=[go.Frame(
            data=[go.Bar(x=df.iloc[i].values, y=dim, orientation='h', marker=dict(color=palette))],
            name=cat
        ) for i, cat in enumerate(cats)]
    )
    fig.update_layout(
        title=title,
        xaxis=dict(range=[0, df.max().max()*1.1]),
        height=350, width=500,
        updatemenus=[dict(type="buttons", showactive=False,
                           buttons=[dict(label="Dessiner", method="animate", args=[None])])]
    )
    return fig

def show_page_graphiques():
    radar_df = get_dimension_scores_per_categorie(dimensions, categories)

    st.markdown("### Radar animé – Note par dimension & catégorie")
    st.plotly_chart(radar_plot(radar_df), use_container_width=True)

    st.markdown("### Bar chart animé – Note par dimension")
    st.plotly_chart(bar_anim(radar_df, "Notes moyennes par dimension"), use_container_width=True)

    # --- Ajout du graphique "effectifs"
    eff_df = pd.DataFrame(effectifs,
                           columns=radar_df.columns, index=radar_df.index)
    st.markdown("### Nombre de répondants par dimension & catégorie")
    st.plotly_chart(bar_anim(eff_df, "Effectifs par dimension et catégorie"), use_container_width=True)

if __name__ == "__main__":
    show_page_graphiques()
