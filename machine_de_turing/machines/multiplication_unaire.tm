// Multiplication en unaire
// Entree : 1^n # 1^m
// On insere un # separateur pour obtenir : 1^n # 1^m # 1^(n*m)
// Pour chaque 1 de n, on copie m uns apres le second #

init: I
accept: F

// Etape 0 : inserer le second # a la fin du ruban
// On avance jusqu'a la fin et on place #
I,1
e0,1,>

e0,1
e0,1,>

e0,#
e1,#,>

e1,1
e1,1,>

e1,_
e2,#,<

// Revenir au debut
e2,1
e2,1,<

e2,#
e2,#,<

e2,_
debut,_,>

// Ruban : 1^n # 1^m # _
// debut : lire un 1 de n
debut,1
an,_,>

// n fini
debut,#
F,#,-

// Avancer jusqu'au premier #
an,1
an,1,>

an,_
an,_,>

an,#
am,#,>

// Lire un 1 de m, le marquer |
// Sauter les | deja marques
am,|
am,|,>

am,1
af,|,>

// m fini : on est au second #
am,#
rs,#,<

// Aller apres le second # pour ecrire 1
af,1
af,1,>

af,|
af,|,>

af,#
af2,#,>

// Ecrire 1 a la fin du resultat
af2,1
af2,1,>

af2,_
aw,1,<

// Revenir au second # 
aw,1
aw,1,<

aw,#
aw2,#,<

// Revenir au | qu'on vient de poser dans m
aw2,1
aw2,1,<

aw2,|
am,1,>

// Restaurer les | en 1 et revenir au debut
rs,|
rs,1,<

rs,1
rs,1,<

rs,#
rs,#,<

rs,_
debut,_,>
