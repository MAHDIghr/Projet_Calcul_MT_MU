# test_machine_de_turing.py

"""
Tests unitaires pour le simulateur de machine de Turing.
Couvre les questions 1 à 5 avec des assertions.
"""

import sys
import os
import tempfile

# Ajouter la racine du projet au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from machine_de_turing.mt_structures import Transition, MT, Configuration
from machine_de_turing.machine_de_turing import (
    # Q1 & Q2 — Parsing
    filtrer_lignes_utiles,
    extraire_etat_initial,
    extraire_etat_final,
    est_ligne_configuration,
    est_ligne_transition_etat,
    parser_ligne_etat,
    parser_ligne_action,
    convertir_mouvement,
    extraire_transitions,
    charger_machine_depuis_fichier,

    # Q2 — Configuration initiale
    configuration_initiale,

    # Q3 — Pas de calcul
    corriger_position_tete,
    lire_symboles_sous_tetes,
    chercher_transition,
    appliquer_ecriture,
    appliquer_mouvements,
    faire_un_pas,

    # Q4 — Simulation
    est_simulation_terminee,
    simuler,

    # Q5 — Affichage
    formater_ruban,
    formater_position_tete,
    afficher_configuration,
)

# ================================
# FIXTURES
# ================================

def creer_fichier_tm_temporel(contenu):
    """Crée un fichier .tm temporaire pour les tests."""
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".tm", delete=False, encoding="utf-8"
    )
    tmp.write(contenu)
    tmp.close()
    return tmp.name


def creer_machine_simple():
    """Crée une machine simple qui accepte les mots finissant par 'a'."""
    contenu = """// Machine de test : accepte les mots finissant par 'a'
init: q0
accept: ACCEPT

q0,a
qa,a,>

q0,b
qb,b,>

qa,a
qa,a,>

qa,b
qb,b,>

qa,_
ACCEPT,_,-

qb,a
qa,a,>

qb,b
qb,b,>
"""
    chemin = creer_fichier_tm_temporel(contenu)
    machine = charger_machine_depuis_fichier(chemin)
    os.unlink(chemin)
    return machine


def creer_machine_flip():
    """Crée une machine qui inverse 0 et 1."""
    contenu = """// Machine flip : 0->1, 1->0
init: start
accept: ACCEPT

start,0
start,1,>

start,1
start,0,>

start,_
ACCEPT,_,-
"""
    chemin = creer_fichier_tm_temporel(contenu)
    machine = charger_machine_depuis_fichier(chemin)
    os.unlink(chemin)
    return machine


# ================================
# TESTS Q1 & Q2 — PARSING
# ================================

def test_filtrer_lignes_utiles():
    """Test du filtrage des lignes : suppression commentaires et lignes vides."""
    contenu = "// commentaire\n\ninit: I\n# autre commentaire\n\nI,1\nX,R,>\n"
    chemin = creer_fichier_tm_temporel(contenu)

    lignes = filtrer_lignes_utiles(chemin)
    os.unlink(chemin)

    assert lignes == ["init: I", "I,1", "X,R,>"], f"Lignes obtenues : {lignes}"
    print("  ✓ filtrer_lignes_utiles")


def test_extraire_etat_initial():
    """Test de l'extraction de l'état initial."""
    assert extraire_etat_initial(["init: q0", "accept: F"]) == "q0"
    assert extraire_etat_initial(["accept: F"]) is None
    assert extraire_etat_initial(["init:   start  "]) == "start"
    print("  ✓ extraire_etat_initial")


def test_extraire_etat_final():
    """Test de l'extraction de l'état final."""
    assert extraire_etat_final(["init: q0", "accept: ACCEPT"]) == "ACCEPT"
    assert extraire_etat_final(["init: q0"]) is None
    assert extraire_etat_final(["accept:   F  "]) == "F"
    print("  ✓ extraire_etat_final")


def test_est_ligne_configuration():
    """Test de la détection des lignes de configuration."""
    assert est_ligne_configuration("init: q0") == True
    assert est_ligne_configuration("accept: F") == True
    assert est_ligne_configuration("I,1") == False
    assert est_ligne_configuration("") == False
    print("  ✓ est_ligne_configuration")


def test_est_ligne_transition_etat():
    """Test de la détection d'une ligne d'état de transition."""
    assert est_ligne_transition_etat("I,1") == True
    assert est_ligne_transition_etat("q0,a") == True
    assert est_ligne_transition_etat("X,R,>") == False  # 2 virgules
    assert est_ligne_transition_etat("init: I") == False  # 0 virgule
    print("  ✓ est_ligne_transition_etat")


