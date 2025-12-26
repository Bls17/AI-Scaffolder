# Scaffold AI CLI

Outil en ligne de commande permettant de générer la structure d’un projet à partir d’un template JSON et d’automatiser la documentation grâce à un modèle de langage (LLM).

---

## Prérequis

- Python ≥ 3.9
- pip
- (optionnel) Clé API Gemini pour la génération automatique du README

---

## Installation

Cloner le dépôt puis installer les dépendances :

```bash
pip install -r requirements.txt
```

Étape 1 – Génération de la structure (Scaffolding)
Créer un projet à partir d’un template :
python scaffold.py --template template.json

Exemple de template.json :
{
"project_name": "mon-app",
"structure": {
"src": ["main.js", "utils.js"],
"tests": ["main.test.js"]
}
}

Étape 2 – Génération automatique du README (IA)
Générer un README.md à partir de la structure créée :
python scaffold.py --template template.json --readme

Clé API (LLM)
Ce projet utilise Google Gemini pour la génération automatique de documentation.
Option 1 – Utilisation d’une clé API réelle
Définir la variable d’environnement :
export GEMINI_API_KEY="votre_cle_api"
