from dash import html, dcc, register_page, callback, Input, Output
from pathlib import Path
import pandas as pd
import plotly.express as px

# Enregistrement de la page
register_page(
    __name__,
    path="/produits",
    name="Produits"
)

# PRÉPARATION DES DONNÉES — PRODUITS
# Chemin vers le fichier FAO nettoyé
DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "FAO_clean.csv"
)

# Chargement des données
df = pd.read_csv(DATA_PATH)

# Grandes catégories exclues pour limiter
# les chevauchements avec les produits détaillés
categories_agregees = [
    "Cereals - Excluding Beer",
    "Vegetables",
    "Fruits - Excluding Wine",
    "Starchy Roots",
    "Milk - Excluding Butter"
]

# Conserver les autres produits
df_produits = df[
    ~df["Item"].isin(categories_agregees)
].copy()

# Calculer les quantités par produit et par usage
df_classement = (
    df_produits
    .groupby(["Item", "Element"], as_index=False)["Value"]
    .sum()
)

# PRÉPARATION — RÉPARTITION FOOD / FEED
# Total de chaque produit, tous usages confondus
totaux_produits = (
    df_classement.groupby("Item")["Value"]
    .sum()
)

# Sélectionner les 10 produits les plus représentés
top_10_items = (
    totaux_produits.nlargest(10).index
)

# Conserver les quantités Food et Feed de ces produits
df_repartition = df_classement[
    df_classement["Item"].isin(top_10_items)
].copy()

# Calculer la part de chaque usage
df_repartition["Total"] = (
    df_repartition.groupby("Item")["Value"]
    .transform("sum")
)

df_repartition["Percentage"] = (
    df_repartition["Value"]
    / df_repartition["Total"] * 100
)


# GRAPHIQUE — RÉPARTITION FOOD / FEED
fig_repartition = px.bar(
    df_repartition,
    x="Percentage",
    y="Item",
    color="Element",
    orientation="h",
    barmode="stack",
    category_orders={
        "Element": ["Food", "Feed"]
    },
    color_discrete_map={
        "Food": "#238C88",
        "Feed": "#E6A24A"
    },
    labels={
        "Percentage": "Part (%)",
        "Item": "Produit",
        "Element": "Utilisation"
    }
)

fig_repartition.update_layout(
    template="plotly_white",
    font_family="IBM Plex Sans",
    legend_title_text="",
    xaxis=dict(range=[0, 100], ticksuffix="%"),
    margin=dict(l=30, r=30, t=20, b=50),
    height=550
)

fig_repartition.update_traces(
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Part : %{x:.1f}%"
        "<extra></extra>"
    )
)

# GRAPHIQUE — TOP 10 DES PRODUITS
# Total par produit, tous usages confondus
top_produits = (
    df_classement.groupby("Item", as_index=False)["Value"]
    .sum()
    .nlargest(10, "Value")
    .sort_values("Value")
)

# Graphique en barres horizontales
fig_produits = px.bar(
    top_produits,
    x="Value",
    y="Item",
    orientation="h",
    color_discrete_sequence=["#238C88"],
    labels={
        "Value": "Quantité cumulée (milliers de tonnes)",
        "Item": "Produit"
    }
)

fig_produits.update_layout(
    template="plotly_white",
    font_family="IBM Plex Sans",
    margin=dict(l=30, r=30, t=20, b=50),
    showlegend=False,
    height=550
)

fig_produits.update_traces(
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Quantité : %{x:,.0f} milliers de tonnes"
        "<extra></extra>"
    )
)

