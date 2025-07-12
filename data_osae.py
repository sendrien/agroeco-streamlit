# data_osae.py

# Toutes les catégories d’acteurs
categories = [
    "Petits exploitants agricoles familiaux",
    "Consommateurs",
    "Membres des Organisations non gouvernementales",
    "Membres des Organisations de la société civile",
    "Autorités administratives régionales et nationales",
    "Membres des structures de formation et de recherche",
    "Membres des systèmes de garantie de la qualité",
]

# Toutes les dimensions et scores des indicateurs
dimensions = [
    {
        "nom": "Dimension environnementale",
        "indicateurs": [
            {"nom": "Indicateur 1", "scores": [1.44, 1.7, 2.7, 2.5, 2.0, 2.5, None]},
            {"nom": "Indicateur 2", "scores": [2.0, 1.6, 3.2, 3.5, 3.0, 3.0, 3.0]},
        ],
    },
    {
        "nom": "Dimension économique",
        "indicateurs": [
            {"nom": "Indicateur 3", "scores": [1.8, 2.1, 2.9, 3.0, 2.2, 2.8, 3.1]},
        ],
    },
    {
        "nom": "Dimension territoriale",
        "indicateurs": [
            {"nom": "Indicateur 4", "scores": [2.2, 1.9, 2.5, 3.0, 2.8, 2.3, 2.7]},
            {"nom": "Indicateur 5", "scores": [2.0, 2.4, 2.7, 2.8, 2.5, 2.1, 2.6]},
        ],
    },
    {
        "nom": "Dimension politique et sociale",
        "indicateurs": [
            {"nom": "Indicateur 6", "scores": [1.7, 1.9, 2.3, 2.7, 2.4, 2.0, 2.8]},
            {"nom": "Indicateur 7", "scores": [2.5, 2.6, 2.9, 3.0, 2.9, 2.7, 3.1]},
        ],
    },
    {
        "nom": "Dimension temporelle",
        "indicateurs": [
            {"nom": "Indicateur 8", "scores": [2.0, 2.2, 2.3, 2.6, 2.1, 2.5, 2.8]},
        ],
    },
]

score_colname = "Scores moyens Indicateurs non pondérés par les poids des acteurs"


# Effectifs de répondants par catégorie et par dimension
effectifs = [
    [195, 200, 199, 200, 199],    # Petits exploitants agricoles familiaux
    [200, 200, 200, 200, 200],    # Consommateurs
    [200, 200, 200, 200, 199],    # Membres des ONG
    [40, 39, 40, 39, 40],         # Membres société civile
    [20, 20, 20, 20, 20],         # Autorités administratives régionales et nationales
    [40, 39, 40, 40, 40],         # Membres formation/recherche
    [19, 20, 20, 20, 20],         # Membres garantie qualité
]
