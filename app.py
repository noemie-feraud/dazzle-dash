
from dash import Dash, html, page_container
from layout import create_navbar, create_footer

# Initialisation de l'application multipage
app = Dash(__name__, use_pages=True)

# Structure commune aux quatre pages
app.layout = html.Div([
    create_navbar(),
    page_container,
    create_footer()
])

server = app.server
