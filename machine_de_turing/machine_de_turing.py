# machine_de_turing.py

"""
PARTIE 1 — SIMULATEUR DE MACHINE DE TURING
Implémentation des questions 1 à 6 du projet.

Structure du fichier .tm attendu :
    init: I
    accept: F

    I,1
    X,R,>
    ...
"""

import sys
import os

# Pour permettre les imports depuis la racine du projet
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from machine_de_turing.mt_structures import Transition, MT, Configuration

# ================================
# Q2 — LECTURE ET PARSING
# ================================

def filtrer_lignes_utiles(chemin_fichier):
    """
    Lit un fichier .tm et retourne uniquement les lignes utiles
    (sans commentaires, sans lignes vides, sans espaces inutiles).
    Supprime aussi les commentaires en ligne après '//'.
    """
    lignes = []
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            # Supprimer les commentaires en ligne
            if "//" in ligne:
                ligne = ligne.split("//")[0]
            
            ligne = ligne.strip()

            if ligne == "":
                continue

            if ligne.startswith("#"):
                continue

            lignes.append(ligne)
    return lignes


def extraire_etat_initial(lignes):
    """
    Recherche la ligne 'init: <etat>' et retourne l'état initial.
    Retourne None si non trouvé.
    """
    for ligne in lignes:
        if ligne.startswith("init:"):
            return ligne.split(":")[1].strip()
    return None


def extraire_etat_final(lignes):
    """
    Recherche la ligne 'accept: <etat>' et retourne l'état final.
    Retourne None si non trouvé.
    """
    for ligne in lignes:
        if ligne.startswith("accept:"):
            return ligne.split(":")[1].strip()
    return None


def est_ligne_configuration(ligne):
    """
    Vérifie si une ligne est une directive de configuration
    (init: ou accept:).
    """
    return ligne.startswith("init:") or ligne.startswith("accept:")


def est_ligne_transition_etat(ligne):
    """
    Vérifie si une ligne correspond à la première ligne d'une transition
    (contient exactement une virgule, ex: 'I,1').
    """
    return ligne.count(",") == 1


def parser_ligne_etat(ligne):
    """
    Parse la première ligne d'une transition.
    Entrée : 'I,1'
    Retourne : ('I', '1')
    """
    etat, symbole = ligne.split(",")
    return etat.strip(), symbole.strip()


def parser_ligne_action(ligne):
    """
    Parse la deuxième ligne d'une transition.
    Entrée : 'X,R,>'
    Retourne : ('X', 'R', '>')
    """
    if ligne.count(",") != 2:
        raise ValueError(f"Transition mal formée : {ligne}")
    
    nouvel_etat, symbole_ecrit, mouvement = ligne.split(",")
    return nouvel_etat.strip(), symbole_ecrit.strip(), mouvement.strip()


def convertir_mouvement(mouvement_brut):  
    """
    Convertit un mouvement du format .tm vers le format interne.
    '<' -> 'L', '>' -> 'R', '-' -> 'S'
    """
    mapping = {"<": "L", ">": "R", "-": "S"}
    
    if mouvement_brut not in mapping:
        raise ValueError(f"Mouvement invalide : {mouvement_brut}")
    
    return mapping[mouvement_brut]


def extraire_transitions(lignes):
    """
    Parcourt les lignes et extrait toutes les transitions.
    Retourne un dictionnaire :
        clé   : (etat_courant, (symbole_lu,))
        valeur: Transition
    """
    transitions = {}
    etats = set()
    alphabet_ruban = set()
    
    i = 0
    while i < len(lignes):
        ligne = lignes[i]

        # Passer les lignes de configuration
        if est_ligne_configuration(ligne):
            i += 1
            continue

        # Détecter une transition (2 lignes consécutives)
        if est_ligne_transition_etat(ligne) and i + 1 < len(lignes):
            # Ligne 1 : état courant et symbole lu
            etat_courant, symbole_lu = parser_ligne_etat(ligne)
            
            # Ligne 2 : nouvel état, symbole écrit, mouvement
            i += 1
            ligne2 = lignes[i]
            nouvel_etat, symbole_ecrit, mouvement_brut = parser_ligne_action(ligne2)
            mouvement = convertir_mouvement(mouvement_brut)

            # Mettre à jour les ensembles
            etats.add(etat_courant)
            etats.add(nouvel_etat)
            alphabet_ruban.add(symbole_lu)
            alphabet_ruban.add(symbole_ecrit)

            # Créer la transition
            cle = (etat_courant, (symbole_lu,))
            transition = Transition(nouvel_etat, [symbole_ecrit], [mouvement])
            transitions[cle] = transition

        i += 1
    
    return transitions, etats, alphabet_ruban


