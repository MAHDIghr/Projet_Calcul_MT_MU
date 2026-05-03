init: I
accept: F

// Étape 1 : Compter les 1 de n (remplacer par X)
I,1
I,X,>

I,#
zero_n,#,>

// Continuer à compter n
I,X
I,X,>

// Arrivé au #, passer à y
I,#
setup,#,>

// n=0 → résultat = 0
zero_n,1
zero_n,1,>

zero_n,_
F,_,-

// Aller à la fin de y, puis copier n
setup,1
setup,1,>

setup,_
rewind,_,<

// Revenir au début pour copier
rewind,1
rewind,1,<

rewind,#
rewind,#,<

rewind,X
copy_one,X,>

rewind,_
copy_one,_,>

// Copier un bloc de n
copy_one,X
copy_one,1,>

copy_one,1
copy_one,1,>

copy_one,#
copy_one,#,>

copy_one,_
dec_m,_,<

// Décrémenter m (remplacer 1 par _)
dec_m,1
go_back,_,<

dec_m,_
cleanup,_,<

// Revenir au début
go_back,_
go_back,_,<

go_back,1
go_back,1,<

go_back,#
go_back,#,<

go_back,X
copy_one,X,>

go_back,1
go_back,1,<

// Nettoyage final
cleanup,_
cleanup,_,<

cleanup,1
cleanup,1,<

cleanup,#
cleanup,#,<

cleanup,X
cleanup,1,<

cleanup,_
F,_,>