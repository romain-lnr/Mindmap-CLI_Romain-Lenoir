# MindMap CLI

Outil en ligne de commande pour créer et gérer des cartes mentales (mindmaps) avec persistance en JSON.

## Installation

1. **Prérequis** :
   - Python 3.8+
   - pip

2. **Installer le projet** :
    git clone https://github.com/romain-lnr/Mindmap-CLI_Romain-Lenoir.git
    
3. **Installer les dépendances** :
   pip install -r requirements.txt

## Lancement du programme

    python main.py

## **Commandes principales**

    create <nom>	        Crée une nouvelle mindmap	    create mon_projet
    load <fichier>	        Charge une mindmap existante	load mon_projet.json
    add <parent> <enfant>	Ajoute un nœud enfant	        add Racine mon_noeud
    delete <noeud>	        Supprime un nœud	            delete mon_noeud
    display     	        Affiche la mindmap	            display
    find <noeud>	        Recherche un nœud	            find mon_noeud
    save	                Sauvegarde les modifications	save
    exit	                Quitte l'application	        exit