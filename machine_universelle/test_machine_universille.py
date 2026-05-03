# test_machine_universelle.py

import sys
import os
import tempfile

# Ajouter la racine du projet au path
chemin_racine = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if chemin_racine not in sys.path:
    sys.path.insert(0, chemin_racine)

from machine_universelle.machine_universelle import *
from machine_de_turing.machine_de_turing import filtrer_lignes_utiles

# ================================
# FIXTURE — MACHINE TEMPORAIRE
# ================================

def creer_fichier_tm_temporel(contenu):
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".tm", delete=False, encoding="utf-8"
    )
    tmp.write(contenu)
    tmp.close()
    return tmp.name


def creer_machine_test():
    """
    Machine flip au format du sujet :
    - état initial = 0
    - état final = 1
    - blanc = _
    """
    contenu = """// Machine flip : transforme 0 en 1 et 1 en 0
init: 0
accept: 1

// Si on lit _, on a fini → accepter
0,_
1,_,-

// Si on lit 0, on écrit 1 et on avance
0,0
0,1,>

// Si on lit 1, on écrit 0 et on avance
0,1
0,0,>
"""
    chemin = creer_fichier_tm_temporel(contenu)
    return chemin

# ================================
# TESTS
# ================================

def test_extraire_transitions():
    chemin = creer_machine_test()

    lignes = filtrer_lignes_utiles(chemin)
    transitions = extraire_transitions(lignes)

    os.unlink(chemin)

    assert isinstance(transitions, list)
    assert len(transitions) > 0

    t = transitions[0]
    assert len(t) == 5  # (etat, lu, q', ecrit, mouv)
    print("  ✓ test_extraire_transitions réussi")


def test_encoder_transition():
    # t = (etat, lu, nouvel_etat, ecrit, mouv)
    t = ("I", "1", "X", "1", ">")
    code = encoder_transition(t)

    # Format : q | s_lu | s_ecrit | direction | q'
    assert code == "I|1|1|>|X", (
        f"Code incorrect :\n"
        f"  obtenu : {code}\n"
        f"  attendu : I|1|1|>|X"
    )
    print("  ✓ test_encoder_transition réussi")

def test_encoder_machine_symbolique():
    chemin = creer_machine_test()

    code = encoder_machine_symbolique(chemin)

    os.unlink(chemin)

    assert isinstance(code, str)
    assert "|" in code
    assert len(code) > 0
    
    # Vérifier le code exact (format avec I et F)
    attendu = "0|_|_|-|1|0|0|1|>|0|0|1|0|>|0"
    assert code == attendu, f"Code incorrect :\n  obtenu : {code}\n  attendu : {attendu}"
    
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
    chemin = creer_machine_test()
    binaire = encoder_machine_binaire(chemin)
    os.unlink(chemin)

    assert isinstance(binaire, str)
    assert set(binaire).issubset({"0", "1"})
    assert len(binaire) > 0

    attendu = (
    "0011000001111100010111110111110001011111011111000010110101111100"
    "0011000101111100001100000111110000110000011111000011000101111100"
    "0011111001111100001100000111110000110000011111000011000101111100"
    "0011000001111100001111100111110000110000"
    )

    assert binaire == attendu, (
        f"Code binaire incorrect :\n"
        f"  longueur obtenu : {len(binaire)} bits\n"
        f"  longueur attendu : {len(attendu)} bits"
    )
    print("  ✓ test_encoder_machine_binaire réussi")


def test_binaire_vers_entier():
    entier = binaire_vers_entier("01000001")

    assert entier == 65
    print("  ✓ test_binaire_vers_entier réussi")


def test_machine_universelle_simulation():
    chemin = creer_machine_test()

    config = machine_universelle_simulation(chemin, "111")

    os.unlink(chemin)

    assert config is not None
    assert hasattr(config, "etat")
    print("  ✓ test_machine_universelle_simulation réussi")


def test_machine_universelle_avec_compteur():
    chemin = creer_machine_test()

    config, steps = machine_universelle_avec_compteur(
        chemin,
        "111",
        10
    )

    os.unlink(chemin)

    assert config is not None
    assert isinstance(steps, int)
    assert steps <= 10
    print("  ✓ test_machine_universelle_avec_compteur réussi")


# ============================
# LANCEMENT GLOBAL
# ============================

def run_all_tests():
    print("\n" + "=" * 50)
    print("LANCEMENT DES TESTS — MACHINE UNIVERSELLE")
    print("=" * 50 + "\n")

    tests = [
        test_extraire_transitions,
        test_encoder_transition,
        test_encoder_machine_symbolique,
        test_caractere_vers_binaire,
        test_encoder_en_binaire,
        test_encoder_machine_binaire,
        test_binaire_vers_entier,
        test_machine_universelle_simulation,
        test_machine_universelle_avec_compteur,
    ]

    total = 0
    reussis = 0

    for test in tests:
        try:
            test()
            reussis += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} ÉCHEC : {e}")
        total += 1

    print("\n" + "=" * 50)
    print(f"RÉSULTAT : {reussis}/{total} tests réussis")
    if reussis == total:
        print("✅ TOUS LES TESTS PASSENT !")
    else:
        print(f"⚠️ {total - reussis} test(s) en échec")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    run_all_tests()