
Il faut d'abord démarrer le serveur en éxecutant serveur.py. Ensuite on peut lancer autant de clients que l'on souhaite, en executant client.py avec en paramètre le nom de l'hôte (entre guillemets... ex: 'localhost').  

Les 2 premiers connectés seront les joueurs, les suivant seront spectateurs. Chaque joueur joue tour à tour, en fin de partie les joueurs ont la possibilité de rejouer : à la réception du message "play again? YES OR NO" si les 2 joueurs répondent "yes", une nouvelle partie se lance et les scores sont alors comptabilisés.

Si un joueur répond "no" il est automatiquement déconnecté. 
En revanche si un joueur répond "yes" et l'autre "no", s'il y a des spectateurs en ligne, ils se verront proposer de jouer à la place du joueur qui se désiste. 

En cas de déconnexion forcée d'un joueur (ctrl-c..), le jeu est mis en pause 30 secondes, si le joueur se reconnecte dans ce délai, la partie reprend (après les 30 secondes d'attente) sinon la partie s'arrête.

Les joueurs ont la possibilité d'abandonner à tout moment la partie en cours en inscrivant "fin" dans un input. Là encore, les joueurs auront la possibilité de rejouer, si c'est le cas, 1 point sera donné à l'adversaire.