def test_parser_ligne_etat():
    """Test du parsing d'une ligne d'état de transition."""
    assert parser_ligne_etat("I,1") == ("I", "1")
    assert parser_ligne_etat("  q0 , a ") == ("q0", "a")
    assert parser_ligne_etat("state_1,_") == ("state_1", "_")
    print("  ✓ parser_ligne_etat")


def test_parser_ligne_action():
    """Test du parsing d'une ligne d'action de transition."""
    assert parser_ligne_action("X,R,>") == ("X", "R", ">")
    assert parser_ligne_action("  q1 , _ , < ") == ("q1", "_", "<")
    assert parser_ligne_action("ACCEPT,a,-") == ("ACCEPT", "a", "-")

    # Test d'erreur : pas assez de virgules
    try:
        parser_ligne_action("X,R")
        assert False, "Devrait lever ValueError"
    except ValueError:
        pass
    print("  ✓ parser_ligne_action")


def test_convertir_mouvement():
    """Test de la conversion des mouvements."""
    assert convertir_mouvement("<") == "L"
    assert convertir_mouvement(">") == "R"
    assert convertir_mouvement("-") == "S"

    try:
        convertir_mouvement("X")
        assert False, "Devrait lever ValueError"
    except ValueError:
        pass
    print("  ✓ convertir_mouvement")


def test_extraire_transitions():
    """Test de l'extraction complète des transitions."""
    lignes = ["init: q0", "accept: F", "q0,0", "q1,1,>", "q0,1", "q0,0,<"]
    transitions, etats, alphabet = extraire_transitions(lignes)

    assert len(transitions) == 2
    assert ("q0", ("0",)) in transitions
    assert ("q0", ("1",)) in transitions
    assert "q0" in etats
    assert "q1" in etats
    assert "0" in alphabet
    assert "1" in alphabet

    # Vérifier la transition q0,0 -> q1,1,>
    t = transitions[("q0", ("0",))]
    assert t.nouvel_etat == "q1"
    assert t.symboles_ecrits == ["1"]
    assert t.mouvements == ["R"]
    print("  ✓ extraire_transitions")


def test_charger_machine_depuis_fichier():
    """Test du chargement complet d'une machine depuis un fichier."""
    contenu = """
init: I
accept: F

I,0
I,1,>

I,1
I,0,>

I,_
F,_,-
"""
    chemin = creer_fichier_tm_temporel(contenu)
    machine = charger_machine_depuis_fichier(chemin)
    os.unlink(chemin)

    assert machine.etat_initial == "I"
    assert machine.etat_final == "F"
    assert machine.nb_rubans == 1
    assert machine.blanc == "_"
    assert len(machine.transitions) == 3
    assert "I" in machine.etats
    assert "F" in machine.etats
    print("  ✓ charger_machine_depuis_fichier")


# ================================
# TESTS Q2 — CONFIGURATION INITIALE
# ================================

def test_configuration_initiale():
    """Test de la création d'une configuration initiale."""
    machine = creer_machine_simple()
    config = configuration_initiale(machine, "aba")

    assert config.etat == "q0"
    assert config.rubans == [["a", "b", "a"]]
    assert config.positions_tetes == [0]
    print("  ✓ configuration_initiale avec mot")


def test_configuration_initiale_vide():
    """Test de la configuration initiale avec mot vide."""
    machine = creer_machine_simple()
    config = configuration_initiale(machine, "")

    assert config.etat == "q0"
    assert config.rubans == [["_"]]
    assert config.positions_tetes == [0]
    print("  ✓ configuration_initiale vide")


# ================================
# TESTS Q3 — PAS DE CALCUL
# ================================

def test_corriger_position_tete_gauche():
    """Test : la tête dépasse à gauche, on ajoute un blanc."""
    ruban = ["1", "0"]
    pos = corriger_position_tete(ruban, -1, "_")
    assert pos == 0
    assert ruban == ["_", "1", "0"]
    print("  ✓ corriger_position_tete (gauche)")


def test_corriger_position_tete_droite():
    """Test : la tête dépasse à droite, on ajoute un blanc."""
    ruban = ["1", "0"]
    pos = corriger_position_tete(ruban, 2, "_")
    assert pos == 2
    assert ruban == ["1", "0", "_"]
    print("  ✓ corriger_position_tete (droite)")


def test_corriger_position_tete_valide():
    """Test : la tête est dans le ruban, pas de changement."""
    ruban = ["1", "0"]
    pos = corriger_position_tete(ruban, 1, "_")
    assert pos == 1
    assert ruban == ["1", "0"]
    print("  ✓ corriger_position_tete (valide)")


