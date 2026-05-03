// Machine flip : transforme 0 en 1 et 1 en 0
init: 0
accept: 1

// Si on lit □, on a fini → accepter
0,_
1,_,-

// Si on lit 0, on écrit 1 et on avance
0,0
0,1,>

// Si on lit 1, on écrit 0 et on avance
0,1
0,0,>