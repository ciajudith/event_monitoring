# Surveillance d'événements (Event Monitoring)

Ce projet implémente une chaîne de traitement d'événements à partir d'un fichier de logs, génère des alertes, produit des statistiques visuelles et un rapport PDF, et propose une interface utilisateur basique.

---

## Structure du projet

Voici la structure du projet :

```
event_monitoring/
├── input/                   # Dossier d'entrée
│   └── events.log          # Fichier de logs à analyser
├── outputs/                 # Dossier de sortie
│   ├── alerts.json         # Alertes détectées au format JSON
│   ├── stats.png           # Graphique des statistiques
│   └── report.pdf          # Rapport PDF généré
├── src/                     # Code source
│   ├── main.py             # Point d'entrée de l'application
│   ├── fonts/              
│   │   └── NotoEmoji-Regular.ttf  # Police utilisée pour les icones dans le PDF
│   ├── models/              # Définitions des classes métiers
│   │   ├── alert.py      
│   │   ├── event.py      
│   │   ├── event_analyzer.py # Analyseur d'événements
│   │   └── event_logger.py # Logger personnalisé
│   └── utils/              # Fonctions utilitaires
│       ├── processing.py   # Chargement et prétraitement des données
│       ├── plot_generation.py # Génération de graphiques
│       ├── report_generation.py # Création du rapport PDF
│       └── ui_interface.py # Interface utilisateur (CLI ou basique)
├── README.md             
└── requirements.txt        # Dépendances Python
```

---

## Installation

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com/ciajudith/event_monitoring
   cd event_monitoring
   ```

2. **Créer et activer un environnement virtuel**

   ```bash
   python -m venv .venv
   # Sous macOS/Linux
   source .venv/bin/activate
   # Sous Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   ```

3. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```


## Usage

Depuis la racine du projet et avec l'environnement virtuel activé, lancez l'application avec la commande suivante:

```bash

python -m src.main
```

---

## Fonctionnalités

1. **Chargement et prétraitement** (`utils/processing.py`) : parsing des lignes de logs en objets `Event`.
2. **Analyse d'événements** (`models/event_analyzer.py`) : détection d'anomalies et création d'objets `Alert`.
3. **Génération de graphiques** (`utils/plot_generation.py`) : production d'un histogramme ou d'un graphique de tendance enregistré en `stats.png`.
4. **Génération de rapport** (`utils/report_generation.py`) : agrégation des résultats et création d'un PDF `report.pdf`.
5. **Interface utilisateur** (`utils/ui_interface.py`) : quelques fonctions CLI pour lancer chaque étape manuellement.

---
>***Made by @ciajudith.***
