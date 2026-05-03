# machine_universelle.py

"""
PARTIE 2 — MACHINE UNIVERSELLE
Implémentation des questions 7 à 10 du projet.
"""
import sys
import os

chemin_racine = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if chemin_racine not in sys.path:
    sys.path.insert(0, chemin_racine)

from machine_de_turing.machine_de_turing import (
    filtrer_lignes_utiles,          
    charger_machine_depuis_fichier,
    configuration_initiale,
    faire_un_pas,
    simuler,
    afficher_configuration,
)

from machine_de_turing.mt_structures import MT, Configuration 

# ================================
# Q7 — CODAGE SYMBOLIQUE <M>
# ================================

def extraire_transitions(lignes):
    """
    Extrait les transitions sous forme structurée :
    [(etat, lu, nouvel_etat, ecrit, mouvement), ...]
    """
    transitions = []
    i = 0

    while i < len(lignes):
        ligne = lignes[i]

        # ignorer init / accept
        if ligne.startswith("init:") or ligne.startswith("accept:"):
            i += 1
            continue

        if ligne.count(",") == 1:
            etat, lu = [x.strip() for x in ligne.split(",")]

            i += 1
            ligne2 = lignes[i]
            nouvel_etat, ecrit, mouv = [x.strip() for x in ligne2.split(",")]

            transitions.append((etat, lu, nouvel_etat, ecrit, mouv))

        i += 1

    return transitions


def encoder_transition(t):
    """
    Encode une transition sous la forme :
    q|s|q'|s'|D
    """
    etat, lu, nouvel_etat, ecrit, mouv = t
    return f"{etat}|{lu}|{ecrit}|{mouv}|{nouvel_etat}"


def encoder_machine_symbolique(chemin):
    """
    Q7 :
    Lit une machine .tm et retourne son codage <M> avec des |.
    """
    lignes = filtrer_lignes_utiles(chemin)
    transitions = extraire_transitions(lignes)

    codes = [encoder_transition(t) for t in transitions]

    return "|".join(codes)


# ================================
# Q8 — CODAGE BINAIRE
# ================================

def caractere_vers_binaire(c):
    """
    Convertit un caractère en binaire (8 bits ASCII).
    """
    return format(ord(c), "08b")


def encoder_en_binaire(chaine):
    """
    Encode une chaîne en binaire.
    """
    return "".join(caractere_vers_binaire(c) for c in chaine)


def encoder_machine_binaire(chemin):
    """
    Retourne le codage binaire de la machine.
    """
    code_symbolique = encoder_machine_symbolique(chemin)
    return encoder_en_binaire(code_symbolique)


def binaire_vers_entier(binaire):
    """
    Convertit une chaîne binaire en entier.
    """
    return int(binaire, 2)

# ================================
# Q9 — MACHINE UNIVERSELLE (VERSION PROPRE AVEC STRUCTURES EXISTANTES)
# ================================

# -------------------------------
# DÉCODAGE BINAIRE
# -------------------------------

def binaire_vers_chaine(binaire):
    return "".join(
        chr(int(binaire[i:i+8], 2))
        for i in range(0, len(binaire), 8)
    )


# -------------------------------
# LECTURE RUBAN 2 (gestion _)
# -------------------------------

def lire_symbole(ruban, pos, blanc="_"):
    if pos < 0:
        ruban.insert(0, blanc)
        return blanc, 0
    while pos >= len(ruban):
        ruban.append(blanc)

    return ruban[pos], pos


# -------------------------------
# RECHERCHE TRANSITION DANS <M>
# -------------------------------

def chercher_transition(code_M, etat, symbole):
    elements = code_M.split("|")
    
    i = 0
    while i + 4 < len(elements):
        q = elements[i]          # état courant
        s = elements[i + 1]      # symbole lu
        s_ecrit = elements[i + 2]  # symbole à écrire
        direction = elements[i + 3] # direction
        q_next = elements[i + 4]   # nouvel état
        
        if q == etat and s == symbole:
            return q_next, s_ecrit, direction
        
        i += 5
    
    return None

# -------------------------------
# UN PAS DE LA MACHINE UNIVERSELLE
# -------------------------------

def faire_un_pas_UTM(machine, config, code_M):

    ruban1, ruban2, ruban3 = config.rubans
    pos1, pos2, pos3 = config.positions_tetes

    # lire état et symbole
    etat = ruban3[pos3]
    symbole, pos2 = lire_symbole(ruban2, pos2)
    config.positions_tetes[1] = pos2

    # chercher transition
    trans = chercher_transition(code_M, etat, symbole)

    if trans is None:
        return None

    q2, s2, D = trans

    # écrire symbole
    ruban2[pos2] = s2

    # mise à jour état
    config.rubans[2] = [q2]
    config.positions_tetes[2] = 0

    # déplacement tête ruban 2
    if D == ">":
        config.positions_tetes[1] += 1
    elif D == "<":
        config.positions_tetes[1] -= 1

    return config


