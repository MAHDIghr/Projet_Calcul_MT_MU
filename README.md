#  Machine de Turing & Machine Universelle

Ce projet implémente plusieurs exercices autour des machines de Turing et d’une machine universelle, avec différents tests unitaires et fonctionnels.

---

##  Structure du projet

- `main.py` : point d’entrée principal
- `machine_de_turing/` : implémentation de la machine de Turing + tests unitaires
- `machine_universelle/` : implémentation de la machine universelle + tests unitaires
- `Makefile` : automatisation des tests

---

##  Prérequis

- Python 3.x installé
- `make` (uniquement sous Linux / macOS)

Vérifier Python :
```bash
python3 --version



▶️ Tous les tests unitaires

make unit_tests

▶️ Tous les tests fonctionnels

make tests

▶️ Tout (unitaires + fonctionnels)

make all


📌 Tests par question

Chaque commande exécute une question spécifique :

make test_q1
make test_q2
make test_q3
make test_q4
make test_q5
make test_q6
make test_q7
make test_q8
make test_q9
make test_q10


🪟 Utilisation sous Windows (sans make)

Windows ne dispose pas de make par défaut.
Voici les commandes équivalentes à exécuter dans un terminal PowerShell ou Invite de commandes.
▶️ Tests unitaires
powershell

python machine_de_turing/test_machine_de_turing.py
python machine_universelle/test_machine_universille.py

▶️ Tests fonctionnels (tous les exercices)
powershell

python main.py all

▶️ Tests par question

Chaque commande exécute une question spécifique :
powershell

python main.py q1
python main.py q2
python main.py q3
python main.py q4
python main.py q5
python main.py q6
python main.py q7
python main.py q8
python main.py q9
python main.py q10