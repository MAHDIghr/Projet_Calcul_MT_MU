# test_machine_universelle.py
#
# Fichier de tests unitaires pour la machine universelle.
# Couvre les questions Q7 à Q10 du projet.


import sys
import os
import tempfile

chemin_racine = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if chemin_racine not in sys.path:
    sys.path.insert(0, chemin_racine)

from machine_universelle.machine_universelle import *
from machine_de_turing.mt_structures import MT, Configuration
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
# TESTS Q7 — CODAGE SYMBOLIQUE
# ================================

# -------------------------------
# TEST : extraire_transitions
# -------------------------------

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

# -------------------------------
# TEST : encoder_transition
# -------------------------------

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

# -------------------------------
# TEST : encoder_machine_symbolique
# -------------------------------

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

# ================================
# TESTS Q8 — CODAGE BINAIRE
# ================================

# -------------------------------
# TEST : caractere_vers_binaire
# -------------------------------

def test_caractere_vers_binaire():
    b = caractere_vers_binaire("A")

    assert isinstance(b, str)
    assert len(b) == 8
    assert b == "01000001"
    print("  ✓ test_caractere_vers_binaire réussi")

# -------------------------------
# TEST : encoder_en_binaire
# -------------------------------

def test_encoder_en_binaire():
    binaire = encoder_en_binaire("AB")

    assert len(binaire) == 16  # 2 caractères * 8 bits
    print("  ✓ test_encoder_en_binaire réussi")

# -------------------------------
# TEST : encoder_machine_binaire
# -------------------------------

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

# -------------------------------
# TEST : binaire_vers_entier
# -------------------------------

def test_binaire_vers_entier():
    entier = binaire_vers_entier("01000001")

    assert entier == 65
    print("  ✓ test_binaire_vers_entier réussi")

# -------------------------------
# TEST : binaire_vers_chaine
# -------------------------------

def test_binaire_vers_chaine():
    texte = "AB"

    binaire = "".join(format(ord(c), "08b") for c in texte)

    resultat = binaire_vers_chaine(binaire)

    assert resultat == "AB", f"Erreur décodage : {resultat}"

    print("  ✓ test_binaire_vers_chaine réussi")

# ================================
# TESTS Q9 — MACHINE UNIVERSELLE
# ================================

# -------------------------------
# TEST : lire_symbole
# -------------------------------

def test_lire_symbole():

    ruban = list("01")

    symbole, pos = lire_symbole(ruban, 0)

    assert symbole == "0"
    assert pos == 0

    # test dépassement droite
    symbole, pos = lire_symbole(ruban, 5)

    assert symbole == "_"
    assert ruban[-1] == "_"

    print("  ✓ test_lire_symbole réussi")

# -------------------------------
# TEST : chercher_transition
# -------------------------------

def test_chercher_transition():
    # Format de encoder_transition : q|s|s'|D|q'
    # Donc "0|0|1|>|1" signifie :
    #   état=0, lit=0, écrit=1, direction=>, nouvel_état=1
    code_M = "0|0|1|>|1|0|1|0|>|0|"
    
    # Chercher transition (état=0, symbole=0)
    t = chercher_transition(code_M, "0", "0")
    
    # Doit retourner (nouvel_état=1, symbole_écrit=1, direction=>)
    assert t == ("1", "1", ">"), (
        f"Transition incorrecte :\n"
        f"  obtenu  : {t}\n"
        f"  attendu : ('1', '1', '>')"
    )
    
    # Chercher transition inexistante
    t2 = chercher_transition(code_M, "9", "0")
    assert t2 is None
    
    print("  ✓ test_chercher_transition réussi")

# -------------------------------
# TEST : faire_un_pas_UTM
# -------------------------------

def test_faire_un_pas_UTM():

    machine = MT(
        etats=["RUN", "1"],
        alphabet_entree=[],
        alphabet_ruban=["0", "1", "_"],
        blanc="_",
        etat_initial="RUN",
        etat_final="1",
        nb_rubans=3,
        transitions={}
    )

    config = Configuration(
        etat="0",
        rubans=[
            list("0|0|1|1|>|"),
            list("0"),
            ["0"]
        ],
        positions_tetes=[0, 0, 0]
    )

    resultat = faire_un_pas_UTM(machine, config, "0|0|1|1|>|")

    assert resultat is not None
    assert resultat.rubans[1][0] in ["0", "1"]

    print("  ✓ test_faire_un_pas_UTM réussi")

# -------------------------------
# TEST : machine_universelle_simple
# -------------------------------

def test_machine_universelle_simple():

    # machine flip simplifiée (0->1, 1->0)
    code_M = "0|_|_|-|1|0|0|1|>|0|0|1|0|>|0"
    x = "01"

    entree = code_M + "#" + x

    entree_binaire = "".join(format(ord(c), "08b") for c in entree)

    config = machine_universelle_simulation(entree_binaire, afficher=False)

    assert config is not None
    assert len(config.rubans) == 3

    resultat = "".join(config.rubans[1]).replace("_", "")

    attendu = "10"

    assert resultat == attendu, (
        f"Erreur UTM :\n"
        f"  obtenu  : {resultat}\n"
        f"  attendu : {attendu}"
    )

    print("  ✓ test_machine_universelle_simple réussi")

