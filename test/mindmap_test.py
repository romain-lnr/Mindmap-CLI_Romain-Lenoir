# ===============================================================
# MODULE : test_mindmap.py
# DESCRIPTION : Tests unitaires pour l'application MindMap CLI
# - Utilise pytest pour tester les modules : models, manager, storage
# - Vérifie la validité de la logique métier et la persistance
# ===============================================================

import pytest
import os
from mindmap.models import Node
from mindmap.manager import MindMap
from mindmap.storage import save_mindmap, load_mindmap

# ===============================================================
# FIXTURES
# DESCRIPTION : Création de jeux de données temporaires pour les tests
# ===============================================================

# ---------------------------------------------------------------
# FIXTURE : mindmap_test
# Crée une structure simple de carte mentale pour tester les actions
# ---------------------------------------------------------------
@pytest.fixture
def mindmap_test():
    mm = MindMap("Racine", "Projet Principal")
    mm.add_node_by_parent("Racine", "Développement", "Backend")
    mm.add_node_by_parent("Développement", "API", "Endpoints")
    mm.add_node_by_parent("Racine", "Design", "UI/UX")
    return mm

# ---------------------------------------------------------------
# FIXTURE : temp_file
# Fournit un chemin vers un fichier temporaire JSON
# ---------------------------------------------------------------
@pytest.fixture
def temp_file(tmp_path):
    return os.path.join(tmp_path, "test_mindmap.json")

# ===============================================================
# TESTS : Classe Node
# ===============================================================
class TestNode:

    # ---------------------------------------------------------------
    # TEST : test_node_creation
    # Vérifie la création d’un noeud avec nom et description
    # ---------------------------------------------------------------
    def test_node_creation(self):
        node = Node("Test", "Description")
        assert node.name == "Test"
        assert node.description == "Description"
        assert len(node.children) == 0

    # ---------------------------------------------------------------
    # TEST : test_add_child
    # Vérifie l’ajout d’un enfant à un noeud parent
    # ---------------------------------------------------------------
    def test_add_child(self):
        parent = Node("Parent", "Parent_description")
        child = Node("Enfant", "Enfant_description")
        parent.add_child(child)
        assert len(parent.children) == 1
        assert parent.children[0].name == "Enfant"

    # ---------------------------------------------------------------
    # TEST : test_remove_child
    # Vérifie la suppression d’un enfant par nom
    # ---------------------------------------------------------------
    def test_remove_child(self):
        parent = Node("Parent", "Parent_description")
        child1 = Node("Enfant1", "Enfant1_description")
        child2 = Node("Enfant2", "Enfant2_description")
        parent.add_child(child1)
        parent.add_child(child2)
        parent.remove_child("Enfant1")
        assert len(parent.children) == 1
        assert parent.children[0].name == "Enfant2"

# ===============================================================
# TESTS : Classe MindMap
# ===============================================================
class TestMindMap:

    def test_mindmap_creation(self):
        mm = MindMap("Racine", "Description")
        assert mm.root.name == "Racine"
        assert mm.root.description == "Description"

    def test_add_node(self, mindmap_test):
        assert len(mindmap_test.root.children) == 2
        dev_node = next(n for n in mindmap_test.root.children if n.name == "Développement")
        assert len(dev_node.children) == 1
        assert dev_node.children[0].name == "API"

    def test_add_node_duplicate(self, mindmap_test):
        with pytest.raises(ValueError, match="existe déjà"):
            mindmap_test.add_node_by_parent("Racine", "Développement")

    def test_depth_limit(self, mindmap_test):
        with pytest.raises(ValueError, match="Limite de sous-branches"):
            mindmap_test.add_node_by_parent("API", "Nouveau")

    def test_find_node_by_name(self, mindmap_test):
        node = mindmap_test.find_node_by_name("API")
        assert node is not None
        assert node.description == "Endpoints"

    def test_find_nonexistent_node(self, mindmap_test):
        assert mindmap_test.find_node_by_name("Inexistant") is None

    def test_find_node_path(self, mindmap_test):
        path = mindmap_test.find_node_path_by_name("API")
        assert path == "Racine >> Développement >> API"

    def test_remove_node(self, mindmap_test):
        assert mindmap_test.remove_node_by_name("Design")
        assert mindmap_test.find_node_by_name("Design") is None

    def test_remove_nonexistent_node(self, mindmap_test):
        assert not mindmap_test.remove_node_by_name("Inexistant")

    def test_remove_root_node(self, mindmap_test):
        assert not mindmap_test.remove_node_by_name("Racine")

    def test_display(self, mindmap_test, capsys):
        mindmap_test.display()
        captured = capsys.readouterr()
        assert "Racine" in captured.out
        assert "Développement" in captured.out
        assert "API" in captured.out

# ===============================================================
# TESTS : Persistance (sauvegarde/chargement)
# ===============================================================
class TestStorage:

    def test_save_and_load(self, mindmap_test, temp_file):
        save_mindmap(mindmap_test, temp_file)
        assert os.path.exists(temp_file)

        loaded_mm = load_mindmap(temp_file)
        assert loaded_mm.root.name == "Racine"
        assert len(loaded_mm.root.children) == 2
        dev_node = next(n for n in loaded_mm.root.children if n.name == "Développement")
        assert len(dev_node.children) == 1
        assert dev_node.children[0].name == "API"

    def test_load_nonexistent_file(self):
        with pytest.raises(FileNotFoundError):
            load_mindmap("nonexistent.json")

# ===============================================================
# TEST : test_depth_limit_enforcement
# Vérifie qu'on ne dépasse pas la limite de profondeur
# ===============================================================
def test_depth_limit_enforcement():
    mm = MindMap("Niveau1")
    mm.add_node_by_parent("Niveau1", "Niveau2")
    mm.add_node_by_parent("Niveau2", "Niveau3")
    with pytest.raises(ValueError, match="Limite de sous-branches"):
        mm.add_node_by_parent("Niveau3", "Niveau4")

# ===============================================================
# TEST : test_complex_path_handling
# Vérifie la manipulation de chemins complexes dans la hiérarchie
# ===============================================================
def test_complex_path_handling():
    mm = MindMap("Racine")
    mm.add_node_by_parent("Racine", "A")
    mm.add_node_by_parent("A", "B")
    mm.add_node_by_parent("Racine", "C")
    mm.add_node_by_parent("C", "D")

    assert mm.find_node_path_by_name("B") == "Racine >> A >> B"
    assert mm.find_node_path_by_name("D") == "Racine >> C >> D"
