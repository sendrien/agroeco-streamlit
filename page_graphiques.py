import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from data_osae import dimensions, categories, effectifs  # effectifs importés

# GÉNÉRATION DYNAMIQUE D'UNE PALETTE DE COULEURS (exemple : Plotly, Matplotlib, ou personnalisée)
def get_palette(n):
    """Retourne une palette de n couleurs distinctes, ici en s'appuyant sur Plotly."""
    from plotly.colors import qualitative
    base_palette = qualitative.Plotly + qualitative.Dark24 + qualitative.Light24
    # Si trop court, génère aléatoirement :
    if n <= len(base_palette):
        return base_palette[:n]
    else:
        # Génère des couleurs random si n > palette
        import random
        def random_color(): return '#'+''.join(random.choices('0123456789ABCDEF', k=6))
        return [random_color() for _ in range(n)]

def get_paletteeffectif(n):
    from plotly.colors import qualitative
    base = qualitative.Plotly + qualitative.Dark24 + qualitative.Light24
    return base[:n] if n <= len(base) else base + [f'#{np.random.randint(0,0xFFFFFF):06X}' for _ in range(n)]


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
            mean_score = round(sum(scores) / len(scores), 2) if scores else None
            cat_scores.append(mean_score)
        data.append(cat_scores)
    df = pd.DataFrame(
        data,
        columns=[dim["nom"].replace("Dimension ", "") for dim in dimensions],
        index=categories
    )
    return df

def radar_plot(radar_df, labels, categories_labels):
    palette = get_palette(len(categories_labels))
    fig = go.Figure()
    for idx, cat in enumerate(categories_labels):
        values = radar_df.loc[cat].tolist()
        values += values[:1]
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=labels + [labels[0]],
            mode='lines+markers',
            name=cat,
            line=dict(width=3, color=palette[idx]),
            marker=dict(size=5, color=palette[idx]),
            opacity=0.85,
            #marker=dict(size=5),
            visible=False if idx > 0 else True
        ))
    frames = [
        go.Frame(
            data=[go.Scatterpolar(
                r=radar_df.loc[categories_labels[j]].tolist() + [radar_df.loc[categories_labels[j]].tolist()[0]],
                theta=labels + [labels[0]],
                mode='lines+markers',
                name=categories_labels[j],
                line=dict(width=3, color=palette[j]),
                marker=dict(size=5, color=palette[j]),
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
            "x": 0,
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
    bar_palette = get_palette(len(dim_labels))
    bar_height = 0.65

    scores = radar_df.iloc[cat_idx].values

    fig = go.Figure(
        data=[go.Bar(
            x=[None]*len(scores),
            y=dim_labels,
            orientation="h",
            marker=dict(
                color=bar_palette,
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
                "x": -0.084,
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
                    color=bar_palette,
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

    fig.update_layout(annotations=[])
    return fig




def get_effectifs_df(effectifs, dimensions, categories):
    return pd.DataFrame(
        effectifs,
        columns=[d["nom"].replace("Dimension ", "") for d in dimensions],
        index=categories
    )

def bar_effectifs_stacked_anim(eff_df):
    dims = eff_df.columns.tolist()
    cats = eff_df.index.tolist()
    palette = get_paletteeffectif(len(dims))

    # Base figure avec zéro valeurs
    fig = go.Figure(
        data=[
            go.Bar(
                y=cats,
                x=[0] * len(cats),
                name=dims[i],
                orientation='h',
                marker_color=palette[i],
                text=[''] * len(cats),
                textposition='inside'
            ) for i in range(len(dims))
        ],
        layout=go.Layout(
            barmode='stack',
            height=480,
            margin=dict(l=160, r=40, t=60, b=40),
            xaxis=dict(title='Nombre de répondants', dtick=50, range=[0, eff_df.values.sum(axis=1).max() * 1.05]),
            yaxis=dict(autorange='reversed'),
            legend=dict(orientation='h', y=-0.15),
            updatemenus=[{
                "type": "buttons",
                "showactive": False,
                "y": 1.25,
                "x": -0.084,
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

    # Génération des frames une dimension à la fois
    frames = []
    for k in range(1, len(dims) + 1):
        frame_data = []
        for i in range(len(dims)):
            vals = eff_df.iloc[:, i].values if i < k else [0] * len(cats)
            frame_data.append(go.Bar(
                y=cats,
                x=vals,
                name=dims[i],
                orientation='h',
                marker_color=palette[i],
                text=[str(v) for v in vals],
                textposition='inside'
            ))
        frames.append(go.Frame(data=frame_data, name=str(k)))

    fig.frames = frames
    return fig







def show_page_graphiques():
    st.markdown("<h3 style='color:#027368;'>Radar plot : Note globale des dimensions par catégories d'acteurs</h3>", unsafe_allow_html=True)
    radar_df = get_dimension_scores_per_categorie(dimensions, categories)
    labels = radar_df.columns.tolist()
    categories_labels = radar_df.index.tolist()

    categorie_a_supprimer = "Petits exploitants agricoles familiaux"
    if categorie_a_supprimer in radar_df.index:
        radar_df = radar_df.drop(categorie_a_supprimer)
        categories_labels = [cat for cat in categories_labels if cat != categorie_a_supprimer]

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

    radar_fig = radar_plot(radar_df, labels, categories_labels)
    st.plotly_chart(radar_fig, use_container_width=True, config=config)

    st.markdown("<h3 style='color:#027368; margin-top:2em;'>Bar chart : Note globale des dimensions par catégories d'acteurs</h3>", unsafe_allow_html=True)
    bar_fig = bar_chart_anim(radar_df, labels, categories_labels, cat_idx=0)
    st.plotly_chart(bar_fig, use_container_width=True, config=config)

    # --- Nouveau graphique effectifs ---
    st.markdown("<h3 style='color:#027368; margin-top:2em;'>Nombre de répondants par dimension par catégories d’acteurs</h3>", unsafe_allow_html=True)

    eff_df = get_effectifs_df(effectifs, dimensions, categories)
    eff_fig = bar_effectifs_stacked_anim(eff_df)

    

    st.plotly_chart(eff_fig, use_container_width=True, config=config)

if __name__ == "__main__" or "streamlit" in __name__:
    show_page_graphiques()
