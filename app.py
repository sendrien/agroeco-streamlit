import streamlit as st
import pandas as pd

# ─── Configuration de la page ───────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard AGROECO (Static)",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Styles CSS personnalisés ───────────────────────────────────────────────
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
      /* Sidebar background */
      .css-1d391kg .css-1lcbmhc {
        background-color: #F0FFF0;
      }
      /* Police des tableaux */
      .stDataFrame div {
        font-family: 'Arial', sans-serif;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─── Titre et description ───────────────────────────────────────────────────
st.title("🌱 Dashboard AGROECO (Données statiques)")
st.markdown("**Visualisation des scores par indicateur et par dimension (exemple statique)**")

# ─── Données statiques d'exemple ─────────────────────────────────────────────
data = {
    "Dimension": [
        "Environnement", "Environnement",
        "Économique", "Économique",
        "Politico-social"
    ],
    "Indicateur": [
        "Qualité de l’eau", "Biodiversité",
        "Viabilité financière", "Chiffre d’affaires",
        "Participation citoyenne"
    ],
    "Producteurs": [5.2, 4.7, 4.8, 5.0, 4.5],
    "Consommateurs": [4.8, 4.3, 4.2, 4.5, 4.0],
    "ONG":           [5.5, 4.9, 4.9, 4.8, 4.6],
    "OSC":           [5.0, 4.2, 4.4, 4.6, 4.1],
    "Autorités":     [4.6, 4.1, 4.1, 4.2, 3.9],
    "Recherche":     [5.1, 4.8, 4.7, 4.9, 4.4],
    "Qualité":       [4.9, 4.0, 4.0, 4.3, 3.8],
}

df_ind = pd.DataFrame(data)

# Calcul de la synthèse par dimension (moyenne non pondérée)
df_dim = (
    df_ind
    .groupby("Dimension", as_index=True)
    .mean()
    .round(2)
)

# ─── Sidebar : choix de la vue ────────────────────────────────────────────────
view = st.sidebar.radio(
    "Sélectionnez la vue",
    ("Détails par indicateur", "Synthèse par dimension")
)

if view == "Détails par indicateur":
    st.header("📊 Détails par indicateur")
    # Filtre par dimension
    dim = st.sidebar.selectbox("Choisir une dimension", df_ind["Dimension"].unique())
    subset = df_ind[df_ind["Dimension"] == dim].drop(columns="Dimension")
    # Affichage colorisé
    st.dataframe(
        subset.style
              .background_gradient(axis=1, cmap="RdYlGn")
              .format("{:.2f}"),
        use_container_width=True,
    )

else:
    st.header("📈 Synthèse par dimension")
    # Sélection des catégories à afficher
    cats = st.sidebar.multiselect(
        "Choisir des catégories",
        df_dim.columns.tolist(),
        default=df_dim.columns.tolist()
    )
    sub = df_dim[cats]
    st.dataframe(
        sub.style
           .background_gradient(axis=1, cmap="RdYlGn")
           .format("{:.2f}"),
        use_container_width=True,
    )

# ─── Pied de page ───────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("*Exemple statique — aucune donnée externe chargée*")
