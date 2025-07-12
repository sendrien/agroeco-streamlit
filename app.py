import streamlit as st
import pandas as pd
import numpy as np

# Titre et description
st.title("Ma première application Streamlit")
st.markdown("""Cette application montre comment :
- Charger des données
- Créer des graphiques interactifs
- Déployer facilement sur Streamlit Cloud""")

# Section : chargement de données
@st.cache_data
def load_data(n_rows=100):
    # Génère un DataFrame aléatoire
    df = pd.DataFrame({
        'x': np.random.randn(n_rows),
        'y': np.random.randn(n_rows),
        'groupe': np.random.choice(['A', 'B', 'C'], n_rows)
    })
    return df

data = load_data(200)
st.write("Aperçu des données", data.head())

# Section : filtre par groupe
groupe_sel = st.multiselect("Choisissez un groupe :", options=data['groupe'].unique(), default=['A','B','C'])
filtered = data[data['groupe'].isin(groupe_sel)]
st.write(f"Données filtrées ({len(filtered)} lignes)", filtered)

# Section : graphique
st.subheader("Nuage de points interactif")
st.scatter_chart(filtered, x='x', y='y')

# Section : slider
st.sidebar.header("Paramètres")
n = st.sidebar.slider("Nombre de points à afficher", min_value=50, max_value=500, value=200, step=50)
if n != len(data):
    data2 = load_data(n)
    st.write(f"Derniers {n} points :", data2)
    st.line_chart(data2[['x','y']])
