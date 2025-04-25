# ===============================================================
# MODULE : storage.py
# DESCRIPTION : Gère la sérialisation et la désérialisation des cartes mentales
# - Convertit les noeuds en dictionnaires et inversement
# - Sauvegarde et chargement des cartes mentales au format JSON
# ===============================================================

import json
from mindmap.models import Node

# ---------------------------------------------------------------
# FONCTION : node_to_dict
# Convertit un noeud Node en dictionnaire (récursivement)
# ---------------------------------------------------------------
def node_to_dict(node):
    return {
        'name': node.name,
        'description': node.description,
        'children': [node_to_dict(child) for child in node.children]
    }

# ---------------------------------------------------------------
# FONCTION : dict_to_node
# Convertit un dictionnaire en noeud Node (récursivement)
# ---------------------------------------------------------------
def dict_to_node(data):
    node = Node(data['name'], data.get('description', ''))
    for child_data in data.get('children', []):
        node.children.append(dict_to_node(child_data))
    return node

# ---------------------------------------------------------------
# FONCTION : save_mindmap
# Sauvegarde la carte mentale au format JSON
# ---------------------------------------------------------------
def save_mindmap(mindmap, filename):
    with open(filename, 'w') as f:
        json.dump(node_to_dict(mindmap.root), f, indent=2)

# ---------------------------------------------------------------
# FONCTION : load_mindmap
# Charge une carte mentale depuis un fichier JSON
# ---------------------------------------------------------------
def load_mindmap(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    from mindmap.manager import MindMap
    mindmap = MindMap(data['name'])
    mindmap.root = dict_to_node(data)
    return mindmap
