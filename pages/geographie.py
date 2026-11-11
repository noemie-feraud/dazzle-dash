from dash import html, dcc, register_page, callback, Input, Output
from pathlib import Path
import pandas as pd
import plotly.express as px

# ENREGISTREMENT DE LA PAGE
register_page(
    __name__,
    path="/geographie",
    name="Géographie"
)

# PRÉPARATION DES DONNÉES GÉOGRAPHIQUES
# Chemin vers notre fichier nettoyé
DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "FAO_clean.csv"
)

# Chargement des données FAO
df = pd.read_csv(DATA_PATH)

# Reprendre les exclusions utilisées
# lors de notre analyse exploratoire
categories_agregees = [
    "Cereals - Excluding Beer",
    "Vegetables",
    "Fruits - Excluding Wine",
    "Starchy Roots",
    "Milk - Excluding Butter"
]

df_geo = df[
    ~df["Item"].isin(categories_agregees)
].copy()

# Quantités par pays et par utilisation
df_geo_totals = (
    df_geo.groupby(
        ["Area", "Element"], as_index=False
    )["Value"]
    .sum()
)


# CLASSEMENT TOP 10 DES TERRITOIRES
# Sélectionner les données Food
df_pays = df_geo_totals[
    df_geo_totals["Element"] == "Food"
].copy()

# Identifier les 10 territoires avec les volumes
# enregistrés les plus importants
top_10_pays = (
    df_pays.nlargest(10, "Value")
    .sort_values("Value")
)

# Créer un graphique horizontal
fig_pays = px.bar(
    top_10_pays,
    x="Value",
    y="Area",
    orientation="h",
    color_discrete_sequence=["#238C88"],
    labels={
        "Value": "Quantité cumulée (milliers de tonnes)",
        "Area": "Territoire"
    }
)

fig_pays.update_layout(
    template="plotly_white",
    font_family="IBM Plex Sans",
    showlegend=False,
    height=520,
    margin=dict(l=30, r=30, t=20, b=50)
)

# CARTE MONDIALE ALIMENTATION HUMAINE
# Conserver uniquement les quantités Food
df_map = df_geo_totals[
    df_geo_totals["Element"] == "Food"
].copy()

# Créer une carte à bulles
fig_geo = px.scatter_geo(
    df_map,
    locations="Area",
    locationmode="country names",
    size="Value",
    hover_name="Area",
    color_discrete_sequence=["#238C88"],
    size_max=45,
    projection="natural earth",
    labels={
        "Value": "Quantité (milliers de tonnes)"
    }
)

# Personnaliser l'apparence de la carte
fig_geo.update_geos(
    showland=True,
    landcolor="#F2F2F2",
    showocean=True,
    oceancolor="#EAF3F5",
    showcountries=True,
    countrycolor="#FFFFFF",
    showcoastlines=False
)

fig_geo.update_layout(
    template="plotly_white",
    font_family="IBM Plex Sans",
    margin=dict(l=10, r=10, t=10, b=10),
    height=650,
    geo=dict(
        bgcolor="rgba(0,0,0,0)"
    )
)

