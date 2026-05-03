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
    """Crée une machine simple qui accepte les mots finissant par '1'."""
    contenu = """// Machine de test : accepte les mots finissant par '1'
init: I
accept: F

I,0
I,0,>

I,1
I,1,>

I,_
verif,_,<

verif,1
F,1,-
"""
    chemin = creer_fichier_tm_temporel(contenu)
    machine = charger_machine_depuis_fichier(chemin)
    os.unlink(chemin)
    return machine


def creer_machine_flip():
    """Crée une machine qui inverse 0 et 1."""
    contenu = """// Machine flip : 0->1, 1->0
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
    return machine


# ================================
# TESTS Q1 & Q2 — PARSING
# ================================

def test_filtrer_lignes_utiles():
    """Test du filtrage des lignes : suppression commentaires et lignes vides."""
    contenu = "// commentaire\n\ninit: I\n# autre commentaire\n\nI,1\nF,1,>\n"
    chemin = creer_fichier_tm_temporel(contenu)

    lignes = filtrer_lignes_utiles(chemin)
    os.unlink(chemin)

    assert lignes == ["init: I", "I,1", "F,1,>"], f"Lignes obtenues : {lignes}"
    print("  ✓ filtrer_lignes_utiles")


def test_extraire_etat_initial():
    """Test de l'extraction de l'état initial."""
    assert extraire_etat_initial(["init: I", "accept: F"]) == "I"
    assert extraire_etat_initial(["accept: F"]) is None
    assert extraire_etat_initial(["init:   I  "]) == "I"
    print("  ✓ extraire_etat_initial")


def test_extraire_etat_final():
    """Test de l'extraction de l'état final."""
    assert extraire_etat_final(["init: I", "accept: F"]) == "F"
    assert extraire_etat_final(["init: I"]) is None
    assert extraire_etat_final(["accept:   F  "]) == "F"
    print("  ✓ extraire_etat_final")


def test_est_ligne_configuration():
    """Test de la détection des lignes de configuration."""
    assert est_ligne_configuration("init: I") == True
    assert est_ligne_configuration("accept: F") == True
    assert est_ligne_configuration("I,1") == False
    assert est_ligne_configuration("") == False
    print("  ✓ est_ligne_configuration")


def test_est_ligne_transition_etat():
    """Test de la détection d'une ligne d'état de transition."""
    assert est_ligne_transition_etat("I,1") == True
    assert est_ligne_transition_etat("I,0") == True
    assert est_ligne_transition_etat("F,1,>") == False  # 2 virgules
    assert est_ligne_transition_etat("init: I") == False  # 0 virgule
    print("  ✓ est_ligne_transition_etat")


def test_parser_ligne_etat():
    """Test du parsing d'une ligne d'état de transition."""
    assert parser_ligne_etat("I,1") == ("I", "1")
    assert parser_ligne_etat("  I , 0 ") == ("I", "0")
    assert parser_ligne_etat("state_1,_") == ("state_1", "_")
    print("  ✓ parser_ligne_etat")


def test_parser_ligne_action():
    """Test du parsing d'une ligne d'action de transition."""
    assert parser_ligne_action("F,1,>") == ("F", "1", ">")
    assert parser_ligne_action("  I , _ , < ") == ("I", "_", "<")
    assert parser_ligne_action("F,0,-") == ("F", "0", "-")

    # Test d'erreur : pas assez de virgules
    try:
        parser_ligne_action("F,1")
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
        convertir_mouvement("Z")
        assert False, "Devrait lever ValueError"
    except ValueError:
        pass
    print("  ✓ convertir_mouvement")


def test_extraire_transitions():
    """Test de l'extraction complète des transitions."""
    lignes = ["init: I", "accept: F", "I,0", "F,1,>", "I,1", "I,0,<"]
    transitions, etats, alphabet = extraire_transitions(lignes)

    assert len(transitions) == 2
    assert ("I", ("0",)) in transitions
    assert ("I", ("1",)) in transitions
    assert "I" in etats
    assert "F" in etats
    assert "0" in alphabet
    assert "1" in alphabet

    # Vérifier la transition I,0 -> F,1,>
    t = transitions[("I", ("0",))]
    assert t.nouvel_etat == "F"
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
    config = configuration_initiale(machine, "101")

    assert config.etat == "I"
    assert config.rubans == [["1", "0", "1"]]
    assert config.positions_tetes == [0]
    print("  ✓ configuration_initiale avec mot")


