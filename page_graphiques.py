import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from data_osae import dimensions, categories, effectifs, poids_relatif

# ===================== Palette =====================
def get_palette(n):
    from plotly.colors import qualitative
    base_palette = qualitative.Plotly + qualitative.Dark24 + qualitative.Light24
    if n <= len(base_palette): return base_palette[:n]
    import random
    return ['#' + ''.join(random.choices('0123456789ABCDEF', k=6)) for _ in range(n)]

def get_paletteeffectif(n):
    from plotly.colors import qualitative
    base = qualitative.Plotly + qualitative.Dark24 + qualitative.Light24
    return base[:n] if n <= len(base) else base + [f'#{np.random.randint(0,0xFFFFFF):06X}' for _ in range(n)]

# ===================== Helpers =====================
def get_plotly_config():
    return {
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToAdd': ['toImage','fullscreen'],
        'modeBarButtonsToRemove': ['lasso2d','select2d','zoom3d','pan3d','orbitRotation','tableRotation',
                                   'zoomInGeo','zoomOutGeo','resetGeo','hoverClosestGeo','editInChartStudio']
    }

def themeify(fig):
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Segoe UI, Roboto, Arial, sans-serif", size=14, color="#0F172A"),
        paper_bgcolor="#fff", plot_bgcolor="#fff",
        title_x=0.02, title_font=dict(size=18)
    )
    return fig

def get_dimension_scores_per_categorie(dimensions, categories):
    data = []
    for i, cat in enumerate(categories):
        cat_scores = []
        for dim in dimensions:
            scores = [v for indic in dim["indicateurs"] for v in ([indic["scores"][i]] if i < len(indic["scores"]) else []) if v is not None]
            mean_score = round(sum(scores) / len(scores), 2) if scores else None
            cat_scores.append(mean_score)
        data.append(cat_scores)
    return pd.DataFrame(
        data,
        columns=[dim["nom"].replace("Dimension ", "") for dim in dimensions],
        index=categories
    )

# ===================== Radar =====================
def radar_plot(radar_df, labels, categories_labels):
    palette = get_palette(len(categories_labels))
    fig = go.Figure()
    for idx, cat in enumerate(categories_labels):
        values = radar_df.loc[cat].tolist(); values += values[:1]
        fig.add_trace(go.Scatterpolar(
            r=values, theta=labels + [labels[0]], mode='lines+markers', name=cat,
            line=dict(width=3, color=palette[idx]), marker=dict(size=5, color=palette[idx]),
            opacity=0.9, visible=False if idx > 0 else True
        ))
    frames = [
        go.Frame(
            data=[go.Scatterpolar(
                r=radar_df.loc[categories_labels[j]].tolist() + [radar_df.loc[categories_labels[j]].tolist()[0]],
                theta=labels + [labels[0]], mode='lines+markers', name=categories_labels[j],
                line=dict(width=3, color=palette[j]), marker=dict(size=5, color=palette[j]),
                opacity=0.9, visible=True if j <= i else False
            ) for j in range(len(categories_labels))]
        ) for i in range(len(categories_labels))
    ]
    fig.frames = frames
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 3.5], tickfont_size=13),
                   angularaxis=dict(tickfont=dict(size=15))),
        showlegend=True, legend=dict(x=1.02, y=0.98, xanchor="left"),
        margin=dict(l=30, r=220, t=20, b=20),
        updatemenus=[{
            "type":"buttons","showactive":False,"y":1.15,"x":0,"xanchor":"left","yanchor":"top",
            "buttons":[{"label":"Dessiner","method":"animate",
                        "args":[None,{"frame":{"duration":600,"redraw":True},"fromcurrent":True,"transition":{"duration":200}}]}],
            "bgcolor":"#fff","bordercolor":"#027368","borderwidth":1.8,"font":{"color":"#027368","size":15}
        }]
    )
    return themeify(fig)

# ===================== Bar animé =====================
def bar_chart_anim(radar_df, dim_labels, cat_labels, cat_idx=0):
    bar_palette = get_palette(len(dim_labels))
    scores = radar_df.iloc[cat_idx].values
    fig = go.Figure(
        data=[go.Bar(
            x=[None]*len(scores), y=dim_labels, orientation="h",
            marker=dict(color=bar_palette, line=dict(color="#ECECEC", width=1.2)),
            text=[""]*len(scores), textposition="outside", hoverinfo="none",
            width=[0.65]*len(dim_labels)
        )]
    )
    frames=[]
    for k in range(1, len(scores)+1):
        frame_scores = list(scores[:k]) + [None]*(len(scores)-k)
        frame_text = [("" if v is None else str(v).replace('.',',')) for v in frame_scores]
        frames.append(go.Frame(data=[go.Bar(x=frame_scores, y=dim_labels, orientation="h",
                                            marker=dict(color=bar_palette, line=dict(color="#ECECEC", width=1.2)),
                                            text=frame_text, textposition="outside")]))
    fig.frames=frames
    fig.update_layout(
        xaxis=dict(range=[0,3.2], gridcolor="#eee", dtick=0.5),
        yaxis=dict(tickfont=dict(size=16), color="#222"),
        height=420, margin=dict(l=120, r=60, t=60, b=60),
        showlegend=False, updatemenus=[{
            "type":"buttons","showactive":False,"y":1.23,"x":-0.08,"xanchor":"left","yanchor":"top",
            "buttons":[{"label":"Dessiner","method":"animate","args":[None,{"frame":{"duration":600,"redraw":True},"fromcurrent":True,"transition":{"duration":200}}]}],
            "bgcolor":"#fff","bordercolor":"#027368","borderwidth":1.8,"font":{"color":"#027368","size":15}
        }]
    )
    return themeify(fig)

