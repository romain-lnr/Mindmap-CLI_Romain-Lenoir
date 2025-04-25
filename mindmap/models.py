# ===============================================================
# MODULE : models.py
# DESCRIPTION : Contient la classe Node pour représenter un noeud
# - Utilisée pour structurer une carte mentale en CLI
# - Chaque noeud peut contenir des sous-noeuds hiérarchiques
# ===============================================================

# ===============================================================
# CLASSE : Node
# DESCRIPTION : Représente un noeud dans une carte mentale
# - Possède un nom unique, une description, et des enfants
# ===============================================================
class Node:

    # ---------------------------------------------------------------
    # MÉTHODE : __init__
    # Initialise un noeud avec un nom, une description
    # et une liste vide d’enfants
    # ---------------------------------------------------------------
    def __init__(self, name, description):
        self.name = name  # Nom du noeud (identifiant principal)
        self.description = description or name  # Titre ou libellé du noeud
        self.children = []  # Liste des enfants de ce noeud (sous-noeuds)

    # ---------------------------------------------------------------
    # MÉTHODE : add_child
    # Ajoute un noeud enfant à la liste des enfants
    # ---------------------------------------------------------------
    def add_child(self, child_node):
        self.children.append(child_node)

    # ---------------------------------------------------------------
    # MÉTHODE : remove_child
    # Supprime un noeud enfant à partir de son nom
    # - Ne fait rien si aucun enfant ne correspond
    # ---------------------------------------------------------------
    def remove_child(self, child_name):
        for i, child in enumerate(self.children):
            if child.name == child_name:
                del self.children[i]
                return True

