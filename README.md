# Dazzle Dash, Exploration des données alimentaires mondiales

## Présentation du projet

**Dazzle Dash** est un projet de Data Storytelling réalisé dans le cadre de notre formation à La Plateforme.

L'objectif est d'explorer et de visualiser les données alimentaires de la **FAO (Organisation des Nations unies pour l'alimentation et l'agriculture)**, afin de mieux comprendre l'évolution des quantités destinées à deux usages :

- **Food** : alimentation humaine ;
- **Feed** : alimentation animale.

L'analyse porte sur la période **1961 à 2013** et s'appuie sur des visualisations interactives réalisées avec **Plotly et Dash**.

## Fonctionnalités de l'application

L'application comprend quatre pages :

- **Accueil** : présentation du projet, du jeu de données et des différents espaces d'exploration.
- **Évolutions** : analyse des quantités Food et Feed au fil du temps, avec des graphiques interactifs et un filtre de période.
- **Produits** : classement des produits alimentaires et comparaison de leur répartition entre Food et Feed.
- **Géographie** : carte mondiale interactive et classement des territoires selon les quantités enregistrées.

Les visualisations peuvent être explorées grâce à différents filtres : période, utilisation alimentaire et nombre de produits affichés.

## Technologies utilisées

- **Python** : traitement des données et développement.
- **Pandas** : nettoyage, transformation et analyse des données.
- **Plotly** : création des graphiques interactifs.
- **Dash** : développement de l'application web multipage.
- **HTML / CSS** : structure et personnalisation de l'interface.
- **Jupyter Notebook** : exploration et analyse des données.

## Organisation du projet

```text
dazzle-dash/
├── app.py
├── index.py
├── layout.py
├── pages/
│   ├── accueil.py
│   ├── evolutions.py
│   ├── produits.py
│   └── geographie.py
├── assets/
│   ├── style.css
│   └── hero-alimentation.jpg
├── data/
│   ├── FAO.csv
│   └── FAO_clean.csv
├── notebooks/
│   ├── 01_exploration_nettoyage_fao.ipynb
│   └── 02_analyse_exploratoire_fao.ipynb
├── docs/
├── requirements.txt
└── README.md
```

## Installation et lancement

**1. Cloner le dépôt et accéder au projet**

```bash
git clone <URL_DU_DEPOT>
cd dazzle-dash
```

**2. Créer et activer un environnement virtuel**

```bash
python -m venv .venv
```

Sous Windows :

```bash
.venv\Scripts\activate
```

**3. Installer les dépendances**

```bash
python -m pip install -r requirements.txt
```

**4. Lancer l'application**

```bash
python index.py
```

Ouvrir ensuite l'adresse suivante dans un navigateur :

http://127.0.0.1:8050/

## Données et limites

Le projet utilise le fichier `FAO.csv`, préparé et nettoyé dans le premier notebook. Les données transformées sont enregistrées dans `FAO_clean.csv`.

Les quantités sont exprimées en **milliers de tonnes**.

Certaines données historiques sont manquantes et plusieurs catégories de produits peuvent se chevaucher. Les résultats doivent donc être interprétés avec précaution, notamment lors des comparaisons entre produits et territoires.

## Documentation

Les étapes détaillées du projet sont présentées dans la documentation complémentaire et les notebooks :

- Recherche sur le Data Storytelling et découverte de Dash ;
- Exploration et nettoyage des données FAO ;
- Analyse exploratoire et visualisations ;
- Conception et développement de l'application.

## Auteurs

Assmine AHAMADA & Noémie FERAUD