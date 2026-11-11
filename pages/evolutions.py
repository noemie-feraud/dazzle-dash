from dash import html, dcc, register_page, callback, Input, Output
from pathlib import Path
import pandas as pd
import plotly.express as px


# ENREGISTREMENT DE LA PAGE
register_page(
    __name__,
    path="/evolutions",
    name="Évolutions"
)


# PRÉPARATION DES DONNÉES
# Chemin vers notre fichier FAO nettoyé
DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "FAO_clean.csv"
)

# Chargement des données
df = pd.read_csv(DATA_PATH)

# Quantités enregistrées par année et par utilisation
df_evolution = (
    df.groupby(["Year", "Element"], as_index=False)["Value"]
    .sum()
)

# CALCUL DES PROPORTIONS FOOD / FEED
df_proportions = df_evolution.copy()

# Total des quantités enregistrées pour chaque année
df_proportions["Total"] = (
    df_proportions.groupby("Year")["Value"]
    .transform("sum")
)

# Part de chaque usage en pourcentage
df_proportions["Percentage"] = (
    df_proportions["Value"] /
    df_proportions["Total"] * 100
)

# GRAPHIQUE  RÉPARTITION FOOD / FEED
fig_proportions = px.area(
    df_proportions,
    x="Year",
    y="Percentage",
    color="Element",
    category_orders={
        "Element": ["Food", "Feed"]
    },
    color_discrete_map={
        "Food": "#238C88",
        "Feed": "#E6A24A"
    },
    labels={
        "Year": "Année",
        "Percentage": "Part (%)",
        "Element": "Utilisation"
    }
)

fig_proportions.update_layout(
    template="plotly_white",
    font_family="IBM Plex Sans",
    hovermode="x unified",
    legend_title_text="",
    yaxis=dict(range=[0, 100], ticksuffix="%"),
    margin=dict(l=40, r=30, t=30, b=40)
)

# CRÉATION DU GRAPHIQUE PLOTLY
fig_evolution = px.line(
    df_evolution,
    x="Year",
    y="Value",
    color="Element",
    color_discrete_map={
        "Food": "#238C88",
        "Feed": "#E6A24A"
    },
    labels={
        "Year": "Année",
        "Value": "Quantité (milliers de tonnes)",
        "Element": "Utilisation"
    }
)

fig_evolution.update_layout(
    template="plotly_white",
    title=None,
    font_family="IBM Plex Sans",
    hovermode="x unified",
    legend_title_text="",
    margin=dict(l=40, r=30, t=30, b=40)
)

fig_evolution.update_traces(
    line_width=3
)

