import streamlit as st
import pandas as pd

st.set_page_config(page_title="Synthèse AGROECO", layout="wide")

st.title("Synthèse des indicateurs – Outil AGROECO")

uploaded_file = st.file_uploader(
    "Chargez votre fichier Excel (structure AGROECO attendue)", 
    type=["xlsx"]
)

def extract_blocks(df):
    blocks = []
    n = len(df)
    i = 0
    while i < n:
        # Recherche d'une ligne de type 'Indicateur X'
        if pd.notna(df.iloc[i, 1]) and "Indicateur" in str(df.iloc[i, 1]):
            indicateur = str(df.iloc[i, 1])
            dimension = str(df.iloc[i-1, 0]) if i >= 1 else ""
            entete = df.iloc[i+1, 1:4].tolist()
            start = i + 2
            # Recherche des 7 lignes de catégories, s'arrête à la prochaine ligne "Indicateur" ou à la fin
            cat_rows = []
            j = start
            while j < n and pd.isna(df.iloc[j, 1]) and not (pd.notna(df.iloc[j, 3]) and "Indicateur" in str(df.iloc[j, 3])):
                if pd.notna(df.iloc[j, 2]):  # Nom catégorie présent
                    cat = [
                        df.iloc[j, 1],  # N°
                        df.iloc[j, 2],  # Catégorie
                        df.iloc[j, 3]   # Score
                    ]
                    cat_rows.append(cat)
                j += 1
                if len(cat_rows) == 7:
                    break
            # Recherche score moyen global par dimension
            score_global = df.iloc[i, 4] if i < n and df.shape[1] >= 5 else None
            blocks.append({
                "dimension": dimension,
                "indicateur": indicateur,
                "entete": entete,
                "categories": cat_rows,
                "score_global": score_global
            })
            i = j
        else:
            i += 1
    return blocks

if uploaded_file:
    # Lecture du fichier (feuille "Tous les résultats")
    df = pd.read_excel(uploaded_file, sheet_name="Tous les résultats", header=None)
    blocks = extract_blocks(df)
    
    for block in blocks:
        st.markdown(f"### {block['dimension']} - {block['indicateur']}")
        data = pd.DataFrame(
            block["categories"], 
            columns=["N°", "Catégorie d'acteurs", "Score moyen"]
        )
        st.table(data)
        if block["score_global"] is not None and pd.notna(block["score_global"]):
            st.markdown(f"**Score moyen global pour la dimension :** {block['score_global']}")
        st.markdown("---")

else:
    st.info("Veuillez charger un fichier pour afficher les résultats.")

