// Recherche dans une liste
// Entrée : x#w1#w2#...#wl
// S'arrête (F) si x = wi pour un i, boucle sinon
// Principe : on compare x avec chaque wi bit à bit
// On marque les bits comparés avec _ et on recommence pour chaque wi

init: I
accept: F

// --- Phase 1 : lire un bit de x ---
I,0
lux0,_,>

I,1
lux1,_,>

// x épuisé → vérifier si le wi courant est aussi épuisé
I,#
verifx,#,>

// --- Traverser x jusqu'au premier # ---
lux0,0
lux0,0,>

lux0,1
lux0,1,>

lux0,#
cy0,#,>

lux1,0
lux1,0,>

lux1,1
lux1,1,>

lux1,#
cy1,#,>

// --- Sauter les wi déjà comparés (marqués _) ---
cy0,_
cy0,_,>

cy1,_
cy1,_,>

// --- Comparer bit de x avec bit de wi ---
// On avait lu 0 dans x
cy0,0
retour,_,<

cy0,1
suivant,1,<

cy0,#
suivant,#,<

cy0,_
LOOP,_,-

// On avait lu 1 dans x
cy1,0
suivant,0,<

cy1,1
retour,_,<

cy1,#
suivant,#,<

cy1,_
LOOP,_,-

// --- x épuisé : vérifier que wi est aussi épuisé ---
verifx,_
F,_,-

verifx,0
suivant,0,<

verifx,1
suivant,1,<

verifx,#
F,#,-

// --- Retour au début de x ---
retour,0
retour,0,<

retour,1
retour,1,<

retour,#
retour,#,<

retour,_
I,_,>

// --- Passer au wi suivant ---
// On avance jusqu'au prochain # puis on repart
suivant,0
suivant,0,>

suivant,1
suivant,1,>

suivant,#
reset,#,>

suivant,_
LOOP,_,-

// --- Remettre x à zéro pour comparer avec wi+1 ---
// On revient au début et on relit x depuis le début
reset,0
reset,0,>

reset,1
reset,1,>

reset,#
reset,#,>

reset,_
rebob,_,<

// Reculer jusqu'au début
rebob,0
rebob,0,<

rebob,1
rebob,1,<

rebob,#
rebob,#,<

rebob,_
I,_,>

// --- Boucle infinie ---
LOOP,0
LOOP,0,>

LOOP,1
LOOP,1,>

LOOP,#
LOOP,#,>

LOOP,_
LOOP,_,>
