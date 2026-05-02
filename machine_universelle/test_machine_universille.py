# test_machine_universelle.py

import sys
import os

chemin_racine = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if chemin_racine not in sys.path:
    sys.path.insert(0, chemin_racine)

from machine_universelle.machine_universelle import *
from machine_de_turing.machine_de_turing import filtrer_lignes_utiles

# Chemin vers une machine de test
TEST_MACHINE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "machine_de_turing",
    "machines",
    "test1.tm"
)

def test_extraire_transitions():
    lignes = filtrer_lignes_utiles(TEST_MACHINE)
    transitions = extraire_transitions(lignes)

    assert isinstance(transitions, list)
    assert len(transitions) > 0

    t = transitions[0]
    assert len(t) == 5  # (etat, lu, q', ecrit, mouv)
    print("  ✓ test_extraire_transitions réussi")


def test_encoder_transition():
    t = ("I", "1", "X", "1", ">")
    code = encoder_transition(t)

    assert code == "I|1|X|1|>"
    print("  ✓ test_encoder_transition réussi")


def test_encoder_machine_symbolique():
    code = encoder_machine_symbolique(TEST_MACHINE)

    assert isinstance(code, str)
    assert "|" in code
    assert len(code) > 0
    print("  ✓ test_encoder_machine_symbolique réussi")


def test_caractere_vers_binaire():
    b = caractere_vers_binaire("A")

    assert isinstance(b, str)
    assert len(b) == 8
    assert b == "01000001"
    print("  ✓ test_caractere_vers_binaire réussi")


def test_encoder_en_binaire():
    binaire = encoder_en_binaire("AB")

    assert len(binaire) == 16  # 2 caractères * 8 bits
    print("  ✓ test_encoder_en_binaire réussi")


def test_encoder_machine_binaire():
    binaire = encoder_machine_binaire(TEST_MACHINE)

    assert isinstance(binaire, str)
    assert set(binaire).issubset({"0", "1"})
    assert len(binaire) > 0
    print("  ✓ test_encoder_machine_binaire réussi")


def test_binaire_vers_entier():
    entier = binaire_vers_entier("01000001")

    assert entier == 65
    print("  ✓ test_binaire_vers_entier réussi")


def test_machine_universelle_simulation():
    config = machine_universelle_simulation(TEST_MACHINE, "111")

    assert config is not None
    assert hasattr(config, "etat")
    print("  ✓ test_machine_universelle_simulation réussi")


def test_machine_universelle_avec_compteur():
    config, steps = machine_universelle_avec_compteur(
        TEST_MACHINE,
        "111",
        10
    )

    assert config is not None
    assert isinstance(steps, int)
    assert steps <= 10
    print("  ✓ test_machine_universelle_avec_compteur réussi")


# ============================
# LANCEMENT GLOBAL
# ============================

def run_all_tests():
    print("\n" + "=" * 50)
    print("LANCEMENT DES TESTS")
    print("=" * 50 + "\n")

    test_extraire_transitions()
    test_encoder_transition()
    test_encoder_machine_symbolique()
    test_caractere_vers_binaire()
    test_encoder_en_binaire()
    test_encoder_machine_binaire()
    test_binaire_vers_entier()
    test_machine_universelle_simulation()
    test_machine_universelle_avec_compteur()

    print("\n" + "=" * 50)
    print("✅ Tous les tests sont passés avec succès !")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    run_all_tests()