# ================================
# TESTS Q10 — MACHINE UNIVERSELLE AVEC COMPTEUR
# ================================

# -------------------------------
# TEST : machine_universelle_avec_compteur
# -------------------------------

def test_machine_universelle_avec_compteur():
    """
    Test de machine_universelle_avec_compteur avec 3 cas :
    - n=20 : la machine termine avant la limite
    - n=3  : la machine est interrompue par la limite
    - n=0  : aucune étape exécutée
    """
    
    # Machine flip : 0 -> 1, 1 -> 0, _ -> fin
    code_M = "0|_|_|-|1|0|0|1|>|0|0|1|0|>|0"
    x = "1001110"
    
    # ------------------------------------------------------------
    # TEST 1 : n=20 -> la machine doit terminer avant la limite
    # ------------------------------------------------------------
    entree = code_M + "#" + x + "#20"
    entree_binaire = "".join(format(ord(c), "08b") for c in entree)
    
    config, steps, limite = machine_universelle_avec_compteur(entree_binaire, afficher=False)
    
    resultat = "".join(config.rubans[1]).replace("_", "")
    
    # Vérifications
    assert steps == 8, (
        f"Test 1 (n=20) : nombre d'étapes incorrect\n"
        f"  obtenu  : {steps}\n"
        f"  attendu : 8"
    )
    assert limite == False, (
        f"Test 1 (n=20) : la machine ne devrait pas dépasser la limite\n"
        f"  limite atteinte : {limite}"
    )
    assert resultat == "0110001", (
        f"Test 1 (n=20) : résultat incorrect\n"
        f"  obtenu  : {resultat}\n"
        f"  attendu : 0110001"
    )
    print("  ✓ Test 1 (n=20) : machine terminée avant limite")
    
    # ----------------------------------------------------------
    # TEST 2 : n=3 -> la machine doit être interrompue
    # ------------------------------------------------------------
    entree = code_M + "#" + x + "#3"
    entree_binaire = "".join(format(ord(c), "08b") for c in entree)
    
    config, steps, limite = machine_universelle_avec_compteur(entree_binaire, afficher=False)
    
    resultat = "".join(config.rubans[1]).replace("_", "")
    
    # Vérifications
    assert steps == 3, (
        f"Test 2 (n=3) : nombre d'étapes incorrect\n"
        f"  obtenu  : {steps}\n"
        f"  attendu : 3"
    )
    assert limite == True, (
        f"Test 2 (n=3) : la limite devrait être atteinte\n"
        f"  limite atteinte : {limite}"
    )
    assert resultat == "0111110", (
        f"Test 2 (n=3) : résultat partiel incorrect\n"
        f"  obtenu  : {resultat}\n"
        f"  attendu : 0111110"
    )
    print("  ✓ Test 2 (n=3) : machine interrompue par la limite")
    
    # ------------------------------------------------------------
    # TEST 3 : n=0 -> aucune étape exécutée
    # ------------------------------------------------------------
    entree = code_M + "#" + x + "#0"
    entree_binaire = "".join(format(ord(c), "08b") for c in entree)
    
    config, steps, limite = machine_universelle_avec_compteur(entree_binaire, afficher=False)
    
    resultat = "".join(config.rubans[1]).replace("_", "")
    
    # Vérifications
    assert steps == 0, (
        f"Test 3 (n=0) : nombre d'étapes incorrect\n"
        f"  obtenu  : {steps}\n"
        f"  attendu : 0"
    )
    assert limite == True, (
        f"Test 3 (n=0) : la limite devrait être atteinte\n"
        f"  limite atteinte : {limite}"
    )
    assert resultat == x, (
        f"Test 3 (n=0) : le mot ne devrait pas changer\n"
        f"  obtenu  : {resultat}\n"
        f"  attendu : {x}"
    )
    print("  ✓ Test 3 (n=0) : aucune étape exécutée")
    
    print("  ✓ test_machine_universelle_avec_compteur réussi")

# ============================
# LANCEMENT GLOBAL
# ============================

def run_all_tests():
    print("\n" + "=" * 50)
    print("LANCEMENT DES TESTS — MACHINE UNIVERSELLE")
    print("=" * 50 + "\n")

    tests = [
        # Q7 — Codage symbolique
        test_extraire_transitions,
        test_encoder_transition,
        test_encoder_machine_symbolique,
        # Q8 — Codage binaire
        test_caractere_vers_binaire,
        test_encoder_en_binaire,
        test_encoder_machine_binaire,
        test_binaire_vers_entier,
        test_binaire_vers_chaine,
        # Q9 — Machine universelle
        test_lire_symbole,
        test_chercher_transition,
        test_faire_un_pas_UTM,
        test_machine_universelle_simple,
        # Q10 — Machine universelle avec compteur
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