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
    binaire_vers_chaine,
    machine_universelle_simulation,
    machine_universelle_avec_compteur,
)

# =========================
# Q1 — Structures
# =========================

def test_q1():
    print("\n" + "=" * 60)
    print("  Q1 — STRUCTURES DE DONNÉES")
    print("=" * 60 + "\n")
    print("Les classes définies dans mt_structures.py :\n")
    print("  • MT          : représente une machine de Turing")
    print("                  (états, alphabets, transitions, ruban...)")
    print("  • Configuration : représente l'état instantané")
    print("                  (état courant, contenu ruban, position tête)")
    print("  • Transition  : représente une règle de transition")
    print("                  (nouvel état, symbole écrit, mouvement)")
    print("\n Structures définies et opérationnelles")

# =========================
# Q2 — Chargement + config initiale
# =========================

def test_q2():
    print("\n" + "=" * 60)
    print("  Q2 — CHARGEMENT MACHINE + CONFIGURATION INITIALE")
    print("=" * 60 + "\n")

    machine = charger_machine_comparaison()
    mot = "10#100"

    print(f"Machine chargée : comparaison.tm")
    print(f"État initial    : {machine.etat_initial}")
    print(f"État final      : {machine.etat_final}")
    print(f"Nb transitions  : {len(machine.transitions)}")
    print(f"\nMot d'entrée    : {mot}")
    print("\nConfiguration initiale :")
    config = configuration_initiale(machine, mot)
    afficher_configuration(config)
# =========================
# Q3 — Un pas
# =========================

def test_q3():
    print("\n" + "=" * 60)
    print("  Q3 — UN PAS DE CALCUL")
    print("=" * 60 + "\n")

    machine = charger_machine_comparaison()
    mot = "10#100"
    config = configuration_initiale(machine, mot)

    print(f"  Mot d'entrée : {mot}\n")
    print("  Avant le pas :")
    afficher_configuration(config)

    config = faire_un_pas(machine, config)

    print("  Après 1 pas :")
    if config:
        afficher_configuration(config)
    else:
        print("  Machine bloquée ou état final atteint")


# =========================
# Q4 — Simulation complète
# =========================

def test_q4():
    print("\n" + "=" * 60)
    print("  Q4 — SIMULATION COMPLÈTE")
    print("=" * 60 + "\n")

    machine = charger_machine_comparaison()
    mot = "10#100"

    print(f"  Mot d'entrée : {mot}  (2 < 4 en décimal)")
    print(f"  Résultat attendu : x < y → machine s'arrête (état F)\n")

    config = simuler(machine, mot, afficher=False)

    if config.etat == machine.etat_final:
        print(f"  ✅ État final atteint : {config.etat} → x < y confirmé")
    else:
        print(f"  ❌ État final non atteint : {config.etat}")

# =========================
# Q5 — Affichage
# =========================

def test_q5():
    print("\n" + "=" * 60)
    print("  Q5 — AFFICHAGE DES CONFIGURATIONS")
    print("=" * 60 + "\n")

    machine = charger_machine_comparaison()
    mot = "10#100"

    print(f"  Simulation pas à pas de : {mot}\n")
    simuler(machine, mot, afficher=True)

# =========================
# Q6 — Machines exemples
# =========================

def test_q6():
    print("\n" + "=" * 60)
    print("  Q6 — MACHINES DE TURING")
    print("=" * 60 + "\n")

    # Comparaison
    print("[Comparaison] 10 < 100 ? (2 < 4 en décimal)")
    m = charger_machine_comparaison()
    config = simuler(m, "10#100", afficher=False)
    print(" x < y → ARRÊT" if config.etat == m.etat_final else " x >= y → BOUCLE")

    # Recherche
    print("\n[Recherche] '10' dans ['01', '10', '11'] ?")
    m = charger_machine_recherche()
    config = simuler(m, "10#01#10#11", afficher=False)
    print(" Mot trouvé → ARRÊT" if config.etat == m.etat_final else " Mot non trouvé → BOUCLE")

    # Multiplication unaire
    print("\n[Multiplication unaire] 2 x 3 = ?")
    m = charger_machine_multiplication_unaire()
    config = simuler(m, "11#111", afficher=False)
    ruban = "".join(config.rubans[0])
    resultat = ruban.split("#")[-1].count("1")
    print(f" Résultat : {resultat} uns" if resultat == 6 else f" Résultat incorrect : {resultat} uns")


