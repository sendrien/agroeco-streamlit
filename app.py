import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Titre de l'application
st.title("Analyse AGROECO")

# Upload du fichier Excel
uploaded_file = st.file_uploader("Chargez votre fichier AGROECO", type=["xlsx"])

if uploaded_file:
    # Lecture des feuilles utiles
    try:
        summary_df = pd.read_excel(uploaded_file, sheet_name="Résumé des résultats", engine="openpyxl")
    except:
        st.error("Impossible de trouver la feuille 'Résumé des résultats'.")
        st.stop()

    try:
        graphs_df = pd.read_excel(uploaded_file, sheet_name="Graphiques finaux", engine="openpyxl")
    except:
        st.warning("Feuille 'Graphiques finaux' introuvable, affichage des graphiques de base.")
        graphs_df = None

    st.success("Fichier chargé avec succès !")

    # Affichage du tableau de résumé
    st.subheader("Résumé des scores par dimension")
    st.dataframe(summary_df)

    # Affichage des graphiques finaux si disponibles
    if graphs_df is not None:
        st.subheader("Graphiques finaux")
        # Affiche la table brute de la feuille Graphiques finaux
        st.dataframe(graphs_df)

        # Supposons que la première partie contient Dimension et Score moyen
        if "Dimension" in graphs_df.columns and "Score moyen" in graphs_df.columns:
            fig1, ax1 = plt.subplots()
            ax1.bar(graphs_df["Dimension"], graphs_df["Score moyen"])
            ax1.set_xlabel("Dimension")
            ax1.set_ylabel("Score moyen")
            ax1.set_xticklabels(graphs_df["Dimension"], rotation=45, ha="right")
            st.pyplot(fig1)

        # Radar chart
        numeric = graphs_df.select_dtypes(include=["number"])
        if not numeric.empty and "Dimension" in graphs_df.columns:
            values = numeric.iloc[0].values
            labels = graphs_df["Dimension"].tolist()
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
            values = np.concatenate((values, [values[0]]))
            angles += angles[:1]

            fig2 = plt.figure()
            ax2 = fig2.add_subplot(111, polar=True)
            ax2.plot(angles, values, 'o-', linewidth=2)
            ax2.fill(angles, values, alpha=0.25)
            ax2.set_thetagrids(np.degrees(angles[:-1]), labels)
            ax2.set_title("Radar des dimensions")
            ax2.grid(True)
            st.pyplot(fig2)
    else:
        # Graphiques de base à partir du résumé
        st.subheader("Graphique des scores moyens (base)")
        if "Dimension" in summary_df.columns and "Score moyen" in summary_df.columns:
            fig, ax = plt.subplots()
            ax.bar(summary_df["Dimension"], summary_df["Score moyen"])
            ax.set_xlabel("Dimension")
            ax.set_ylabel("Score moyen")
            ax.set_xticklabels(summary_df["Dimension"], rotation=45, ha="right")
            st.pyplot(fig)
        else:
            st.info("Le fichier ne contient pas les colonnes attendues pour les graphiques.")

    # Option : afficher la base brute
    if st.checkbox("Afficher la base brute (Tous les résultats)"):
        try:
            raw = pd.read_excel(uploaded_file, sheet_name="Tous les résultats", engine="openpyxl")
            st.subheader("Données brutes")
            st.dataframe(raw.head(100))
        except:
            st.error("Feuille 'Tous les résultats' introuvable.")

    # Téléchargement du rapport nettoyé
    if st.button("Télécharger le rapport CSV nettoyé"):
        cleaned = summary_df.copy()
        cleaned.to_csv("rapport_agroeco.csv", index=False)
        st.success("Le fichier 'rapport_agroeco.csv' a été généré.")
