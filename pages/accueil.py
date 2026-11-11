from dash import html, dcc, register_page

# Enregistrement de la page d'accueil
register_page(__name__, path="/", name="Accueil")

layout = html.Main([

    # SECTION 1 — HERO
    html.Section(
        className="hero",
        children=[
            html.Div(
                className="hero-content",
                children=[
                    html.P(
                        "EXPLORATION DES DONNÉES FAO",
                        className="hero-label"
                    ),

                    html.H1(
                        "Comprendre les usages alimentaires "
                        "dans le monde.",
                        className="hero-title"
                    ),

                    html.P(
                        "Découvrez comment les quantités destinées "
                        "à l'alimentation humaine et animale "
                        "évoluent à travers le monde, de 1961 à 2013.",
                        className="hero-description"
                    ),

                    dcc.Link(
                        "Explorer les données →",
                        href="/evolutions",
                        className="hero-button"
                    )
                ]
            )
        ]
    ),

    # SECTION 2 EXPLORATION
    html.Section(
        className="explore-section",
        children=[
            html.P(
                "DÉCOUVRIR L'APPLICATION",
                className="section-label"
            ),

            html.H2(
                "Comment explorer les données ?",
                className="section-title"
            ),

            html.P(
                "Quatre espaces pour comprendre les usages "
                "alimentaires à travers le monde.",
                className="section-description"
            ),

            html.Div(
                className="explore-grid",
                children=[

                    # Carte 1 Vue d'ensemble
                    html.Div(
                        className="explore-card",
                        children=[
                            html.Span(
                                "01",
                                className="card-number"
                            ),
                            html.H3("Vue d'ensemble"),
                            html.P(
                                "Découvrez le contexte de notre exploration."
                            )
                        ]
                    ),

                    # Carte 2 Évolutions
                    html.Div(
                        className="explore-card",
                        children=[
                            html.Span(
                                "02",
                                className="card-number"
                            ),
                            html.H3("Évolutions"),
                            html.P(
                                "Observez les changements entre 1961 et 2013."
                            )
                        ]
                    ),

                    # Carte 3 Produits
                    html.Div(
                        className="explore-card",
                        children=[
                            html.Span(
                                "03",
                                className="card-number"
                            ),
                            html.H3("Produits"),
                            html.P(
                                "Comparez les différents usages alimentaires."
                            )
                        ]
                    ),

                    # Carte 4 Géographie
                    html.Div(
                        className="explore-card",
                        children=[
                            html.Span(
                                "04",
                                className="card-number"
                            ),
                            html.H3("Géographie"),
                            html.P(
                                "Explorez les différences entre les pays."
                            )
                        ]
                    )
                ]
            )
        ]
    ),

    # SECTION 3 À PROPOS DES DONNÉES
    html.Section(
        className="about-section",
        children=[
            html.Div(
                className="about-content",
                children=[
                    html.P(
                        "COMPRENDRE LES DONNÉES",
                        className="section-label"
                    ),

                    html.H2(
                        "Des données pour comprendre "
                        "les usages alimentaires.",
                        className="section-title"
                    ),

                    html.P(
                        "Cette application s'appuie sur un jeu de "
                        "données de la FAO couvrant la période "
                        "de 1961 à 2013.",
                        className="about-description"
                    ),

                    html.P(
                        "Nous explorons deux types d'utilisation : "
                        "Food, pour l'alimentation humaine, et "
                        "Feed, pour l'alimentation animale.",
                        className="about-description"
                    ),

                    html.P(
                        "Les quantités sont exprimées en milliers "
                        "de tonnes. Certaines données historiques "
                        "sont manquantes et certaines catégories "
                        "de produits peuvent se chevaucher.",
                        className="about-note"
                    )
                ]
            )
        ]
    ),

    # SECTION 4 APPEL À L'ACTION
    html.Section(
        className="cta-section",
        children=[
            html.Div(
                className="cta-content",
                children=[
                    html.H2(
                        "Les données ont une histoire "
                        "à raconter.",
                        className="cta-title"
                    ),

                    html.P(
                        "Explorez les évolutions, les produits "
                        "et les différences géographiques "
                        "à travers nos visualisations interactives.",
                        className="cta-description"
                    ),

                    dcc.Link(
                        "Commencer l'exploration →",
                        href="/evolutions",
                        className="cta-button"
                    )
                ]
            )
        ]
    )
])