# STRUCTURE DE LA PAGE PRODUITS
layout = html.Main(
    className="analysis-page",
    children=[
        html.Section(
            className="analysis-header",
            children=[
                html.P(
                    "02 / ANALYSE PAR PRODUIT",
                    className="section-label"
                ),

                html.H1(
                    "Quels produits sont destinés "
                    "aux humains ou aux animaux ?",
                    className="analysis-title"
                ),

                html.P(
                    "Découvrez les produits alimentaires "
                    "les plus représentés dans notre jeu "
                    "de données FAO et comparez leurs "
                    "différents usages.",
                    className="analysis-description"
                )
            ]
        ),

        # SECTION 2 — FILTRES DES PRODUITS
        html.Section(
            className="analysis-filters product-filters",
            children=[
                # Nombre de produits affichés
                html.Div(
                    className="filter-group",
                    children=[
                        html.Label(
                            "Nombre de produits",
                            htmlFor="product-top",
                            className="filter-label"
                        ),

                        dcc.Dropdown(
                            id="product-top",
                            options=[
                                {"label": "Top 5", "value": 5},
                                {"label": "Top 10", "value": 10},
                                {"label": "Top 20", "value": 20}
                            ],
                            value=10,
                            clearable=False
                        )
                    ]
                ),

                # Type d'utilisation
                html.Div(
                    className="filter-group",
                    children=[
                        html.Label(
                            "Utilisation",
                            htmlFor="product-usage",
                            className="filter-label"
                        ),

                        dcc.Dropdown(
                            id="product-usage",
                            options=[
                                {"label": "Food + Feed", "value": "all"},
                                {"label": "Food", "value": "Food"},
                                {"label": "Feed", "value": "Feed"}
                            ],
                            value="all",
                            clearable=False
                        )
                    ]
                ),

                # Période étudiée
                html.Div(
                    className="filter-group",
                    children=[
                        html.Label(
                            "Période",
                            htmlFor="product-years",
                            className="filter-label"
                        ),

                        dcc.RangeSlider(
                            id="product-years",
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

        # SECTION 3 — CLASSEMENT DES PRODUITS
        html.Section(
            className="chart-section",
            children=[
                html.H2(
                    "Les produits les plus représentés",
                    className="chart-title"
                ),

                html.P(
                    "Classement selon les quantités cumulées "
                    "enregistrées entre 1961 et 2013.",
                    className="chart-description"
                ),

                dcc.Graph(
                    id="products-ranking-chart",
                    figure=fig_produits,
                    config={"displaylogo": False},
                    style={"height": "550px"}
                )
            ]
        ),

        # SECTION 4 — RÉPARTITION PAR PRODUIT
        html.Section(
            className="chart-section",
            children=[
                html.H2(
                    "Répartition Food / Feed par produit",
                    className="chart-title"
                ),

                html.P(
                    "Part de chaque utilisation dans les quantités "
                    "enregistrées pour les principaux produits.",
                    className="chart-description"
                ),

                dcc.Graph(
                    id="products-share-chart",
                    figure=fig_repartition,
                    config={
                        "displaylogo": False,
                        "responsive": True
                    },
                    style={"height": "550px"}
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
                    "Des produits aux usages très différents.",
                    className="insight-title"
                ),

                html.P(
                    "Les quantités enregistrées varient fortement "
                    "d'un produit à l'autre. Certains produits "
                    "sont davantage associés à l'alimentation "
                    "humaine, tandis que d'autres occupent une "
                    "place importante dans l'alimentation animale.",
                    className="insight-description"
                ),

                html.P(
                    "Les classements dépendent de la période "
                    "et de l'utilisation sélectionnées. "
                    "Certaines catégories FAO peuvent également "
                    "se chevaucher, malgré les exclusions "
                    "effectuées pour cette analyse.",
                    className="insight-note"
                )
            ]
        )
    ]
)

# CALLBACK — GRAPHIQUES DES PRODUITS
@callback(
    Output("products-ranking-chart", "figure"),
    Output("products-share-chart", "figure"),
    Input("product-top", "value"),
    Input("product-usage", "value"),
    Input("product-years", "value")
)
def update_products_ranking(top_n, usage, years):

    # 1. Filtrer les données selon la période
    df_filtered = df_produits[
        (df_produits["Year"] >= years[0]) &
        (df_produits["Year"] <= years[1])
    ]

    # 2. Appliquer le filtre d'utilisation au classement
    df_ranking = df_filtered.copy()

    if usage != "all":
        df_ranking = df_ranking[
            df_ranking["Element"] == usage
        ]

    # 3. Recalculer les produits les plus représentés
    ranking = (
        df_ranking.groupby("Item", as_index=False)["Value"]
        .sum()
        .nlargest(top_n, "Value")
        .sort_values("Value")
    )

    # 4. Premier graphique : classement
    fig_ranking = px.bar(
        ranking,
        x="Value",
        y="Item",
        orientation="h",
        color_discrete_sequence=["#238C88"],
        labels={
            "Value": "Quantité cumulée (milliers de tonnes)",
            "Item": "Produit"
        }
    )

    fig_ranking.update_layout(
        template="plotly_white",
        font_family="IBM Plex Sans",
        showlegend=False,
        height=550,
        margin=dict(l=30, r=30, t=20, b=50)
    )

    # 5. Conserver les mêmes produits pour la répartition
    selected_items = ranking["Item"].tolist()

    df_share = df_filtered[
        df_filtered["Item"].isin(selected_items)
    ]

    share = (
        df_share.groupby(
            ["Item", "Element"], as_index=False
        )["Value"]
        .sum()
    )

    # Calculer les proportions Food / Feed
    share["Total"] = (
        share.groupby("Item")["Value"].transform("sum")
    )

    share = share[share["Total"] > 0].copy()

    share["Percentage"] = (
        share["Value"] / share["Total"] * 100
    )

    # 6. Deuxième graphique : répartition
    fig_share = px.bar(
        share,
        x="Percentage",
        y="Item",
        color="Element",
        orientation="h",
        barmode="stack",
        category_orders={
            "Element": ["Food", "Feed"],
            "Item": selected_items
        },
        color_discrete_map={
            "Food": "#238C88",
            "Feed": "#E6A24A"
        },
        labels={
            "Percentage": "Part (%)",
            "Item": "Produit",
            "Element": "Utilisation"
        }
    )

    fig_share.update_layout(
        template="plotly_white",
        font_family="IBM Plex Sans",
        legend_title_text="",
        xaxis=dict(range=[0, 100], ticksuffix="%"),
        height=550,
        margin=dict(l=30, r=30, t=20, b=50)
    )

    return fig_ranking, fig_share