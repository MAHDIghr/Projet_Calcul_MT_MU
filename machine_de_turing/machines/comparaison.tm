init: I
accept: F

// Avancer jusqu'au #
I,0
I,0,>

I,1
I,1,>

I,#
check,#,>

// Lire x (après #)
check,0
found_0,#,<

check,1
found_1,#,<

check,_
F,_,-       // x fini avant y → x < y → accepter

// Revenir au # après avoir trouvé 0 dans x
found_0,_
found_0,_,<

found_0,0
found_0,0,<

found_0,1
found_0,1,<

found_0,#
go_y_0,#,>

// Revenir au # après avoir trouvé 1 dans x
found_1,_
found_1,_,<

found_1,0
found_1,0,<

found_1,1
found_1,1,<

found_1,#
go_y_1,#,>

// Aller à y après #
go_y_0,0
go_y_0,0,>

go_y_0,1
go_y_0,1,>

go_y_0,_
go_y_0,_,>

// Lire y pour x=0
go_y_0,0
equal,0,<      // 0=0 → continuer

go_y_0,1
accept,1,<     // 0<1 → x<y → accepter

go_y_0,_
loop,_,-       // y fini mais pas x → x>y → boucler

// Aller à y après #
go_y_1,0
go_y_1,0,>

go_y_1,1
go_y_1,1,>

go_y_1,_
go_y_1,_,>

// Lire y pour x=1
go_y_1,0
loop,0,-       // 1>0 → x>y → boucler

go_y_1,1
equal,1,<      // 1=1 → continuer

go_y_1,_
loop,_,-       // y fini → x>y → boucler

// Continuer la comparaison
equal,_
equal,_,<

equal,0
equal,0,<

equal,1
equal,1,<

equal,#
check,#,>      // Revenir à l'état check

// Accepter (x < y)
accept,_
F,_,-

accept,0
F,0,-

accept,1
F,1,-

// Boucle infinie (x >= y)
loop,_
loop,_,-

loop,0
loop,0,-

loop,1
loop,1,-