# -------------------------------
# SIMULATION PRINCIPALE
# -------------------------------

def simuler_UTM(machine, config, code_M, afficher=False):

    if afficher:
        afficher_configuration(config)

    while True:

        if config.rubans[2][0] == machine.etat_final:
            break

        nouvelle = faire_un_pas_UTM(machine, config, code_M)

        if nouvelle is None:
            print("❌ Machine bloquée")
            break

        config = nouvelle

        if afficher:
            afficher_configuration(config)

    return config


# -------------------------------
# MACHINE UNIVERSELLE (POINT D'ENTRÉE)
# -------------------------------

def machine_universelle_simulation(entree_binaire, afficher=True):

    # décodage
    chaine = binaire_vers_chaine(entree_binaire)

    if "#" not in chaine:
        raise ValueError("Entrée invalide")

    code_M, x = chaine.split("#", 1)

    # -----------------------
    # MACHINE (3 rubans)
    # -----------------------

    machine = MT(
        etats=["RUN", "ACCEPT"],
        alphabet_entree=[],
        alphabet_ruban=["0", "1", "_", "|", "#"],
        blanc="_",
        etat_initial="RUN",
        etat_final="1",
        nb_rubans=3,
        transitions={}
    )

    # -----------------------
    # CONFIGURATION INITIALE
    # -----------------------

    config = Configuration(
        etat="0",
        rubans=[
            list(code_M),
            list(x) if x else ["_"],
            ["0"]
        ],
        positions_tetes=[0, 0, 0]
    )

    # -----------------------
    # SIMULATION
    # -----------------------

    return simuler_UTM(machine, config, code_M, afficher)

# ================================
# Q10 — MACHINE UNIVERSELLE AVEC LIMITE
# ================================

def machine_universelle_avec_compteur(entree_binaire, afficher=True):
    """
    Q10 : Simule M sur x pendant n étapes.
    
    Args:
        entree_binaire (str): code binaire de <M>#x#n
        afficher (bool): afficher les étapes
    
    Returns:
        (Configuration, steps_executed, limit_reached)
    """
    # 1. Décodage binaire → chaîne
    chaine = binaire_vers_chaine(entree_binaire)
    
    # 2. Séparer <M>, x et n
    if chaine.count("#") != 2:
        raise ValueError(f"Format invalide. Attendu : <M>#x#n, obtenu : {chaine}")
    
    code_M, x, n_str = chaine.split("#", 2)
    n = int(n_str)  # Nombre maximum d'étapes
    
    print(f"  Code <M>  : {code_M}")
    print(f"  Mot x     : {x}")
    print(f"  Limite n  : {n}\n")
    
    # 3. Créer la machine universelle (3 rubans)
    machine = MT(
        etats=["RUN", "ACCEPT"],
        alphabet_entree=[],
        alphabet_ruban=["0", "1", "_", "|", "#", "<", ">", "-"],
        blanc="_",
        etat_initial="RUN",
        etat_final="1",
        nb_rubans=3,
        transitions={}
    )
    
    # 4. Configuration initiale
    config = Configuration(
        etat="RUN",
        rubans=[
            list(code_M),            # Ruban 1 : code <M>
            list(x) if x else ["_"], # Ruban 2 : mot x
            ["0"]                    # Ruban 3 : état initial
        ],
        positions_tetes=[0, 0, 0]
    )
    
    # 5. Simulation avec limite
    steps = 0
    
    if afficher:
        print(f"Configuration initiale (max {n} étapes) :")
        afficher_configuration(config)
    
    while steps < n:
        # Arrêt si état final
        if config.rubans[2][0] == machine.etat_final:
            if afficher:
                print(f"✅ État final atteint en {steps} étapes")
            return config, steps, False  # False = pas de dépassement
        
        nouvelle = faire_un_pas_UTM(machine, config, code_M)
        
        if nouvelle is None:
            if afficher:
                print(f" Machine bloquée après {steps} étapes")
            return config, steps, False
        
        config = nouvelle
        steps += 1
        
        if afficher:
            print(f"--- Étape {steps}/{n} ---")
            afficher_configuration(config)
    
    limit_reached = (steps >= n)
    if afficher and limit_reached:
        print(f" Limite de {n} étapes atteinte")
    
    return config, steps, limit_reached