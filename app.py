import streamlit as st
import pandas as pd

# 1) Chargement des données
df = pd.read_excel("AGROECO 07072025.xlsx", sheet_name="Tous les résultats")

# 2) Préparation de la table « Indicateurs par catégorie »
df_ind = df.pivot_table(
    index=["Dimension", "Indicateur"],
    columns="Catégorie d’acteurs",
    values="Score moyen non pondéré"
).reset_index()

# 3) Préparation de la table « Résumé par dimension »
df_dim = df.drop_duplicates(["Dimension", "Catégorie d’acteurs"]) \
    .pivot_table(
        index="Dimension",
        columns="Catégorie d’acteurs",
        values="Score moyen global par dimension"
    )

# ==== Streamlit UI ====
st.title("Tableau de bord AGROECO")

# Onglet de navigation
view = st.sidebar.radio("Vue", ["Détails par indicateur", "Synthèse par dimension"])

if view == "Détails par indicateur":
    dim_sel = st.sidebar.selectbox("Choisir une dimension", df_ind["Dimension"].unique())
    df_display = df_ind[df_ind["Dimension"] == dim_sel].drop(columns="Dimension")
    st.header(f"Indicateurs – Dimension : {dim_sel}")
    st.dataframe(df_display)

else:  # Synthèse par dimension
    cat_sel = st.sidebar.multiselect("Choisir des catégories", df_dim.columns.tolist(), default=df_dim.columns.tolist())
    st.header("Scores moyens par dimension")
    st.dataframe(df_dim[cat_sel])