def charger_machine_depuis_fichier(chemin_fichier):
    """
    Q1 & Q2 :
    Lit un fichier .tm et construit un objet MT.
    
    Format attendu :
        init: I
        accept: F
        
        I,1
        X,R,>
        ...
    """
    # 1. Lecture et filtrage des lignes
    lignes = filtrer_lignes_utiles(chemin_fichier)

    # 2. Extraction des métadonnées
    etat_initial = extraire_etat_initial(lignes)
    etat_final = extraire_etat_final(lignes)

    # 3. Extraction des transitions
    transitions, etats, alphabet_ruban = extraire_transitions(lignes)

    # 4. Ajout des états spéciaux
    if etat_initial:
        etats.add(etat_initial)
    if etat_final:
        etats.add(etat_final)

    # 5. Construction de la machine
    machine = MT(
        etats=list(etats),
        alphabet_entree=[],                    # Non utilisé pour l'instant
        alphabet_ruban=list(alphabet_ruban),
        blanc="_",                             # Convention : symbole blanc
        etat_initial=etat_initial,
        etat_final=etat_final,
        nb_rubans=1,                           # Un seul ruban par défaut
        transitions=transitions
    )

    return machine


def configuration_initiale(machine, mot):
    """
    Q2 :
    Crée la configuration initiale de la machine.
    
    - Ruban contenant le mot d'entrée (caractère par caractère)
    - Tête de lecture en position 0
    - État initial de la machine
    """
    ruban = list(mot) if mot else [machine.blanc]
    
    return Configuration(
        etat=machine.etat_initial,
        rubans=[ruban],
        positions_tetes=[0]
    )


# ================================
# Q3 — UN PAS DE CALCUL
# ================================

def corriger_position_tete(ruban, position, symbole_blanc):
    """
    Corrige la position de la tête si elle dépasse du ruban.
    Ajoute des symboles blancs si nécessaire.
    Retourne la nouvelle position.
    """
    if position < 0:
        ruban.insert(0, symbole_blanc)
        return 0
    elif position >= len(ruban):
        ruban.append(symbole_blanc)
    return position


def lire_symboles_sous_tetes(machine, configuration):
    """
    Lit les symboles sous chaque tête de lecture.
    Corrige les positions si nécessaire.
    Retourne la liste des symboles lus.
    """
    symboles_lus = []
    
    for i in range(machine.nb_rubans):
        ruban = configuration.rubans[i]
        position = configuration.positions_tetes[i]
        
        # Corriger la position si nécessaire
        configuration.positions_tetes[i] = corriger_position_tete(
            ruban, position, machine.blanc
        )
        
        symboles_lus.append(ruban[configuration.positions_tetes[i]])
    
    return symboles_lus


def chercher_transition(machine, etat, symboles_lus):
    """
    Cherche la transition correspondant à l'état courant
    et aux symboles lus. Retourne None si aucune transition trouvée.
    """
    cle = (etat, tuple(symboles_lus))
    return machine.transitions.get(cle, None)


def appliquer_ecriture(machine, configuration, transition):
    """
    Écrit les nouveaux symboles sur chaque ruban
    selon la transition.
    """
    for i in range(machine.nb_rubans):
        ruban = configuration.rubans[i]
        position = configuration.positions_tetes[i]
        ruban[position] = transition.symboles_ecrits[i]


def appliquer_mouvements(machine, configuration, transition):
    """
    Déplace les têtes de lecture selon les mouvements
    spécifiés dans la transition.
    """
    for i in range(machine.nb_rubans):
        mouvement = transition.mouvements[i]
        
        if mouvement == "L":
            configuration.positions_tetes[i] -= 1
        elif mouvement == "R":
            configuration.positions_tetes[i] += 1
        # "S" : ne rien faire


def faire_un_pas(machine, configuration):
    """
    Q3 :
    Exécute un seul pas de calcul de la machine de Turing.
    
    Étapes :
    1. Lire les symboles sous les têtes
    2. Chercher la transition correspondante
    3. Écrire les nouveaux symboles
    4. Déplacer les têtes
    5. Changer d'état
    
    Retourne la nouvelle configuration, ou None si bloquée.
    """
    # Si déjà dans l'état final, ne rien faire
    if configuration.etat == machine.etat_final:
        return None

    # 1. Lire les symboles
    symboles_lus = lire_symboles_sous_tetes(machine, configuration)

    # 2. Chercher la transition
    transition = chercher_transition(machine, configuration.etat, symboles_lus)
    if transition is None:
        return None  # Machine bloquée

    # 3. Écrire les symboles
    appliquer_ecriture(machine, configuration, transition)

    # 4. Déplacer les têtes
    appliquer_mouvements(machine, configuration, transition)

    # 5. Changer d'état
    configuration.etat = transition.nouvel_etat

    return configuration


