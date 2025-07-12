import streamlit as st
import pandas as pd

# Titre de l'application
st.title("Synthèse : Tous les résultats")

# Données statiques d'exemple
# Chaque indicateur contient une liste de dictionnaires représentant les catégories
data = {
    "Indicateur 1": [
        {"N°": 1, "Catégorie": "Producteurs", "Score": 75},
        {"N°": 2, "Catégorie": "Consommateurs", "Score": 82},
        {"N°": 3, "Catégorie": "Membres ONG", "Score": 68},
        {"N°": 4, "Catégorie": "Membres OSC", "Score": 71},
        {"N°": 5, "Catégorie": "Autorités administratives", "Score": 79},
        {"N°": 6, "Catégorie": "Formation et recherches", "Score": 74},
        {"N°": 7, "Catégorie": "Acteurs garantie qualité", "Score": 77},
    ],
    "Indicateur 2": [
        {"N°": 1, "Catégorie": "Producteurs", "Score": 68},
        {"N°": 2, "Catégorie": "Consommateurs", "Score": 80},
        {"N°": 3, "Catégorie": "Membres ONG", "Score": 65},
        {"N°": 4, "Catégorie": "Membres OSC", "Score": 70},
        {"N°": 5, "Catégorie": "Autorités administratives", "Score": 76},
        {"N°": 6, "Catégorie": "Formation et recherches", "Score": 72},
        {"N°": 7, "Catégorie": "Acteurs garantie qualité", "Score": 75},
    ],
    # Ajoutez d'autres indicateurs ici
}

# Boucle d'affichage par indicateur
for indicateur, rows in data.items():
    st.subheader(indicateur)
    df = pd.DataFrame(rows)
    # Affichage du tableau
    st.table(df)

# Note : pour lancer cette application
# 1. Installez Streamlit : pip install streamlit
# 2. Exécutez : streamlit run app.py
