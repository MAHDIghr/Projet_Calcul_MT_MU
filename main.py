# main.py

import sys
import os

from machine_de_turing.machine_de_turing import (
    charger_machine_depuis_fichier,
    configuration_initiale,
    faire_un_pas,
    simuler,
    afficher_configuration,
    charger_machine_comparaison,
    charger_machine_recherche,
    charger_machine_multiplication_unaire,
)

from machine_universelle.machine_universelle import (
    encoder_machine_symbolique,
    encoder_machine_binaire,
    binaire_vers_entier,
    machine_universelle_simulation,
    machine_universelle_avec_compteur,
)

# =========================
# Q1 — Structures
# =========================

def test_q1():
    print("\n=== Q1 : Structures ===")
    print("Les classes MT, Configuration et Transition sont définies dans mt_structures.py")


# =========================
# Q2 — Chargement + config initiale
# =========================

def test_q2():
    print("\n=== Q2 : Chargement machine ===")
    machine = charger_machine_comparaison()
    config = configuration_initiale(machine, "10#100")
    afficher_configuration(config)


# =========================
# Q3 — Un pas
# =========================

def test_q3():
    print("\n=== Q3 : Un pas ===")
    machine = charger_machine_comparaison()
    config = configuration_initiale(machine, "10#100")

    print("Avant :")
    afficher_configuration(config)

    config = faire_un_pas(machine, config)

    print("Après 1 pas :")
    if config:
        afficher_configuration(config)


# =========================
# Q4 — Simulation complète
# =========================

def test_q4():
    print("\n=== Q4 : Simulation ===")
    machine = charger_machine_comparaison()
    simuler(machine, "10#100", afficher=True)


# =========================
# Q5 — Affichage
# =========================

def test_q5():
    print("\n=== Q5 : Affichage ===")
    machine = charger_machine_comparaison()
    simuler(machine, "10#100", afficher=True)


# =========================
# Q6 — Machines exemples
# =========================

def test_q6():
    print("\n=== Q6 : Machines ===")

    # Comparaison
    print("\n[Comparaison]")
    m = charger_machine_comparaison()
    simuler(m, "10#100", afficher=True)

    # Recherche
    print("\n[Recherche]")
    m = charger_machine_recherche()
    simuler(m, "10#01#10#11", afficher=True)

    # Multiplication unaire
    print("\n[Multiplication unaire]")
    m = charger_machine_multiplication_unaire()
    config = simuler(m, "11#111", afficher=True)
    print("Résultat :", "".join(config.rubans[0]).replace("_", ""))


# =========================
# Q7 — Codage symbolique
# =========================

def test_q7():
    print("\n=== Q7 : Codage symbolique ===")
    chemin = "machines/comparaison.tm"
    code = encoder_machine_symbolique(chemin)
    print(code)

def test_q7():
    """Q7 : Codage symbolique <M>."""
    print("\n" + "=" * 60)
    print("  Q7 — CODAGE SYMBOLIQUE <M>")
    print("=" * 60 + "\n")

    chemin = "machines/machine_test_q7.tm"

    print(" Machine : transforme 0 en 1 et 1 en 0 (flip)")
    print(f"   Fichier : machines/machine_test_q7.tm\n")

    # Encodage symbolique
    code = encoder_machine_symbolique(chemin)

    # Code attendu selon le sujet
    attendu = "0|_|_|-|1|0|0|1|>|0|0|1|0|>|0"

    print("Code attendu :")
    print(f"  {attendu}\n")

    print("Code obtenu :")
    print(f"  {code}\n")

    # Comparaison
    if code == attendu:
        print(" Le code obtenu correspond au code attendu !\n")
    else:
        print(" Le code obtenu ne correspond PAS au code attendu.\n")

    # Réponse à la question : accepter n'importe quel alphabet de travail
    print("=" * 60)
    print("Question : Que faudrait-il faire si on veut pouvoir")
    print("           accepter n'importe quel alphabet de travail ?")
    print("=" * 60)
    print("""
    Réponse : Il faudrait étendre l'alphabet de codage. Actuellement,
    on utilise les caractères ASCII pour coder les symboles. Pour
    accepter n'importe quel alphabet de travail, il faut :

    1. Choisir un caractère d'échappement (ex: \\) pour encoder des
       symboles qui ne sont pas dans l'alphabet de codage.

    2. Ou bien utiliser un codage universel comme l'Unicode (UTF-8)
       pour représenter tous les symboles possibles.
    """)
    print("=" * 60)


# =========================
# Q8 — Codage binaire
# =========================

def test_q8():
    print("\n" + "=" * 60)
    print("  Q8 — CODAGE BINAIRE")
    print("=" * 60 + "\n")

    print("Choix du codage binaire :")
    print("  Chaque caractère du codage symbolique <M> est converti")
    print("  en sa représentation ASCII sur 8 bits (1 octet).")
    print("  Cela permet de représenter tout symbole de l'alphabet")
    print("  de travail {0, 1, #, |, _} (□ représenté par _).\n")
    
    chemin = "machines/machine_test_q8.tm"

    code_sym = encoder_machine_symbolique(chemin)
    code_bin = encoder_machine_binaire(chemin)
    entier = binaire_vers_entier(code_bin)

    print("Symbolique :", code_sym)
    print("Binaire ",len(code_bin), " Bits \n\nAffichage des 100 premiers bits : \n", code_bin[:100], "...")  # éviter affichage énorme
    print("\nInterprétation en tant qu'entier :\n", entier)
    print("Cet entier peut être vu comme le numéro unique de la machine")
    print("=" * 60)

# =========================
# Q9 — Machine universelle
# =========================

def test_q9():
    print("\n=== Q9 : Machine universelle ===")
    chemin = "machine_de_turing/machines/comparaison.tm"
    machine_universelle_simulation(chemin, "10#100", afficher=True)


# =========================
# Q10 — Machine universelle limitée
# =========================

def test_q10():
    print("\n=== Q10 : Machine universelle avec limite ===")
    chemin = "machine_de_turing/machines/comparaison.tm"

    config, steps = machine_universelle_avec_compteur(
        chemin, "10#100", 10, afficher=True
    )

    print("Steps exécutés :", steps)


# =========================
# ALL
# =========================

def run_all():
    test_q1()
    test_q2()
    test_q3()
    test_q4()
    test_q5()
    test_q6()
    test_q7()
    test_q8()
    test_q9()
    test_q10()


# =========================
# MAIN CLI
# =========================

if __name__ == "__main__":
    actions = {
        "q1": test_q1,
        "q2": test_q2,
        "q3": test_q3,
        "q4": test_q4,
        "q5": test_q5,
        "q6": test_q6,
        "q7": test_q7,
        "q8": test_q8,
        "q9": test_q9,
        "q10": test_q10,
        "all": run_all,
    }

    if len(sys.argv) < 2:
        print("Usage: python main.py [q1|q2|...|q10|all]")
        sys.exit(1)

    arg = sys.argv[1]

    if arg not in actions:
        print("Argument invalide")
        sys.exit(1)

    actions[arg]()