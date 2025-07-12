import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titre de l'application
st.title("Analyse AGROECO")

# Upload du fichier Excel
uploaded_file = st.file_uploader("Chargez votre fichier AGROECO", type=["xlsx"])

if uploaded_file:
    # Lecture de la feuille de synthèse
    try:
        df = pd.read_excel(uploaded_file, sheet_name="Résumé des résultats", engine="openpyxl")
    except:
        df = pd.read_excel(uploaded_file, sheet_name=0, engine="openpyxl")

    st.success("Fichier chargé avec succès !")

    # Affichage du tableau de résumé
    st.subheader("Résumé des scores par dimension")
    st.dataframe(df)

    # Graphiques simples : barres des moyennes
    st.subheader("Graphique des scores moyens")
    # Supposons que les colonnes sont Nom de la dimension et Score
    if "Dimension" in df.columns and "Score moyen" in df.columns:
        fig, ax = plt.subplots()
        ax.bar(df["Dimension"], df["Score moyen"])
        ax.set_xlabel("Dimension")
        ax.set_ylabel("Score moyen")
        ax.set_xticklabels(df["Dimension"], rotation=45, ha="right")
        st.pyplot(fig)
    else:
        st.info("Le fichier ne contient pas les colonnes attendues (Dimension / Score moyen).")

    # Option : afficher la feuille brute
    if st.checkbox("Afficher la base brute (Tous les résultats)"):
        raw = pd.read_excel(uploaded_file, sheet_name="Tous les résultats", engine="openpyxl")
        st.subheader("Données brutes")
        st.dataframe(raw.head(100))

    # Téléchargement du rapport nettoyé
    if st.button("Télécharger le rapport CSV nettoyé"):
        cleaned = df.copy()
        cleaned.to_csv("rapport_agroeco.csv", index=False)
        st.success("Le fichier rapport_agroeco.csv a été généré dans votre environnement Streamlit.")