# ===================== Effectifs empilés =====================
def get_effectifs_df(effectifs, dimensions, categories):
    return pd.DataFrame(effectifs,
        columns=[d["nom"].replace("Dimension ", "") for d in dimensions],
        index=categories
    )

def bar_effectifs_stacked_anim(eff_df):
    dims = eff_df.columns.tolist(); cats = eff_df.index.tolist()
    palette = get_paletteeffectif(len(dims))
    fig = go.Figure(data=[
        go.Bar(y=cats, x=[0]*len(cats), name=dims[i], orientation='h',
               marker_color=palette[i], text=['']*len(cats), textposition='inside')
        for i in range(len(dims))
    ])
    frames=[]
    for k in range(1, len(dims)+1):
        frame_data=[]
        for i in range(len(dims)):
            vals = eff_df.iloc[:, i].values if i < k else [0]*len(cats)
            frame_data.append(go.Bar(y=cats, x=vals, name=dims[i], orientation='h',
                                     marker_color=palette[i], text=[str(v) for v in vals],
                                     textposition='inside'))
        frames.append(go.Frame(data=frame_data, name=str(k)))
    fig.frames=frames
    fig.update_layout(
        barmode='stack', height=480, margin=dict(l=160, r=40, t=60, b=40),
        xaxis=dict(title='Nombre de répondants', dtick=50, range=[0, eff_df.values.sum(axis=1).max()*1.05]),
        yaxis=dict(autorange='reversed'),
        legend=dict(orientation='h', y=-0.18),
        updatemenus=[{
            "type":"buttons","showactive":False,"y":1.12,"x":-0.17,"xanchor":"left","yanchor":"top",
            "buttons":[{"label":"Dessiner","method":"animate","args":[None,{"frame":{"duration":600,"redraw":True},"fromcurrent":True,"transition":{"duration":200}}]}],
            "bgcolor":"#fff","bordercolor":"#027368","borderwidth":1.5,"font":{"color":"#027368","size":14}
        }]
    )
    return themeify(fig)

# ===================== Camembert animé =====================
def pie_poids_relatif_anim(categories, poids_relatif):
    labels = categories; values = poids_relatif; palette = get_palette(len(labels))
    fig = go.Figure(data=[go.Pie(labels=labels, values=[0]*len(values),
                                 textinfo='label+percent', textposition='outside',
                                 marker=dict(colors=palette, line=dict(color='#fff', width=1)),
                                 sort=False)])
    frames=[]; cumulative=[0]*len(values)
    for i in range(len(values)):
        cumulative[i]=values[i]
        frames.append(go.Frame(data=[go.Pie(values=cumulative)]))
    fig.frames=frames
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20), height=500, showlegend=True,
        legend=dict(orientation='v', x=0.02, y=0.98, font=dict(size=12)),
        updatemenus=[{
            "type":"buttons","showactive":False,"x":0.02,"y":1.08,"xanchor":"left","yanchor":"top",
            "buttons":[{"label":"Dessiner","method":"animate","args":[None,{"frame":{"duration":400,"redraw":True},"fromcurrent":True,"transition":{"duration":200}}]}],
            "font":{"size":14,"color":"#027368"}, "bgcolor":"#fff", "bordercolor":"#027368", "borderwidth":1.5
        }]
    )
    return themeify(fig)

# ===================== Page =====================
def show_page_graphiques():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#027368;margin:0 0 10px 0;'>Radar plot · Note globale des dimensions par catégories d'acteurs</h3>", unsafe_allow_html=True)
    radar_df = get_dimension_scores_per_categorie(dimensions, categories)
    labels = radar_df.columns.tolist()
    categories_labels = radar_df.index.tolist()

    # Exemple de filtrage : suppression éventuelle d’une catégorie
    categorie_a_supprimer = "Petits exploitants agricoles familiaux"
    if categorie_a_supprimer in radar_df.index:
        radar_df = radar_df.drop(categorie_a_supprimer)
        categories_labels = [cat for cat in categories_labels if cat != categorie_a_supprimer]

    radar_fig = radar_plot(radar_df, labels, categories_labels)
    st.plotly_chart(radar_fig, use_container_width=True, config=get_plotly_config())
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card' style='margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#027368;margin:0 0 10px 0;'>Bar chart · Note globale des dimensions par catégories d'acteurs</h3>", unsafe_allow_html=True)
    bar_fig = bar_chart_anim(radar_df, labels, categories_labels, cat_idx=0)
    st.plotly_chart(bar_fig, use_container_width=True, config=get_plotly_config())
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card' style='margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#027368;margin:0 0 10px 0;'>Nombre de répondants par dimension et par catégorie d’acteurs</h3>", unsafe_allow_html=True)
    eff_df = get_effectifs_df(effectifs, dimensions, categories)
    eff_fig = bar_effectifs_stacked_anim(eff_df)
    st.plotly_chart(eff_fig, use_container_width=True, config=get_plotly_config())
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card' style='margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#027368;margin:0 0 10px 0;'>Poids relatif des acteurs dans le processus de transition (en %)</h3>", unsafe_allow_html=True)
    pie_fig = pie_poids_relatif_anim(categories, poids_relatif)
    st.plotly_chart(pie_fig, use_container_width=True, config=get_plotly_config())
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__" or "streamlit" in __name__:
    show_page_graphiques()