def test_chercher_transition():
    """Test de la recherche de transition."""
    machine = creer_machine_simple()

    # Transition existante
    t = chercher_transition(machine, "q0", ["a"])
    assert t is not None
    assert t.nouvel_etat == "qa"

    # Transition inexistante
    t = chercher_transition(machine, "qa", ["_"])
    assert t is not None  # existe
    t = chercher_transition(machine, "q0", ["c"])
    assert t is None
    print("  ✓ chercher_transition")


def test_appliquer_ecriture():
    """Test de l'écriture sur le ruban."""
    machine = creer_machine_simple()
    config = configuration_initiale(machine, "a")

    transition = Transition("qa", ["X"], ["R"])
    appliquer_ecriture(machine, config, transition)

    assert config.rubans[0][0] == "X"
    print("  ✓ appliquer_ecriture")


def test_appliquer_mouvements():
    """Test des déplacements de tête."""
    machine = creer_machine_simple()
    config = configuration_initiale(machine, "abc")

    # Droite
    transition = Transition("q", ["a"], ["R"])
    appliquer_mouvements(machine, config, transition)
    assert config.positions_tetes == [1]

    # Gauche
    transition = Transition("q", ["b"], ["L"])
    appliquer_mouvements(machine, config, transition)
    assert config.positions_tetes == [0]

    # Sur place
    transition = Transition("q", ["a"], ["S"])
    appliquer_mouvements(machine, config, transition)
    assert config.positions_tetes == [0]
    print("  ✓ appliquer_mouvements")


def test_faire_un_pas():
    """Test d'un pas de calcul complet."""
    machine = creer_machine_simple()
    config = configuration_initiale(machine, "a")

    nouvelle = faire_un_pas(machine, config)
    assert nouvelle is not None
    assert nouvelle.etat == "qa"
    assert nouvelle.rubans[0][0] == "a"
    assert nouvelle.positions_tetes == [1]
    print("  ✓ faire_un_pas")


def test_faire_un_pas_bloque():
    """Test d'un pas de calcul quand aucune transition n'existe."""
    machine = creer_machine_simple()
    config = configuration_initiale(machine, "c")  # 'c' n'a pas de transition

    nouvelle = faire_un_pas(machine, config)
    assert nouvelle is None
    print("  ✓ faire_un_pas (blocage)")


def test_faire_un_pas_etat_final():
    """Test : pas de calcul depuis l'état final."""
    machine = creer_machine_simple()
    config = Configuration(
        etat="ACCEPT",
        rubans=[["_"]],
        positions_tetes=[0]
    )

    nouvelle = faire_un_pas(machine, config)
    assert nouvelle is None
    print("  ✓ faire_un_pas (état final)")

# ================================
# TESTS Q4 — SIMULATION
# ================================

def test_simuler_mot_accepte():
    """Test de la simulation d'un mot accepté (atteint l'état final)."""
    machine = creer_machine_simple()
    config = simuler(machine, "bba", afficher=False)

    assert config is not None, "La simulation a retourné None"
    assert config.etat == "ACCEPT", f"État attendu: ACCEPT, obtenu: {config.etat}"
    print("  ✓ simuler (mot accepté → ACCEPT)")


def test_simuler_mot_bloque():
    """Test de la simulation d'un mot qui bloque (pas d'état final)."""
    machine = creer_machine_simple()
    config = simuler(machine, "abb", afficher=False)

    assert config is not None, "La simulation a retourné None"
    assert config.etat != "ACCEPT", f"Le mot ne devrait pas être accepté, état: {config.etat}"
    print("  ✓ simuler (mot bloqué → état non final)")


def test_simuler_mot_vide():
    """Test de la simulation d'un mot vide (bloque immédiatement)."""
    machine = creer_machine_simple()
    config = simuler(machine, "", afficher=False)

    assert config is not None, "La simulation a retourné None"
    assert config.etat == "q0", f"État attendu: q0, obtenu: {config.etat}"
    assert config.etat != "ACCEPT", "Le mot vide ne devrait pas être accepté"
    assert config.rubans[0] == ["_"], "Le ruban devrait contenir uniquement le blanc"
    print("  ✓ simuler (mot vide → bloqué)")


def test_simuler_flip():
    """Test de la machine flip (inverse 0 et 1)."""
    machine = creer_machine_flip()
    config = simuler(machine, "01", afficher=False)

    assert config is not None, "La simulation a retourné None"
    assert config.etat == "ACCEPT", f"État attendu: ACCEPT, obtenu: {config.etat}"
    assert config.rubans[0][:2] == ["1", "0"], (
        f"0→1 et 1→0 attendu, obtenu: {config.rubans[0][:2]}"
    )
    print("  ✓ simuler (flip 01 → 10)")


