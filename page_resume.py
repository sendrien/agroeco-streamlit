def show_page_resume():
    st.markdown("<h2 style='color:#027368;'>Note globale des dimensions par catégories d'acteurs</h2>", unsafe_allow_html=True)

    radar_df = get_dimension_scores_per_categorie(dimensions, categories)

    # Affichage justifié
    st.markdown("""
        <style>
        .radar-justif th, .radar-justif td {
            text-align: justify !important;
            text-justify: inter-word !important;
            font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
            font-size: 1.05em;
            padding: 7px 13px !important;
        }
        .radar-justif th { background: #027368 !important; color: #fff; font-size: 0.85em;}
        .radar-justif { width: 100% !important; border-radius: 7px !important; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(
        radar_df.reset_index().to_html(index=False, classes="radar-justif", border=0), 
        unsafe_allow_html=True
    )

    st.info("Ce tableau est structuré pour permettre la génération du radar plot : chaque ligne = une catégorie d’acteurs, chaque colonne = une dimension (moyenne de ses indicateurs pour la catégorie).")
