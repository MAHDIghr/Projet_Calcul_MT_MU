// Comparaison x#y en binaire
// S'arrête (F) si x < y, boucle sinon
// On efface x bit par bit, on saute les bits de y sans les effacer
// On utilise | pour marquer jusqu'où on est allé dans y

init: I
accept: F

// Lire le prochain bit de x
I,0
lu0,_,>

I,1
lu1,_,>

// x épuisé → regarder si y a encore des bits
I,#
finx,#,>

// Traverser jusqu'au #
lu0,0
lu0,0,>

lu0,1
lu0,1,>

lu0,_
lu0,_,>

lu0,#
cy0,#,>

lu1,0
lu1,0,>

lu1,1
lu1,1,>

lu1,_
lu1,_,>

lu1,#
cy1,#,>

// Sauter les | déjà marqués dans y
cy0,|
cy0,|,>

cy1,|
cy1,|,>

// Comparer : on avait lu 0 dans x
cy0,0
retour,|,<

cy0,1
F,|,-

cy0,_
LOOP,_,-

// Comparer : on avait lu 1 dans x
cy1,0
LOOP,|,-

cy1,1
retour,|,<

cy1,_
LOOP,_,-

// Retour au début
retour,|
retour,|,<

retour,0
retour,0,<

retour,1
retour,1,<

retour,#
retour,#,<

retour,_
I,_,>

// x fini : si y a encore des bits → x < y
finx,|
finx,|,>

finx,0
F,0,-

finx,1
F,1,-

finx,_
LOOP,_,-

// Boucle infinie
LOOP,0
LOOP,0,>

LOOP,1
LOOP,1,>

LOOP,#
LOOP,#,>

LOOP,|
LOOP,|,>

LOOP,_
LOOP,_,>
