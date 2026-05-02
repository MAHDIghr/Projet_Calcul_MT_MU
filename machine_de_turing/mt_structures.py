# fichier: mt_structures.py

class Transition:
    """
    Représente une transition de la machine de Turing.
    Pour un état courant et des symboles lus, on sait :
    - dans quel nouvel état aller,
    - quels symboles écrire,
    - comment bouger les têtes.
    """
    def __init__(self, nouvel_etat, symboles_ecrits, mouvements):
        self.nouvel_etat = nouvel_etat              # str
        self.symboles_ecrits = symboles_ecrits      # liste de str, taille = nb de rubans
        self.mouvements = mouvements                # liste de 'L', 'R' ou 'S'


class MT:
    """
    Représente une machine de Turing.
    """
    def __init__(self, etats, alphabet_entree, alphabet_ruban,
                 blanc, etat_initial, etat_final, nb_rubans, transitions):
        self.etats = etats                          # liste de str
        self.alphabet_entree = alphabet_entree      # liste de str
        self.alphabet_ruban = alphabet_ruban        # liste de str
        self.blanc = blanc                          # str
        self.etat_initial = etat_initial            # str
        self.etat_final = etat_final                # str
        self.nb_rubans = nb_rubans                  # int

        # transitions est un dictionnaire :
        # clé   = (etat_courant, (symbole_lu_ruban1, ..., symbole_lu_rubank))
        # valeur = objet Transition
        self.transitions = transitions               # dict


class Configuration:
    """
    Représente une configuration de la machine :
    - état courant
    - contenu des rubans
    - positions des têtes
    """
    def __init__(self, etat, rubans, positions_tetes):
        self.etat = etat                    # str
        self.rubans = rubans                # liste de listes de str
        self.positions_tetes = positions_tetes  # liste d'int
