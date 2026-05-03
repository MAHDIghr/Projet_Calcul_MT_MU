init: I
accept: F

// Marquer le début du mot x (remplacer premier bit par X ou Y)
I,0
mark_0,X,>

I,1
mark_1,Y,>

// Chercher le # après x
mark_0,0
mark_0,0,>

mark_0,1
mark_0,1,>

mark_0,#
go_start,#,<

mark_1,0
mark_1,0,>

mark_1,1
mark_1,1,>

mark_1,#
go_start,#,<

// Revenir au début du ruban
go_start,_
go_start,_,<

go_start,0
go_start,0,<

go_start,1
go_start,1,<

go_start,X
compare,X,>

go_start,Y
compare,Y,>

// Comparer le bit courant de x avec le mot
compare,X
check_w,0,>    // On attend 0

compare,Y
check_w,1,>    // On attend 1

check_w,0
match,_,>      // OK : 0=0

check_w,1
next_word,_,>  // KO : on attend 0, on a 1

// Avancer jusqu'au prochain # ou _
match,_
match,_,>

match,0
match,0,>

match,1
match,1,>

match,X
compare,X,>    // Continuer avec le prochain bit de x

match,Y
compare,Y,>    // Continuer avec le prochain bit de x

match,#
found,#,<      // x et le mot ont la même longueur

// Mot trouvé → accepter
found,_
F,_,-

found,X
F,_,-

found,Y
F,_,-

// Passer au mot suivant
next_word,_
next_word,_,>

next_word,0
next_word,0,>

next_word,1
next_word,1,>

next_word,#
next_word,#,>

next_word,X
go_start,_,<   // Recommencer depuis le début

next_word,Y
go_start,_,<   // Recommencer depuis le début

// Fin de liste : mot non trouvé → boucler
go_start,_
loop,_,-       // Rien trouvé → boucle infinie

// Boucle infinie
loop,_
loop,_,-

loop,0
loop,0,-

loop,1
loop,1,-

loop,#
loop,#,-

loop,X
loop,X,-

loop,Y
loop,Y,-