# STRUCTURE DE LA PAGE GÉOGRAPHIE
layout = html.Main(
    className="analysis-page",
    children=[
        html.Section(
            className="analysis-header",
            children=[
                html.P(
                    "03 / EXPLORATION GÉOGRAPHIQUE",
                    className="section-label"
                ),

                html.H1(
                    "Comment les usages alimentaires "
                    "varient-ils selon les pays ?",
                    className="analysis-title"
                ),

                html.P(
                    "Explorez la répartition géographique "
                    "des quantités destinées à l'alimentation "
                    "humaine et animale entre 1961 et 2013.",
                    className="analysis-description"
                )
            ]
        ),

        # SECTION 2 — FILTRES GÉOGRAPHIQUES
        html.Section(
            className="analysis-filters",
            children=[
                # Sélection du type d'utilisation
                html.Div(
                    className="filter-group",
                    children=[
                        html.Label(
                            "Utilisation",
                            htmlFor="geo-usage",
                            className="filter-label"
                        ),

                        dcc.Dropdown(
                            id="geo-usage",
                            options=[
                                {"label": "Food", "value": "Food"},
                                {"label": "Feed", "value": "Feed"}
                            ],
                            value="Food",
                            clearable=False
                        )
                    ]
                ),

                # Sélection de la période
                html.Div(
                    className="filter-group",
                    children=[
                        html.Label(
                            "Période",
                            htmlFor="geo-years",
                            className="filter-label"
                        ),

                        dcc.RangeSlider(
                            id="geo-years",
                            min=1961,
                            max=2013,
                            step=1,
                            value=[1961, 2013],
                            marks={
                                1961: "1961",
                                1980: "1980",
                                2000: "2000",
                                2013: "2013"
                            },
                            allowCross=False
                        )
                    ]
                )
            ]
        ),

        # SECTION 3 — CARTE MONDIALE
        html.Section(
            className="chart-section",
            children=[
                html.H2(
                    "Répartition mondiale des quantités alimentaires",
                    className="chart-title"
                ),

                html.P(
                    "La taille des bulles représente les quantités "
                    "enregistrées pour chaque territoire.",
                    className="chart-description"
                ),

                dcc.Graph(
                    id="geo-map",
                    figure=fig_geo,
                    config={
                        "displaylogo": False,
                        "responsive": True
                    },
                    style={"height": "650px"}
                )
            ]
        ),

        # SECTION 4 — CLASSEMENT DES PAYS
        html.Section(
            className="chart-section",
            children=[
                html.H2(
                    "Les territoires les plus représentés",
                    className="chart-title"
                ),

                html.P(
                    "Classement selon les quantités cumulées "
                    "enregistrées dans le jeu de données FAO.",
                    className="chart-description"
                ),

                dcc.Graph(
                    id="geo-ranking-chart",
                    figure=fig_pays,
                    config={
                        "displaylogo": False,
                        "responsive": True
                    },
                    style={"height": "520px"}
                )
            ]
        ),

        # SECTION 5 — À RETENIR
        html.Section(
            className="insight-section",
            children=[
                html.P(
                    "À RETENIR",
                    className="section-label"
                ),

                html.H2(
                    "Des volumes alimentaires très différents "
                    "selon les territoires.",
                    className="insight-title"
                ),

                html.P(
                    "La carte mondiale et le classement mettent "
                    "en évidence des différences importantes "
                    "dans les quantités enregistrées selon "
                    "les territoires. Ces résultats varient "
                    "également selon la période et l'utilisation "
                    "alimentaire sélectionnées.",
                    className="insight-description"
                ),

                html.P(
                    "Les quantités présentées ne sont pas "
                    "rapportées à la population. Leur interprétation "
                    "doit aussi tenir compte des données manquantes, "
                    "de la couverture géographique et des éventuels "
                    "chevauchements entre catégories de produits.",
                    className="insight-note"
                )
            ]
        )
    ]
)

# CALLBACK — CARTE ET CLASSEMENT GÉOGRAPHIQUE
@callback(
    Output("geo-map", "figure"),
    Output("geo-ranking-chart", "figure"),
    Input("geo-usage", "value"),
    Input("geo-years", "value")
)
def update_geo_map(usage, years):

    # 1. Filtrer les données
    df_filtered = df_geo[
        (df_geo["Year"] >= years[0]) &
        (df_geo["Year"] <= years[1]) &
        (df_geo["Element"] == usage)
    ]

    # 2. Calculer les quantités par territoire
    df_map = (
        df_filtered.groupby("Area", as_index=False)["Value"]
        .sum()
    )

    # Couleur selon l'utilisation sélectionnée
    color = "#238C88" if usage == "Food" else "#E6A24A"

    # GRAPHIQUE 1 — CARTE MONDIALE
    fig_map = px.scatter_geo(
        df_map,
        locations="Area",
        locationmode="country names",
        size="Value",
        hover_name="Area",
        color_discrete_sequence=[color],
        size_max=45,
        projection="natural earth",
        labels={
            "Value": "Quantité (milliers de tonnes)"
        }
    )

    fig_map.update_geos(
        showland=True,
        landcolor="#F2F2F2",
        showocean=True,
        oceancolor="#EAF3F5",
        showcountries=True,
        countrycolor="#FFFFFF",
        showcoastlines=False
    )

    fig_map.update_layout(
        template="plotly_white",
        font_family="IBM Plex Sans",
        margin=dict(l=10, r=10, t=10, b=10),
        height=650,
        geo=dict(bgcolor="rgba(0,0,0,0)")
    )

    # GRAPHIQUE 2 — TOP 10 DES TERRITOIRES
    top_10_pays = (
        df_map.nlargest(10, "Value")
        .sort_values("Value")
    )

    fig_ranking = px.bar(
        top_10_pays,
        x="Value",
        y="Area",
        orientation="h",
        color_discrete_sequence=[color],
        labels={
            "Value": "Quantité cumulée (milliers de tonnes)",
            "Area": "Territoire"
        }
    )

    fig_ranking.update_layout(
        template="plotly_white",
        font_family="IBM Plex Sans",
        showlegend=False,
        height=520,
        margin=dict(l=30, r=30, t=20, b=50)
    )

    return fig_map, fig_ranking