# ================================
# Q4 — SIMULATION COMPLÈTE
# ================================

def est_simulation_terminee(configuration, machine):
    """
    Vérifie si l'état final est atteint.
    """
    return configuration.etat == machine.etat_final


def simuler(machine, mot, afficher=False, max_pas=1000):
    """
    Q4 :
    Simule la machine de Turing sur un mot d'entrée.
    
    La simulation s'arrête quand :
    - L'état final est atteint
    - Aucune transition n'est possible (machine bloquée)
    
    Args:
        machine : objet MT
        mot : chaîne de caractères (mot d'entrée)
        afficher : bool, si True affiche chaque configuration
    
    Returns:
        La configuration finale
    """
    # 1. Configuration initiale
    configuration = configuration_initiale(machine, mot)
    
    if afficher:
        afficher_configuration(configuration)

    # 2. Boucle de simulation
    while not est_simulation_terminee(configuration, machine):
        nouvelle_config = faire_un_pas(machine, configuration)
        
        if nouvelle_config is None:
            break  # Machine bloquée
        
        configuration = nouvelle_config
        
        if afficher:
            afficher_configuration(configuration)
        
    
    return configuration


# ================================
# Q5 — AFFICHAGE DES CONFIGURATIONS
# ================================

def formater_ruban(ruban):
    """
    Formate le contenu d'un ruban pour affichage.
    Exemple : ['1', '0', '_'] -> '1 0 _'
    """
    return " ".join(str(x) for x in ruban)

def formater_position_tete(ruban, position):
    """
    Affiche correctement la tête sous le bon symbole.
    """
    affichage = " ".join(str(x) for x in ruban)

    # position réelle = chaque élément = 2 chars environ ("x ")
    index_char = position * 2

    return " " * index_char + " ^"


def afficher_configuration(configuration):
    """
    Q5 :
    Affiche une configuration de la machine :
    - État courant
    - Contenu de chaque ruban
    - Position de chaque tête
    
    Format d'affichage :
        Ruban : 1 0 _ 1
                ^
        État  : q1
        ----------------------------------
    """
    for i in range(len(configuration.rubans)):
        ruban = configuration.rubans[i]
        position = configuration.positions_tetes[i]

        affichage = formater_ruban(ruban)

        if len(configuration.rubans) > 1:
            print(f"Ruban {i+1} : {affichage}")
        else:
            print(f"Ruban : {affichage}")

        print(f"       {formater_position_tete(ruban, position)}")

    print(f"État  : {configuration.etat}")
    print("-" * 40)


# ================================
# Q6 — MACHINES DE TURING PRÉDÉFINIES
# ================================

def charger_machine_comparaison():
    """
    Q6 : Machine de comparaison d'entiers en binaire.
    Entrée : x#y (x,y en binaire)
    S'arrête si x < y, boucle sinon.
    """
    chemin = os.path.join(
        os.path.dirname(__file__), "machines", "comparaison.tm"
    )
    return charger_machine_depuis_fichier(chemin)


def charger_machine_recherche():
    """
    Q6 : Machine de recherche dans une liste.
    Entrée : x#w1#w2#...#wl
    S'arrête si x = wi, boucle sinon.
    """
    chemin = os.path.join(
        os.path.dirname(__file__), "machines", "recherche.tm"
    )
    return charger_machine_depuis_fichier(chemin)


def charger_machine_multiplication_unaire():
    """
    Q6 : Machine de multiplication en unaire.
    Entrée : 1^n # 1^m
    Sortie : 1^{n*m}
    """
    chemin = os.path.join(
        os.path.dirname(__file__), "machines", "multiplication_unaire.tm"
    )
    return charger_machine_depuis_fichier(chemin)


def charger_machine_multiplication_binaire():
    """
    Q6 (Bonus) : Machine de multiplication en binaire.
    Entrée : x#y (x,y en binaire)
    Sortie : x*y en binaire
    """
    chemin = os.path.join(
        os.path.dirname(__file__), "machines", "multiplication_binaire.tm"
    )
    return charger_machine_depuis_fichier(chemin)
