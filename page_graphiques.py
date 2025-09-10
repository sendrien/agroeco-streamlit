import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.colors import qualitative
from data_osae import dimensions, categories, effectifs, poids_relatif

# ========================== Palette ==========================
def get_palette(n: int):
    base = qualitative.Plotly + qualitative.Dark24 + qualitative.Light24
    if n <= len(base):
        return base[:n]
    rng = np.random.default_rng(7)
    return [f'#{int(c):06X}' for c in rng.integers(0, 0xFFFFFF, size=n)]

def get_palette_effectif(n: int):
    base = qualitative.Plotly + qualitative.Dark24 + qualitative.Light24
    return base[:n] if n <= len(base) else base + get_palette(n - len(base))

# ========================== Helpers ==========================
def plot_config():
    return {
        "displayModeBar": True,
        "displaylogo": False,
        "modeBarButtonsToAdd": ["toImage", "fullscreen"],
        "modeBarButtonsToRemove": [
            "lasso2d","select2d","zoom3d","pan3d","orbitRotation","tableRotation",
            "zoomInGeo","zoomOutGeo","resetGeo","hoverClosestGeo","editInChartStudio"
        ],
    }

def themeify(fig: go.Figure):
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Segoe UI, Roboto, Arial, sans-serif", size=14, color="#0F172A"),
        paper_bgcolor="#fff",
        plot_bgcolor="#fff",
    )
    return fig

def add_title_and_play(fig: go.Figure, title: str, btn_y: float = 1.22, btn_x: float = 0.0):
    """Ajoute un titre interne + bouton 'Dessiner' au-dessus du graphe, sans chevauchement."""
    # Titre
    fig.add_annotation(
        text=title,
        xref="paper", yref="paper", x=0, y=1.28,
        showarrow=False, align="left",
        font=dict(size=18, color="#0D2A27")
    )
    # Espace top suffisant
    m = fig.layout.margin or dict()
    fig.update_layout(margin=dict(l=m.get("l", 30), r=m.get("r", 40), t=max(110, m.get("t", 80)), b=m.get("b", 40)))

    # Bouton d’animation
    fig.update_layout(
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            x=btn_x, y=btn_y, xanchor="left", yanchor="top",
            buttons=[dict(
                label="Dessiner",
                method="animate",
                args=[None, {"frame": {"duration": 600, "redraw": True},
                             "fromcurrent": True,
                             "transition": {"duration": 200}}]
            )],
            bgcolor="#fff",
            bordercolor="#027368",
            borderwidth=1.6,
            font=dict(color="#027368", size=14),
            pad=dict(t=2, r=2, b=2, l=2)
        )]
    )
    return fig

def get_dimension_scores_per_categorie(dimensions, categories):
    data = []
    for i, _cat in enumerate(categories):
        row = []
        for dim in dimensions:
            vals = []
            for indic in dim["indicateurs"]:
                if i < len(indic["scores"]):
                    v = indic["scores"][i]
                    if v is not None:
                        vals.append(v)
            row.append(round(sum(vals) / len(vals), 2) if vals else None)
        data.append(row)
    return pd.DataFrame(
        data,
        columns=[d["nom"].replace("Dimension ", "") for d in dimensions],
        index=categories
    )

# ========================== Radar ==========================
def radar_plot(radar_df: pd.DataFrame):
    labels = radar_df.columns.tolist()
    cats   = radar_df.index.tolist()
    palette = get_palette(len(cats))

    fig = go.Figure()
    for idx, cat in enumerate(cats):
        vals = radar_df.loc[cat].tolist()
        vals += vals[:1]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=labels + [labels[0]],
            mode="lines+markers", name=cat,
            line=dict(width=3, color=palette[idx]),
            marker=dict(size=5, color=palette[idx]),
            opacity=0.9,
            visible=(idx == 0)
        ))
    frames = []
    for i in range(len(cats)):
        frame_data = []
        for j in range(len(cats)):
            vals = radar_df.loc[cats[j]].tolist() + [radar_df.loc[cats[j]].tolist()[0]]
            frame_data.append(go.Scatterpolar(
                r=vals, theta=labels + [labels[0]],
                mode="lines+markers", name=cats[j],
                line=dict(width=3, color=palette[j]),
                marker=dict(size=5, color=palette[j]),
                opacity=0.9, visible=(j <= i)
            ))
        frames.append(go.Frame(data=frame_data, name=f"f{i}"))
    fig.frames = frames

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 3.5], tickfont_size=13),
            angularaxis=dict(tickfont=dict(size=15))
        ),
        showlegend=True,
        legend=dict(x=1.02, y=0.98, xanchor="left"),
        margin=dict(l=30, r=220, t=20, b=20),
    )
    themeify(fig)
    add_title_and_play(fig, "Radar plot · Note globale des dimensions par catégories d'acteurs")
    return fig

# ========================== Bar animé ==========================
def bar_chart_anim(radar_df: pd.DataFrame, cat_idx: int = 0):
    dim_labels = radar_df.columns.tolist()
    scores     = radar_df.iloc[cat_idx].values
    palette    = get_palette(len(dim_labels))

    base = go.Figure(data=[go.Bar(
        x=[None]*len(scores), y=dim_labels, orientation="h",
        marker=dict(color=palette, line=dict(color="#ECECEC", width=1.2)),
        text=[""]*len(scores), textposition="outside", hoverinfo="none",
        width=[0.65]*len(dim_labels)
    )])
    frames=[]
    for k in range(1, len(scores)+1):
        xs = list(scores[:k]) + [None]*(len(scores)-k)
        txt = [("" if v is None else str(v).replace('.', ',')) for v in xs]
        frames.append(go.Frame(data=[go.Bar(
            x=xs, y=dim_labels, orientation="h",
            marker=dict(color=palette, line=dict(color="#ECECEC", width=1.2)),
            text=txt, textposition="outside"
        )], name=f"s{k}"))
    base.frames = frames

    base.update_layout(
        xaxis=dict(range=[0, 3.2], gridcolor="#eee", dtick=0.5),
        yaxis=dict(tickfont=dict(size=16), color="#222"),
        height=430, margin=dict(l=130, r=60, t=60, b=60),
        showlegend=False,
    )
    themeify(base)
    add_title_and_play(base, "Bar chart · Note globale des dimensions par catégories d'acteurs", btn_x=-0.02, btn_y=1.22)
    return base

