import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Tous les résultats", layout="wide")
st.title("Tous les résultats")

# Données statiques d'exemple
# Chaque indicateur contient une liste de dicts représentant les catégories
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

# Affichage de chaque bloc indicateur
for indicateur, rows in data.items():
    st.markdown(f"### {indicateur}")
    df = pd.DataFrame(rows)
    # Renommage des colonnes pour correspondre à l'onglet Excel
    df = df.rename(columns={
        "N°": "N°",
        "Catégorie": "Catégories d’acteurs",
        "Score": "Score moyen global"
    })
    # Calcul de la moyenne (excluant les zéros)
    avg = df["Score moyen global"].loc[df["Score moyen global"] != 0].mean()
    
    # Mise en forme du tableau pour ressembler à Excel
    styled = df.style.hide_index().set_table_styles([
        {
            'selector': 'th',
            'props': [
                ('background-color', '#e0e0e0'),
                ('font-weight', 'bold'),
                ('text-align', 'center')
            ]
        },
        {
            'selector': 'td',
            'props': [
                ('padding', '6px'),
                ('text-align', 'center')
            ]
        }
    ])
    st.write(styled.to_html(), unsafe_allow_html=True)
    st.markdown(f"**Moyenne (excl. zéros) :** {avg:.2f}")
    st.markdown("---")
