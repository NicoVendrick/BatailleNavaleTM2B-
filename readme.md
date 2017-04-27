Bon c'est pas très avancé et un peu instable.. pour l'instant le serveur permet à 2 joueurs de jouer successivement,
et à un 3ème client d'assister au jeu en tant que spectateur 
-> Le jeu démarre automatiquement dès que 2 clients sont connectés 
(j'ai pas encore touché à ça donc pour l'instant il faut que ce soit Thread-1 et Thread-2)
-> Quand le 3ème joueur se connecte, il est spectateur et reçoit automatiquement les coups/grilles des 2 joueurs
(pareil j'ai gardé la contrainte des noms pour l'instant.. le 3ème client doit être Thread-3) 