# ========================== Effectifs empilés ==========================
def get_effectifs_df(effectifs, dimensions, categories):
    return pd.DataFrame(
        effectifs,
        columns=[d["nom"].replace("Dimension ", "") for d in dimensions],
        index=categories
    )

def bar_effectifs_stacked_anim(eff_df: pd.DataFrame):
    dims = eff_df.columns.tolist()
    cats = eff_df.index.tolist()
    palette = get_palette_effectif(len(dims))

    fig = go.Figure(data=[
        go.Bar(y=cats, x=[0]*len(cats), name=dims[i], orientation="h",
               marker_color=palette[i], text=['']*len(cats), textposition="inside")
        for i in range(len(dims))
    ])

    frames=[]
    for k in range(1, len(dims)+1):
        frame_bars = []
        for i in range(len(dims)):
            vals = eff_df.iloc[:, i].values if i < k else [0]*len(cats)
            frame_bars.append(go.Bar(
                y=cats, x=vals, name=dims[i], orientation="h",
                marker_color=palette[i], text=[str(v) for v in vals],
                textposition="inside"
            ))
        frames.append(go.Frame(data=frame_bars, name=f"e{k}"))
    fig.frames = frames

    xmax = float(eff_df.sum(axis=1).max()) * 1.08
    fig.update_layout(
        barmode="stack",
        height=500,
        margin=dict(l=170, r=40, t=60, b=80),
        xaxis=dict(title="Nombre de répondants", dtick=50, range=[0, xmax]),
        yaxis=dict(autorange="reversed"),
        legend=dict(orientation="h", y=-0.24),
    )
    themeify(fig)
    add_title_and_play(fig, "Nombre de répondants par dimension et par catégorie d’acteurs", btn_x=-0.02, btn_y=1.22)
    return fig

# ========================== Camembert animé ==========================
def pie_poids_relatif_anim(categories, values):
    palette = get_palette(len(categories))
    fig = go.Figure(data=[go.Pie(
        labels=categories, values=[0]*len(values),
        textinfo="label+percent", textposition="outside",
        marker=dict(colors=palette, line=dict(color="#fff", width=1)),
        sort=False
    )])

    frames=[]; cumul=[0]*len(values)
    for i in range(len(values)):
        cumul[i] = values[i]
        frames.append(go.Frame(data=[go.Pie(values=cumul)], name=f"p{i}"))
    fig.frames = frames

    fig.update_layout(
        height=500,
        margin=dict(l=30, r=30, t=60, b=40),
        showlegend=True,
        legend=dict(orientation="v", x=0.02, y=0.98, font=dict(size=12)),
    )
    themeify(fig)
    add_title_and_play(fig, "Poids relatif des acteurs dans le processus de transition (en %)", btn_x=0.0, btn_y=1.22)
    return fig

# ========================== PAGE ==========================
def show_page_graphiques():
    # Carte/ruban de section
    st.markdown("<div class='card' style='padding:10px 14px;margin:0 0 10px 0;'>"
                "<div style='display:flex;align-items:center;gap:10px;'>"
                "<span style='width:8px;height:24px;border-radius:99px;background:#027368;display:inline-block;'></span>"
                "<h3 style='margin:0;font-size:1.05rem;color:#0d2a27'>Visualisations interactives</h3>"
                "</div></div>", unsafe_allow_html=True)

    # Données pour les graphes
    radar_df = get_dimension_scores_per_categorie(dimensions, categories)
    # Exemple éventuel de filtrage
    to_drop = "Petits exploitants agricoles familiaux"
    if to_drop in radar_df.index:
        radar_df = radar_df.drop(to_drop)

    # Grille simple : 1 colonne (meilleure lisibilité). Vous pouvez passer à 2 si besoin.
    # RADAR
    st.markdown("<div class='card' style='margin-top:12px;'>", unsafe_allow_html=True)
    st.plotly_chart(radar_plot(radar_df), use_container_width=True, config=plot_config())
    st.markdown("</div>", unsafe_allow_html=True)

    # BAR
    st.markdown("<div class='card' style='margin-top:16px;'>", unsafe_allow_html=True)
    st.plotly_chart(bar_chart_anim(radar_df, cat_idx=0), use_container_width=True, config=plot_config())
    st.markdown("</div>", unsafe_allow_html=True)

    # EFFECTIFS
    st.markdown("<div class='card' style='margin-top:16px;'>", unsafe_allow_html=True)
    eff_df = get_effectifs_df(effectifs, dimensions, categories)
    st.plotly_chart(bar_effectifs_stacked_anim(eff_df), use_container_width=True, config=plot_config())
    st.markdown("</div>", unsafe_allow_html=True)

    # PIE
    st.markdown("<div class='card' style='margin-top:16px;'>", unsafe_allow_html=True)
    st.plotly_chart(pie_poids_relatif_anim(categories, poids_relatif), use_container_width=True, config=plot_config())
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__" or "streamlit" in __name__:
    show_page_graphiques()
