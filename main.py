# ==============================================================================
# FICHIER : main.py
# DESCRIPTION :
#     Interface en ligne de commande pour manipuler une carte mentale.
#     Permet de créer, afficher, modifier, sauvegarder et charger une carte.
#
# COMMANDES :
#     - create <nom> <titre>           : Crée une nouvelle carte mentale
#     - add <parent> <nom> <titre>     : Ajoute un noeud sous un parent
#     - remove <nom>                   : Supprime un noeud par son nom
#     - display                        : Affiche la carte
#     - find <nom>                     : Recherche le chemin d’un noeud
#     - save <fichier.json>            : Sauvegarde la carte dans un fichier JSON
#     - load <fichier.json>            : Charge une carte à partir d’un fichier JSON
#     - help                           : Affiche l’aide
#     - exit                           : Quitte le programme
#
# AUTEUR : Romain Lenoir
# ==============================================================================

import os
from mindmap.manager import MindMap
from mindmap.storage import save_mindmap, load_mindmap

# ---------------------------------------------------------------
# FONCTION : print_help
# Affiche la liste des commandes disponibles à l'utilisateur
# ---------------------------------------------------------------
def print_help():
    print("""
Commandes disponibles :
  create <nom> <titre>            - Créer une nouvelle carte mentale
  add <parent> <nom> <titre>      - Ajouter un noeud
  remove <noeud>                  - Supprimer un noeud
  display                         - Afficher la carte
  find <noeud>                    - Trouver le chemin d'un noeud spécifique
  save <fichier.json>             - Sauvegarder la carte dans un fichier
  load <fichier.json>             - Charger une carte depuis un fichier
  help                            - Afficher cette aide
  exit                            - Quitter le programme
""")

# ---------------------------------------------------------------
# FONCTION : main
# Fonction principale qui exécute la boucle de commande interactive
# ---------------------------------------------------------------
def main():
    mindmap = None
    filename = None
    prompt = ">> "

    print("--- MindMap CLI")
    print_help()

    while True:
        try:
            command = input(prompt).strip()
            if not command:
                continue

            parts = command.split(" ", 2)
            cmd = parts[0].lower()

            if cmd == 'exit':
                break

            elif cmd == 'help':
                print_help()

            elif cmd == 'create':
                parts = command.split(" ", 2)
                if len(parts) < 3:
                    print("Usage : create <nom> <titre>")
                    continue
                name = parts[1]
                description = parts[2]
                prompt = "(unsaved) >> "
                mindmap = MindMap(name, description)
                print(f"Nouvelle carte créée avec la racine '{name}' et le titre '{description}'.")

            elif cmd == 'add':
                parts = command.split(" ", 3)
                if mindmap is None:
                    print("Aucune carte chargée. Utilise 'create' ou 'load'.")
                    continue
                if len(parts) < 4:
                    print("Usage : add <parent> <name> <description>")
                    continue

                parent = parts[1]
                name = parts[2]
                description = parts[3]

                added = mindmap.add_node_by_parent(parent, name, description)
                if added:
                    print(f"Noeud '{name}' ajouté sous '{parent}' avec le titre '{description}'.")
                else:
                    print(f"Parent '{parent}' introuvable ou nom déjà utilisé.")

            elif cmd == 'remove':
                parts = command.split(" ", 1)
                if mindmap is None:
                    print("Aucune carte chargée.")
                    continue
                if len(parts) < 2:
                    print("Usage : remove <noeud>")
                    continue
                node_name = parts[1]
                removed = mindmap.remove_node_by_name(node_name)
                if removed:
                    print(f"noeud '{node_name}' supprimé.")
                else:
                    print(f"noeud '{node_name}' introuvable ou tentative de suppression de la racine.")

            elif cmd == 'display':
                if mindmap is None:
                    print("Aucune carte à afficher.")
                    continue
                mindmap.display()

            elif cmd == 'find':
                parts = command.split(" ", 1)
                if mindmap is None:
                    print("Aucune carte à rechercher.")
                    continue
                if len(parts) < 2:
                    print("Usage : find <nom_du_noeud>")
                    continue
                node_name = parts[1]
                path = mindmap.find_node_path_by_name(node_name)
                if path:
                    print(f"{node_name} = {path}")
                else:
                    print(f"noeud '{node_name}' non trouvé.")

            elif cmd == 'save':
                parts = command.split(" ", 1)
                if mindmap is None:
                    print("Aucune carte à sauvegarder.")
                    continue
                if len(parts) < 2:
                    print("Usage : save <fichier.json>")
                    continue
                if not parts[1].endswith(".json"):
                    filename = f"data/{parts[1]}.json"
                else:
                    filename = f"data/{parts[1]}"
                
                if not os.path.exists("data"):
                    os.makedirs("data")

                save_mindmap(mindmap, filename)
                prompt = f"({filename}) >> "
                print(f"Carte sauvegardée dans '{filename}'.")

            elif cmd == 'load':
                parts = command.split(" ", 1)
                if len(parts) < 2:
                    print("Usage : load <fichier.json>")
                    continue
                if not parts[1].startswith("data/"):
                    parts[1] = f"data/{parts[1]}"
                
                if not parts[1].endswith(".json"):
                    filename = f"{parts[1]}.json"
                else:
                    filename = parts[1]

                mindmap = load_mindmap(filename)
                prompt = f"({filename}) >> "
                print(f"Carte chargée depuis '{filename}'.")

            else:
                print(f"Commande inconnue : {cmd}. Tapez 'help' pour voir les commandes.")

        except Exception as e:
            print(f"Erreur : {e}")

# ---------------------------------------------------------------
# POINT D’ENTRÉE
# Exécute la boucle principale si le fichier est lancé directement
# ---------------------------------------------------------------
if __name__ == "__main__":
    main()
