import json
import os
import argparse
import sys


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


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold CLI – Générateur de structure de projet"
    )
    parser.add_argument(
        "--template", required=True, help="Chemin vers le fichier template.json"
    )

    args = parser.parse_args()

    template = load_template(args.template)
    create_project(template)

    print(" Scaffolding terminé avec succès")


if __name__ == "__main__":
    main()