def test_est_simulation_terminee():
    """Test de la condition d'arrêt."""
    machine = creer_machine_simple()

    config = Configuration("q0", [["a"]], [0])
    assert est_simulation_terminee(config, machine) == False

    config = Configuration("ACCEPT", [["a"]], [0])
    assert est_simulation_terminee(config, machine) == True
    print("  ✓ est_simulation_terminee")

# ================================
# TESTS Q5 — AFFICHAGE
# ================================

def test_formater_ruban():
    """Test du formatage du ruban."""
    assert formater_ruban(["1", "0", "_"]) == "1 0 _"
    assert formater_ruban(["a"]) == "a"
    assert formater_ruban([]) == ""
    print("  ✓ formater_ruban")


def test_formater_position_tete():
    """Test du formatage de la position de la tête."""
    assert formater_position_tete(0) == "^"
    assert formater_position_tete(1) == "   ^"
    assert formater_position_tete(2) == "      ^"
    print("  ✓ formater_position_tete")


# ================================
# TESTS STRUCTURES (Q1)
# ================================

def test_transition_creation():
    """Test de la création d'une Transition."""
    t = Transition("q1", ["a", "b"], ["L", "R"])
    assert t.nouvel_etat == "q1"
    assert t.symboles_ecrits == ["a", "b"]
    assert t.mouvements == ["L", "R"]
    print("  ✓ Transition")


def test_mt_creation():
    """Test de la création d'une MT."""
    machine = MT(
        etats=["q0", "q1"],
        alphabet_entree=["0", "1"],
        alphabet_ruban=["0", "1", "_"],
        blanc="_",
        etat_initial="q0",
        etat_final="q1",
        nb_rubans=2,
        transitions={}
    )
    assert machine.etats == ["q0", "q1"]
    assert machine.nb_rubans == 2
    assert machine.blanc == "_"
    print("  ✓ MT")


def test_configuration_creation():
    """Test de la création d'une Configuration."""
    config = Configuration(
        etat="q0",
        rubans=[["a", "b"], ["c"]],
        positions_tetes=[1, 0]
    )
    assert config.etat == "q0"
    assert config.rubans == [["a", "b"], ["c"]]
    assert config.positions_tetes == [1, 0]
    print("  ✓ Configuration")


# ================================
# LANCEUR
# ================================

def run_all_tests():
    """Lance tous les tests et affiche un résumé."""
    print("\n" + "=" * 55)
    print("  TESTS UNITAIRES — MACHINE DE TURING")
    print("=" * 55 + "\n")

    tests = [
        # Structures (Q1)
        ("Q1 — Structures", [
            test_transition_creation,
            test_mt_creation,
            test_configuration_creation,
        ]),
        # Parsing (Q1 & Q2)
        ("Q2 — Parsing", [
            test_filtrer_lignes_utiles,
            test_extraire_etat_initial,
            test_extraire_etat_final,
            test_est_ligne_configuration,
            test_est_ligne_transition_etat,
            test_parser_ligne_etat,
            test_parser_ligne_action,
            test_convertir_mouvement,
            test_extraire_transitions,
            test_charger_machine_depuis_fichier,
        ]),
        # Configuration initiale (Q2)
        ("Q2 — Configuration initiale", [
            test_configuration_initiale,
            test_configuration_initiale_vide,
        ]),
        # Pas de calcul (Q3)
        ("Q3 — Pas de calcul", [
            test_corriger_position_tete_gauche,
            test_corriger_position_tete_droite,
            test_corriger_position_tete_valide,
            test_chercher_transition,
            test_appliquer_ecriture,
            test_appliquer_mouvements,
            test_faire_un_pas,
            test_faire_un_pas_bloque,
            test_faire_un_pas_etat_final,
        ]),
                # Simulation (Q4)
        ("Q4 — Simulation", [
            test_simuler_mot_accepte,
            test_simuler_mot_bloque,
            test_simuler_mot_vide,
            test_simuler_flip,
        ]),
        # Affichage (Q5)
        ("Q5 — Affichage", [
            test_formater_ruban,
            test_formater_position_tete,
        ]),
    ]

    total = 0
    reussis = 0

    for section, fonctions in tests:
        print(f"[{section}]")
        for fonction in fonctions:
            try:
                fonction()
                reussis += 1
            except AssertionError as e:
                print(f"  ✗ {fonction.__name__} ÉCHEC : {e}")
            except Exception as e:
                print(f"  ✗ {fonction.__name__} ERREUR : {e}")
            total += 1
        print()

    print("=" * 55)
    print(f"  RÉSULTAT : {reussis}/{total} tests réussis")
    if reussis == total:
        print("  ✅ TOUS LES TESTS PASSENT !")
    else:
        print(f"  ⚠️  {total - reussis} test(s) en échec")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    run_all_tests()