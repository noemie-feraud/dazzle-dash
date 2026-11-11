
from dash import html, dcc

def create_navbar():
    return html.Header(
        className="navbar",
        children=[
            dcc.Link(
                "Dazzle Dash",
                href="/",
                className="navbar-brand"
            ),

            html.Nav(
                className="navbar-links",
                children=[
                    dcc.Link("Accueil", href="/"),
                    dcc.Link("Évolutions", href="/evolutions"),
                    dcc.Link("Produits", href="/produits"),
                    dcc.Link("Géographie", href="/geographie")
                ]
            )
        ]
    )


def create_footer():
    return html.Footer(
        className="footer",
        children=[
            html.Span(
                "Dazzle Dash",
                className="footer-brand"
            ),

            html.P(
                "Projet Data Storytelling • Données FAO (1961–2013)",
                className="footer-description"
            )
        ]
    )
