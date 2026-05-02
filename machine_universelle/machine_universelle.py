# machine_universelle.py

"""
PARTIE 2 — MACHINE UNIVERSELLE
Implémentation des questions 7 à 10 du projet.
"""
import sys
import os

# Cela permet de faire des imports absolus depuis n'importe où dans le projet
chemin_racine = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if chemin_racine not in sys.path:
    sys.path.insert(0, chemin_racine)

from machine_de_turing.machine_de_turing import (
    filtrer_lignes_utiles,          
    charger_machine_depuis_fichier,
    configuration_initiale,
    faire_un_pas,
    simuler,
)

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
    return f"{etat}|{lu}|{nouvel_etat}|{ecrit}|{mouv}"


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
    Q8 :
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
# Q9 — MACHINE UNIVERSELLE (SIMULATION)
# ================================


def decoder_machine(chemin):
    """
    Charge une machine M depuis un fichier.
    """
    return charger_machine_depuis_fichier(chemin)


def machine_universelle_simulation(chemin_machine, mot, afficher=False):
    """
    Simule U(<M>, x) en utilisant ton simulateur existant.

    👉 Equivalent à :
        U(<M>, x) = M(x)
    """
    machine = decoder_machine(chemin_machine)
    return simuler(machine, mot, afficher=afficher)

# ================================
# Q10 — MACHINE UNIVERSELLE AVEC LIMITE
# ================================

def simuler_avec_limite(machine, mot, max_steps, afficher=False):
    """
    Simule une machine avec une limite de nombre d'étapes.
    """
    config = configuration_initiale(machine, mot)
    steps = 0

    if afficher:
        print("Configuration initiale :")
    
    while steps < max_steps:
        if config.etat == machine.etat_final:
            return config, steps

        new_config = faire_un_pas(machine, config)

        if new_config is None:
            return config, steps

        config = new_config
        steps += 1

    return config, steps  # limite atteinte


def machine_universelle_avec_compteur(chemin_machine, mot, n, afficher=False):
    """
    Simule U(<M>, x, n) : exécute M sur x pendant au plus n étapes.
    """
    machine = decoder_machine(chemin_machine)
    return simuler_avec_limite(machine, mot, n, afficher)