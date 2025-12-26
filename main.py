import json
import os
import argparse
import sys
import google.generativeai as genai


def load_template(template_path: str) -> dict:
    if not os.path.exists(template_path):
        print(f" Fichier introuvable : {template_path}")
        sys.exit(1)

    with open(template_path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_project(template: dict):
    project_name = template.get("project_name")
    structure = template.get("structure")

    if not project_name or not structure:
        print(" template.json invalide (project_name ou structure manquant)")
        sys.exit(1)

    os.makedirs(project_name, exist_ok=True)
    print(f" Création du projet : {project_name}")

    for folder, files in structure.items():
        folder_path = os.path.join(project_name, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f" {folder}/")

        for file in files:
            file_path = os.path.join(folder_path, file)
            open(file_path, "w").close()
            print(f" {file}")


def analyze_project_structure(project_path: str) -> str:
    description = ""
    for root, dirs, files in os.walk(project_path):
        level = root.replace(project_path, "").count(os.sep)
        indent = "  " * level
        description += f"{indent}{os.path.basename(root)}/\n"
        for file in files:
            description += f"{indent}  - {file}\n"
    return description


def generate_readme_with_gemini(project_name: str, structure: str) -> str:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
Tu es un expert en documentation logicielle.

Génère un fichier README.md professionnel pour un projet nommé "{project_name}".

Structure du projet :
{structure}

Le README doit contenir :
- Description du projet
- Structure des fichiers
- Instructions d'installation
- Instructions d'exécution
- Technologies utilisées
"""

    response = model.generate_content(prompt)
    return response.text


def save_readme(project_path: str, content: str):
    readme_path = os.path.join(project_path, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold CLI – Générateur de structure de projet"
    )
    parser.add_argument(
        "--template", required=True, help="Chemin vers le fichier template.json"
    )
    parser.add_argument(
        "--readme",
        action="store_true",
        help="Génère un README.md avec l'aide de LLM(Gemini)",
    )

    args = parser.parse_args()

    template = load_template(args.template)
    create_project(template)

    print(" Scaffolding terminé avec succès")

    if args.readme:
        project_name = template["project_name"]
        structure_desc = analyze_project_structure(project_name)

        readme = generate_readme_with_gemini(project_name, structure_desc)
        save_readme(project_name, readme)

        print("README.md généré avec succès via Gemini")


if __name__ == "__main__":
    main()
