import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="Dashboard AGROECO",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown(
    """
    <style>
    /* Titre principal */
    h1 {
        color: #2E8B57;
        font-size: 2.5rem;
    }
    /* Sous-titres */
    h2, h3 {
        color: #556B2F;
    }
    /* Sidebar */
    .css-1d391kg .css-1lcbmhc {
        background-color: #F0FFF0;
    }
    /* Table style */
    .stDataFrame div {
        font-family: 'Arial', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True
)

# Titre de l'application
st.title("🌱 Dashboard AGROECO")
st.markdown("**Visualisation interactive des scores par indicateur et par dimension**")

# Chargement des données
@st.cache_data
def load_data(path: str):
    df = pd.read_excel(path, sheet_name="Tous les résultats")
    # Renommage clair des colonnes
    df = df.rename(columns={
        "Score moyen non pondéré": "Score indicateur (non pondéré)",
        "Score moyen global par dimension": "Score dimension (non pondéré)"
    })
    return df

df = load_data("AGROECO 07072025.xlsx")

# Préparation des pivots
# Détails par indicateur
df_ind = df.pivot_table(
    index=["Dimension", "Indicateur"],
    columns="Catégorie d’acteurs",
    values="Score indicateur (non pondéré)"
).reset_index()

# Synthèse par dimension
df_dim = df.drop_duplicates(["Dimension", "Catégorie d’acteurs"]) \
    .pivot_table(
        index="Dimension",
        columns="Catégorie d’acteurs",
        values="Score dimension (non pondéré)"
    )

# Sélecteur de vue
view = st.sidebar.radio(
    "Sélectionnez la vue", 
    ["Détails par indicateur", "Synthèse par dimension"]
)

if view == "Détails par indicateur":
    st.header("📊 Détails par indicateur")
    # Filtre par dimension
    dim_sel = st.sidebar.selectbox(
        "Choisir une dimension", 
        df_ind["Dimension"].unique()
    )
    df_display = df_ind[df_ind["Dimension"] == dim_sel].drop(columns="Dimension")
    # Affichage avec coloration en dégradé
    styled = df_display.style.background_gradient(
        axis=1, 
        cmap="RdYlGn"
    ).set_precision(2)
    st.dataframe(styled, use_container_width=True)

else:
    st.header("📈 Synthèse par dimension")
    # Sélection des catégories
    cat_sel = st.sidebar.multiselect(
        "Choisir des catégories", 
        df_dim.columns.tolist(), 
        default=df_dim.columns.tolist()
    )
    # Affichage synthèse
    styled_dim = df_dim[cat_sel].style.background_gradient(
        axis=1, 
        cmap="RdYlGn"
    ).set_precision(2)
    st.dataframe(styled_dim, use_container_width=True)

# Pied de page
st.markdown("---")
st.markdown("*Développé par l'équipe AGROECO*  _Date de génération : 07/07/2025_")