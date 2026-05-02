from chargeur import charger_machine_depuis_fichier, configuration_initiale
from simulateur import simuler

# 1. Charger la machine depuis le fichier
machine = charger_machine_depuis_fichier("machines/hash_to_x_clean.tm")
print("TRANSITIONS CHARGÉES :")
for cle, t in machine.transitions.items():
    print(cle, "→", t.nouvel_etat, t.symboles_ecrits, t.mouvements)


# 2. Mot d'entrée
mot = "111#111"

# 3. Simuler avec affichage
resultat = simuler(machine, mot, afficher=True)

# 4. Afficher le résultat final
print("Résultat final :", "".join(resultat.rubans[0]))