# STRUCTURE DE LA PAGE
layout = html.Main(
    className="analysis-page",
    children=[

        # SECTION 1 — EN-TÊTE
        html.Section(
            className="analysis-header",
            children=[
                html.P(
                    "01 / ANALYSE TEMPORELLE",
                    className="section-label"
                ),

                html.H1(
                    "Comment les usages alimentaires "
                    "ont-ils évolué ?",
                    className="analysis-title"
                ),

                html.P(
                    "Explorez les changements des quantités "
                    "destinées à l'alimentation humaine et "
                    "animale entre 1961 et 2013.",
                    className="analysis-description"
                )
            ]
        ),

        # SECTION 2 — FILTRES
        html.Section(
            className="analysis-filters",
            children=[

                # Filtre de période
                html.Div(
                    className="filter-group",
                    children=[
                        html.Label(
                            "Période",
                            htmlFor="year-range",
                            className="filter-label"
                        ),

                        dcc.RangeSlider(
                            id="year-range",
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
                ),

                # Filtre d'utilisation
                html.Div(
                    className="filter-group",
                    children=[
                        html.Label(
                            "Utilisation",
                            htmlFor="usage-filter",
                            className="filter-label"
                        ),

                        dcc.Dropdown(
                            id="usage-filter",
                            options=[
                                {
                                    "label": "Food + Feed",
                                    "value": "all"
                                },
                                {
                                    "label": "Food",
                                    "value": "Food"
                                },
                                {
                                    "label": "Feed",
                                    "value": "Feed"
                                }
                            ],
                            value="all",
                            clearable=False
                        )
                    ]
                )
            ]
        ),

        # SECTION 3 — GRAPHIQUE
        html.Section(
            className="chart-section",
            children=[
                html.H2(
                    "Évolution des quantités alimentaires",
                    className="chart-title"
                ),

                dcc.Graph(
                    id="evolution-chart",
                    figure=fig_evolution,
                    config={
                        "displaylogo": False,
                        "responsive": True
                    },
                    style={"height": "450px"}
                )
            ]
        ),

        # SECTION 4 RÉPARTITION EN POURCENTAGE
        html.Section(
            className="chart-section",
            children=[
                html.H2(
                    "Répartition Food / Feed au fil du temps",
                    className="chart-title"
                ),

                html.P(
                    "Évolution de la part de chaque utilisation "
                    "dans les quantités enregistrées chaque année.",
                    className="chart-description"
                ),

                dcc.Graph(
                    id="proportions-chart",
                    figure=fig_proportions,
                    config={"displaylogo": False},
                    style={"height": "450px"}
                )
            ]
        ),
        
        # SECTION 5  À RETENIR
        html.Section(
            className="insight-section",
            children=[
                html.P(
                    "À RETENIR",
                    className="section-label"
                ),

                html.H2(
                    "Des quantités en hausse, "
                    "mais une répartition qui évolue.",
                    className="insight-title"
                ),

                html.P(
                    "Entre 1961 et 2013, les quantités enregistrées "
                    "pour l'alimentation humaine et animale "
                    "augmentent globalement. Cependant, "
                    "la part relative de Food progresse, "
                    "tandis que celle de Feed recule.",
                    className="insight-description"
                ),

                html.P(
                    "Ces tendances doivent être interprétées "
                    "avec prudence : la couverture historique "
                    "des pays varie et certaines catégories "
                    "de produits peuvent se chevaucher.",
                    className="insight-note"
                )
            ]
        )
    ]
)


# CALLBACK FILTRES DU GRAPHIQUE
@callback(
    Output("evolution-chart", "figure"),
    Output("proportions-chart", "figure"),
    Input("year-range", "value"),
    Input("usage-filter", "value")
)
def update_evolution_chart(year_range, usage):
    # Filtrer les données selon la période choisie
    df_filtered = df_evolution[
        (df_evolution["Year"] >= year_range[0]) &
        (df_evolution["Year"] <= year_range[1])
    ]

    # Filtrer selon l'utilisation
    if usage != "all":
        df_filtered = df_filtered[
            df_filtered["Element"] == usage
        ]

    # Construire le graphique actualisé
    fig = px.line(
        df_filtered,
        x="Year",
        y="Value",
        color="Element",
        color_discrete_map={
            "Food": "#238C88",
            "Feed": "#E6A24A"
        },
        labels={
            "Year": "Année",
            "Value": "Quantité (milliers de tonnes)",
            "Element": "Utilisation"
        }
    )

    # Appliquer notre style
    fig.update_layout(
        template="plotly_white",
        font_family="IBM Plex Sans",
        hovermode="x unified",
        legend_title_text="",
        margin=dict(l=40, r=30, t=30, b=40)
    )

    fig.update_traces(line_width=3)

    
    # Filtrer les proportions selon la période
    df_prop_filtered = df_proportions[
        (df_proportions["Year"] >= year_range[0]) &
        (df_proportions["Year"] <= year_range[1])
    ]

    # Construire le graphique des proportions
    fig_prop = px.area(
        df_prop_filtered,
        x="Year",
        y="Percentage",
        color="Element",
        category_orders={
            "Element": ["Food", "Feed"]
        },
        color_discrete_map={
            "Food": "#238C88",
            "Feed": "#E6A24A"
        },
        labels={
            "Year": "Année",
            "Percentage": "Part (%)",
            "Element": "Utilisation"
        }
    )

    fig_prop.update_layout(
        template="plotly_white",
        font_family="IBM Plex Sans",
        hovermode="x unified",
        legend_title_text="",
        yaxis=dict(range=[0, 100], ticksuffix="%"),
        margin=dict(l=40, r=30, t=30, b=40)
    )

    return fig, fig_prop