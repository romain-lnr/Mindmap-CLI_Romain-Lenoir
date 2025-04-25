# ===============================================================
# MODULE : mindmap.py
# DESCRIPTION : Classe MindMap pour gérer une carte mentale via CLI
# - Utilise la librairie 'rich' pour un affichage en arbre stylisé
# - Les noeuds sont représentés avec la classe Node (modèle externe)
# ===============================================================

from mindmap.models import Node
from rich.console import Console
from rich.tree import Tree

# ===============================================================
# CLASSE : MindMap
# DESCRIPTION : Représente une carte mentale composée de noeuds hiérarchiques
# ===============================================================
class MindMap:
    
    # ---------------------------------------------------------------
    # MÉTHODE : __init__
    # Crée une carte mentale avec un noeud racine
    # ---------------------------------------------------------------
    def __init__(self, root_name, root_title=None):
        self.root = Node(root_name, root_title)
        self.console = Console()
        
    # ---------------------------------------------------------------
    # MÉTHODE : get_depth
    # Retourne la profondeur d'un noeud donné dans la hiérarchie
    # ---------------------------------------------------------------
    def get_depth(self, node, current_node=None, depth=1):
        if current_node is None:
            current_node = self.root
        if current_node == node:
            return depth
        for child in current_node.children:
            d = self.get_depth(node, child, depth + 1)
            if d is not None:
                return d
        return None

    # ---------------------------------------------------------------
    # MÉTHODE : find_node_path_by_name
    # Retourne le chemin complet d’un noeud à partir de son nom
    # ---------------------------------------------------------------
    def find_node_path_by_name(self, node_name, current_node=None, path=None):
        if current_node is None:
            current_node = self.root
        if path is None:
            path = [current_node.name]
        if current_node.name == node_name:
            return " >> ".join(path)
        for child in current_node.children:
            new_path = path + [child.name]
            found_path = self.find_node_path_by_name(node_name, child, new_path)
            if found_path:
                return found_path
        return None

    # ---------------------------------------------------------------
    # MÉTHODE : find_node_by_name
    # Recherche récursive d’un noeud par son nom
    # ---------------------------------------------------------------
    def find_node_by_name(self, name, node=None):
        if node is None:
            node = self.root
        if node.name == name:
            return node
        for child in node.children:
            found = self.find_node_by_name(name, child)
            if found:
                return found
        return None
        
    # ---------------------------------------------------------------
    # MÉTHODE : add_node_by_parent
    # Ajoute un noeud enfant sous un noeud parent donné
    # ---------------------------------------------------------------
    def add_node_by_parent(self, parent_name, name, title=None):        
        parent_node = self.find_node_by_name(parent_name)
        if parent_node:
            if any(child.name == name for child in parent_node.children):
                raise ValueError(f"Un noeud nommé '{name}' existe déjà sous '{parent_name}'.")
            depth = self.get_depth(parent_node)
            if depth is not None and depth >= 3:
                raise ValueError("Limite de sous-branches (3) atteinte")
            parent_node.add_child(Node(name, title))
            return True
        return False

    # ---------------------------------------------------------------
    # MÉTHODE : remove_node_by_name
    # Supprime un noeud par son nom de manière récursive
    # ---------------------------------------------------------------
    def remove_node_by_name(self, name):
        if self.root.name == name:
            return False
        return self.root.remove_child(name)

    # ---------------------------------------------------------------
    # MÉTHODE : display
    # Affiche la carte mentale dans le terminal avec rich.tree
    # ---------------------------------------------------------------
    def display(self):
        tree = Tree(f"[bold green]{self.root.name} ({self.root.description})[/bold green]")
        self._add_children_to_tree(self.root, tree)
        self.console.print(tree)

    # ---------------------------------------------------------------
    # MÉTHODE PRIVÉE : _add_children_to_tree
    # Ajoute récursivement les enfants dans l'arbre rich
    # ---------------------------------------------------------------
    def _add_children_to_tree(self, node, tree):
        for child in node.children:
            branch = tree.add(f"{child.name} ({child.description})", style="blue")
            self._add_children_to_tree(child, branch)
