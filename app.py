#!/usr/bin/env python3
"""
Streamlit app pour charger le fichier AGROECO et afficher automatiquement
les visualisations synthétiques (barres, courbes, heatmap) des indicateurs
et indices de collaboration.
"""
import io
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- Fonctions de tracés ---
def plot_bar_chart(df, x_col, y_col, title):
    fig, ax = plt.subplots()
    ax.bar(df[x_col], df[y_col])
    ax.set_title(title)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig


def plot_line_chart(df, x_col, y_cols, title):
    fig, ax = plt.subplots()
    for y in y_cols:
        ax.plot(df[x_col], df[y], marker='o', label=y)
    ax.set_title(title)
    ax.set_xlabel(x_col)
    ax.legend()
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig


def plot_heatmap(df, title):
    fig, ax = plt.subplots()
    cax = ax.imshow(df.values, aspect='auto', cmap='viridis')
    ax.set_xticks(range(len(df.columns)))
    ax.set_xticklabels(df.columns, rotation=90)
    ax.set_yticks(range(len(df.index)))
    ax.set_yticklabels(df.index)
    ax.set_title(title)
    fig.colorbar(cax)
    plt.tight_layout()
    return fig

# --- Interface Streamlit ---
st.set_page_config(page_title="Visualisation AGROECO", layout="wide")
st.title("Visualisation Synthétique des Indicateurs AGROECO")

uploaded_file = st.file_uploader("Téléversez le fichier Excel AGROECO", type=["xlsx"])
if uploaded_file:
    try:
        # Lecture du fichier Excel
        in_memory = io.BytesIO(uploaded_file.read())
        xls = pd.ExcelFile(in_memory)

        # Onglets pour chaque type de graphique
        tabs = st.tabs([
            "Barres - Indicateurs",
            "Heatmap - Collaboration",
            "Courbes - Indices collaboration"
        ])

        # 1) Bar charts pour chaque dimension d'indicateurs
        with tabs[0]:
            st.header("Indicateurs par Dimension")
            indicator_sheets = {
                '1. Indicateurs environnementaux': 'Environnementnels',
                '2. Indicateurs économiques': 'Économiques',
                '3. Indicateurs politico-sociaux': 'Politico-sociaux',
                '4. Indicateurs territoriaux': 'Territoriaux',
                '5. Indicateurs temporels': 'Temporels'
            }
            for sheet_name, label in indicator_sheets.items():
                if sheet_name in xls.sheet_names:
                    df = xls.parse(sheet_name)
                    if 'Indicateur' in df.columns and 'Score moyen' in df.columns:
                        df_clean = df[['Indicateur', 'Score moyen']].dropna()
                        fig = plot_bar_chart(df_clean, 'Indicateur', 'Score moyen', f'Indicateurs {label}')
                        st.pyplot(fig)

        # 2) Heatmap de la matrice de collaboration
        with tabs[1]:
            st.header("Matrice des Indices de Collaboration")
            if 'Résumé des résultats' in xls.sheet_names:
                df_summary = xls.parse('Résumé des résultats', index_col=0)
                n = min(df_summary.shape)
                collab_matrix = df_summary.iloc[:n, :n]
                fig = plot_heatmap(collab_matrix, 'Collaboration entre Acteurs')
                st.pyplot(fig)

        # 3) Line charts pour les indices de collaboration détaillés
        with tabs[2]:
            st.header("Indices de Collaboration Détaillés")
            if '6. Indices de collaboration' in xls.sheet_names:
                df_coll = xls.parse('6. Indices de collaboration')
                if 'Acteur source' in df_coll.columns and 'Score moyen' in df_coll.columns:
                    df_pivot = df_coll.pivot(index='Acteur source', columns='Acteur cible', values='Score moyen')
                    df_plot = df_pivot.reset_index()
                    fig = plot_line_chart(df_plot, 'Acteur source', list(df_pivot.columns),
                                          'Indices de Collaboration par Acteur')
                    st.pyplot(fig)

    except Exception as e:
        st.error(f"Erreur lors du traitement du fichier: {e}")
else:
    st.info("Veuillez téléverser un fichier Excel pour commencer.")