# =========================
# Q7 — Codage symbolique
# =========================

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
# Q9 — MACHINE UNIVERSELLE
# =========================

def test_q9():
    """
    Question 9 : Machine de Turing universelle à 3 rubans.
    Lit un fichier contenant <M>#x en binaire et simule M sur x.
    """
    print("\n" + "=" * 60)
    print("  Q9 — MACHINE UNIVERSELLE À 3 RUBANS")
    print("=" * 60 + "\n")
    
    # ------------------------------------------------------------
    # 1. Lire le fichier binaire
    # ------------------------------------------------------------
    chemin_fichier = "machines/machine_test_q9.tm"
    
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        entree_binaire = f.read().strip()
    
    print(f" Fichier lu : {chemin_fichier}")
    print(f" Entrée binaire ({len(entree_binaire)} bits)")
    print(f"   {entree_binaire[:80]}...\n")
    
    # 2. Décoder le binaire → chaîne symbolique
    chaine = binaire_vers_chaine(entree_binaire)
    code_M, x = chaine.split("#", 1)
    
    print(f" Code symbolique <M> : {code_M}")
    print(f" Mot d'entrée x      : {x}\n")
    
    # 3. Simulation avec la machine universelle
    print("=" * 60)
    print("  SIMULATION")
    print("=" * 60 + "\n")
    
    config_finale = machine_universelle_simulation(entree_binaire, afficher=True)
    
    resultat = "".join(config_finale.rubans[1]).replace("_", "")
    
    print("=" * 60)
    print("  RÉSULTAT")
    print("=" * 60)
    print(f"  Mot x avant  : {x}")
    print(f"  Mot x après  : {resultat}")
    print("=" * 60 + "\n")

# =========================
# Q10 — Machine universelle limitée
# =========================

def test_q10():
    """
    Question 9 : Machine de Turing universelle à 3 rubans.
    Lit un fichier contenant <M>#x en binaire et simule M sur x.
    """
    print("\n" + "=" * 60)
    print("  Q9 — MACHINE UNIVERSELLE AVEC COMPTEUR")
    print("=" * 60 + "\n")
    
    # ------------------------------------------------------------
    # 1. Lire le fichier binaire
    # ------------------------------------------------------------
    chemin_fichier = "machines/machine_test_q10.tm"
    
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        entree_binaire = f.read().strip()
    
    print(f" Fichier lu : {chemin_fichier}")
    print(f" Entrée binaire ({len(entree_binaire)} bits)")
    print(f"   {entree_binaire[:80]}...\n")
    
    # 2. Décoder le binaire → chaîne symbolique
    chaine = binaire_vers_chaine(entree_binaire)
    code_M, x, n = chaine.split("#", 2)
    
    print(f" Code symbolique <M> : {code_M}")
    print(f" Mot d'entrée x      : {x}\n")
    print(f" Nombre d'étapes n      : {n}\n")
    
    # 3. Simulation avec la machine universelle
    print("=" * 60)
    print("  SIMULATION")
    print("=" * 60 + "\n")
    
    config_finale, steps, limite = machine_universelle_avec_compteur(entree_binaire, afficher=True)
    
    resultat = "".join(config_finale.rubans[1]).replace("_", "")
    
    print("=" * 60)
    print("  RÉSULTAT")
    print("=" * 60)
    print(f"    Étapes exécutées : {steps}")
    print(f"    Limite dépassée ? : {'Oui' if limite else 'Non'}")
    print(f"  Mot x avant  : {x}")
    print(f"  Mot x après  : {resultat}")
    print("=" * 60 + "\n")