def test_configuration_initiale_vide():
    """Test de la configuration initiale avec mot vide."""
    machine = creer_machine_simple()
    config = configuration_initiale(machine, "")

    assert config.etat == "I"
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

    # Transition existante : I lit 0
    t = chercher_transition(machine, "I", ["0"])
    assert t is not None
    assert t.nouvel_etat == "I"

    # Transition inexistante : I lit #
    t = chercher_transition(machine, "I", ["#"])
    assert t is None
    print("  ✓ chercher_transition")


def test_appliquer_ecriture():
    """Test de l'écriture sur le ruban."""
    machine = creer_machine_simple()
    config = configuration_initiale(machine, "1")

    transition = Transition("I", ["0"], ["R"])
    appliquer_ecriture(machine, config, transition)

    assert config.rubans[0][0] == "0"
    print("  ✓ appliquer_ecriture")


def test_appliquer_mouvements():
    """Test des déplacements de tête."""
    machine = creer_machine_simple()
    config = configuration_initiale(machine, "101")

    # Droite
    transition = Transition("I", ["1"], ["R"])
    appliquer_mouvements(machine, config, transition)
    assert config.positions_tetes == [1]

    # Gauche
    transition = Transition("I", ["0"], ["L"])
    appliquer_mouvements(machine, config, transition)
    assert config.positions_tetes == [0]

    # Sur place
    transition = Transition("I", ["1"], ["S"])
    appliquer_mouvements(machine, config, transition)
    assert config.positions_tetes == [0]
    print("  ✓ appliquer_mouvements")


def test_faire_un_pas():
    """Test d'un pas de calcul complet."""
    machine = creer_machine_simple()
    config = configuration_initiale(machine, "1")

    nouvelle = faire_un_pas(machine, config)
    assert nouvelle is not None
    assert nouvelle.etat == "I"
    assert nouvelle.rubans[0][0] == "1"
    assert nouvelle.positions_tetes == [1]
    print("  ✓ faire_un_pas")


def test_faire_un_pas_bloque():
    """Test d'un pas de calcul quand aucune transition n'existe."""
    machine = creer_machine_simple()
    config = configuration_initiale(machine, "#")  # '#' n'a pas de transition depuis I

    nouvelle = faire_un_pas(machine, config)
    assert nouvelle is None
    print("  ✓ faire_un_pas (blocage)")


def test_faire_un_pas_etat_final():
    """Test : pas de calcul depuis l'état final."""
    machine = creer_machine_simple()
    config = Configuration(
        etat="F",
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
    config = simuler(machine, "001", afficher=False)

    assert config is not None, "La simulation a retourné None"
    assert config.etat == "F", f"État attendu: F, obtenu: {config.etat}"
    print("  ✓ simuler (mot accepté → F)")


def test_simuler_mot_bloque():
    """Test de la simulation d'un mot qui bloque (pas d'état final)."""
    machine = creer_machine_simple()
    config = simuler(machine, "010", afficher=False)

    assert config is not None, "La simulation a retourné None"
    assert config.etat != "F", f"Le mot ne devrait pas être accepté, état: {config.etat}"
    print("  ✓ simuler (mot bloqué → état non final)")


def test_simuler_mot_vide():
    """Test de la simulation d'un mot vide (bloque après une étape)."""
    machine = creer_machine_simple()
    config = simuler(machine, "", afficher=False)

    assert config is not None, "La simulation a retourné None"
    assert config.etat == "verif", f"État attendu: verif, obtenu: {config.etat}"
    assert config.etat != "F", "Le mot vide ne devrait pas être accepté"
    assert config.rubans[0][0] == "_", "Le ruban devrait contenir le blanc"
    print("  ✓ simuler (mot vide → bloqué)")


def test_simuler_flip():
    """Test de la machine flip (inverse 0 et 1)."""
    machine = creer_machine_flip()
    config = simuler(machine, "01", afficher=False)

    assert config is not None, "La simulation a retourné None"
    assert config.etat == "F", f"État attendu: F, obtenu: {config.etat}"
    assert config.rubans[0][:2] == ["1", "0"], (
        f"0->1 et 1->0 attendu, obtenu: {config.rubans[0][:2]}"
    )
    print("  ✓ simuler (flip 01 → 10)")


def test_est_simulation_terminee():
    """Test de la condition d'arrêt."""
    machine = creer_machine_simple()

    config = Configuration("I", [["1"]], [0])
    assert est_simulation_terminee(config, machine) == False

    config = Configuration("F", [["1"]], [0])
    assert est_simulation_terminee(config, machine) == True
    print("  ✓ est_simulation_terminee")


# ================================
# TESTS Q5 — AFFICHAGE
# ================================

def test_formater_ruban():
    """Test du formatage du ruban."""
    assert formater_ruban(["1", "0", "_"]) == "1 0 _"
    assert formater_ruban(["1"]) == "1"
    assert formater_ruban([]) == ""
    print("  ✓ formater_ruban")


def test_formater_position_tete():
    """Test du formatage de la position de la tête."""
    # Test 1 : position 0 sur un ruban de 3 éléments
    ruban = ["1", "0", "_"]
    resultat = formater_position_tete(ruban, 0)
    assert resultat == " ^", f"Position 0 échouée : '{resultat}'"
    
    # Test 2 : position 1
    ruban = ["1", "0", "_"]
    resultat = formater_position_tete(ruban, 1)
    assert resultat == "   ^", f"Position 1 échouée : '{resultat}'"
    
    # Test 3 : position 2
    ruban = ["1", "0", "_"]
    resultat = formater_position_tete(ruban, 2)
    assert resultat == "     ^", f"Position 2 échouée : '{resultat}'"
    
    # Test 4 : ruban à un seul élément
    ruban = ["_"]
    resultat = formater_position_tete(ruban, 0)
    assert resultat == " ^", f"Ruban seul échoué : '{resultat}'"
    
    # Test 5 : ruban vide 
    ruban = []
    resultat = formater_position_tete(ruban, 0)
    assert resultat == " ^", f"Ruban vide échoué : '{resultat}'"
    
    print("  ✓ formater_position_tete")

# ================================
# TESTS STRUCTURES (Q1)
# ================================

def test_transition_creation():
    """Test de la création d'une Transition."""
    t = Transition("F", ["0", "1"], ["L", "R"])
    assert t.nouvel_etat == "F"
    assert t.symboles_ecrits == ["0", "1"]
    assert t.mouvements == ["L", "R"]
    print("  ✓ Transition")


def test_mt_creation():
    """Test de la création d'une MT."""
    machine = MT(
        etats=["I", "F"],
        alphabet_entree=["0", "1"],
        alphabet_ruban=["0", "1", "_"],
        blanc="_",
        etat_initial="I",
        etat_final="F",
        nb_rubans=1,
        transitions={}
    )
    assert machine.etats == ["I", "F"]
    assert machine.nb_rubans == 1
    assert machine.blanc == "_"
    print("  ✓ MT")


def test_configuration_creation():
    """Test de la création d'une Configuration."""
    config = Configuration(
        etat="I",
        rubans=[["0", "1"], ["1"]],
        positions_tetes=[1, 0]
    )
    assert config.etat == "I"
    assert config.rubans == [["0", "1"], ["1"]]
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
            test_est_simulation_terminee,
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