def test_q11():
    """
    Question 11 : Décidabilité de L1, L2, L3.
    """
    print("\n" + "=" * 60)
    print("  Q11 — DÉCIDABILITÉ DE L1, L2, L3")
    print("=" * 60 + "\n")
    
    # Machine flip utilisée pour les tests
    code_M = "0|_|_|-|1|0|0|1|>|0|0|1|0|>|0"
    
    # ============================================================
    # L1 : DÉCIDABLE 
    # ============================================================
    print("=" * 60)
    print("  L1 = {<M>#n | M s'arrête sur n en moins de n étapes}")
    print("=" * 60 + "\n")
    
    print(" Test avec M = flip, n = 10 (entrée simulée : 10)")
    print("   La machine flip traite 2 caractères, donc 3 étapes suffisent.\n")
    
    # Utilisation de machine_universelle_avec_compteur (Q10)
    entree1 = code_M + "#10#10"
    entree_bin1 = "".join(format(ord(c), "08b") for c in entree1)
    
    config1, steps1, limite1 = machine_universelle_avec_compteur(entree_bin1, afficher=False)
    
    if not limite1:
        print(f"    M s'est arrêtée en {steps1} étapes (< 10)")
        print(f"   → Le mot <M>#10 est DANS L1\n")
    else:
        print(f"    M ne s'est pas arrêtée en 10 étapes")
        print(f"   → Le mot <M>#10 n'est PAS dans L1\n")
    
    print(" Test avec M = flip, n = 1 (entrée simulée : 111)")
    print("   La machine a besoin d'au moins 4 étapes pour 3 caractères.\n")
    
    entree2 = code_M + "#111#1"
    entree_bin2 = "".join(format(ord(c), "08b") for c in entree2)
    
    config2, steps2, limite2 = machine_universelle_avec_compteur(entree_bin2, afficher=False)
    
    if not limite2:
        print(f"    M s'est arrêtée en {steps2} étapes (< 1)")
    else:
        print(f"   M ne s'est pas arrêtée en 1 étape (limite atteinte)")
        print(f"   → Le mot <M>#1 n'est PAS dans L1\n")
    
    print(" Conclusion : L1 est DÉCIDABLE")
    print("   Preuve : machine_universelle_avec_compteur(Q10) est un décideur.")
    print("   Elle simule n étapes maximum et répond toujours OUI/NON.\n")
    
    # ============================================================
    # L2 : INDÉCIDABLE — illustration de la réduction
    # ============================================================
    print("=" * 60)
    print("  L2 = {<M>#n | M s'arrête sur tous les mots de taille n}")
    print("=" * 60 + "\n")
    
    print(" Tentative de test pour n=1 :")
    print("   Il faudrait tester M sur '0' et '1' (2 mots de taille 1)")
    print("   Si M boucle sur l'un d'eux → impossible à détecter !\n")
    
    print(" Preuve d'indécidabilité (réduction de HALT) :")
    print("   Si L2 était décidable, on pourrait résoudre HALT :")
    print("   1. Pour savoir si M s'arrête sur x :")
    print("   2. Construire M' qui ignore son entrée et simule M sur x")
    print("   3. M' s'arrête sur les mots de taille 0 ⇔ M s'arrête sur x")
    print("   4. Or HALT est indécidable → contradiction")
    print("   → L2 est INDÉCIDABLE\n")
    
    # ============================================================
    # L3 : INDÉCIDABLE — illustration de la réduction
    # ============================================================
    print("=" * 60)
    print("  L3 = {<M>#x#y | M calcule la même chose sur x et y}")
    print("=" * 60 + "\n")
    
    print(" Exemple avec M = flip :")
    print("   x = '01' → M(x) = '10'")
    print("   y = '10' → M(y) = '01'")
    print("   M(x) ≠ M(y) → le mot n'est PAS dans L3\n")
    
    print(" Preuve d'indécidabilité (théorème de Rice) :")
    print("   « M calcule la même chose sur x et y » est une propriété")
    print("   sémantique (comportementale) non triviale de M.")
    print("   Le théorème de Rice (cours p.26) dit que toute propriété")
    print("   non triviale du langage d'une MT est indécidable.")
    print("   → L3 est INDÉCIDABLE\n")
    
    # Résumé
    print("=" * 60)
    print("  RÉSUMÉ")
    print("=" * 60)
    print("  L1 : DÉCIDABLE   → machine_universelle_avec_compteur() le prouve")
    print("  L2 : INDÉCIDABLE → réduction de HALT")
    print("  L3 : INDÉCIDABLE → théorème de Rice")
    print("=" * 60 + "\n")


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
    test_q11()


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
        "q11": test_q11,
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