#!/usr/bin/env python
# -*- coding:utf-8 -*-


# Définition d'un serveur réseau gérant un système de CHAT simplifié.
# Utilise les threads pour gérer les connexions clientes en parallèle.

HOST = 'localhost'
PORT = 40000

import socket, sys, threading
from game import *
import  random
import time

#j'ai mis ton abandon dans une fonction 
def GiveUp(name):
    if name=="Thread-1":
        index=1
        other="Thread-2"
    if name=="Thread-2":
        other="Thread-1"
        index=0
    print "Client %s déconnecté"%name
    over=1
    score[index]+=1
    conn_client[other].send('print("You win! The other player gives up!")\n')
    conn_client[name].send('print("You loose by giving up!")\n')
    return over



#teste si name est dans le dico conn_client
def isInConn_client(name):
    b=False
    for client in conn_client.keys():
        if client == name :
            b=True
    return b

#diffuse le msg à tous les spectateurs 
def broadcastSpectateurs(msg):
    if len(spectateurs) >= 1:
        for name in spectateurs.keys():
            try :                 #le try permet d'éviter les erreurs et de supprimer le spectateur du dico lorsque il s'est déconnecté 
                spectateurs[name].send(msg)
            except socket.error:
                print "Le spectateur %s n'est plus là"%name
                del spectateurs[name]

""" generate a random valid configuration """
def randomConfiguration():
    boats = [];
    while not isValidConfiguration(boats):
        boats=[]
        for i in range(5):
            x = random.randint(1,10)
            y = random.randint(1,10)
            isHorizontal = random.randint(0,1) == 0
            boats = boats + [Boat(x,y,LENGTHS_REQUIRED[i],isHorizontal)]
    return boats
   

def displayConfiguration(player, boats, shots=[], showBoats=True):  
    Matrix = [[" " for x in range(WIDTH+1)] for y in range(WIDTH+1)]
    for i  in range(1,WIDTH+1):
        Matrix[i][0] = chr(ord("A")+i-1)
        Matrix[0][i] = i

    if showBoats:
        for i in range(NB_BOATS):
            b = boats[i]
            (w,h) = boat2rec(b)
            for dx in range(w):
                for dy in range(h):
                    Matrix[b.x+dx][b.y+dy] = str(i)

    for (x,y,stike) in shots:
      if (x>0) and (x<11):
        if stike:
            Matrix[x][y] = "X"
        else:
            Matrix[x][y] = "O"
    for y in range(0, WIDTH+1):
        if y == 0:
            l = "  "
        else:
            l = str(y)
            if y < 10:
                l = l + " "
        for x in range(1,WIDTH+1):
            l = l + str(Matrix[x][y]) + " "
        if player==0:
            conn_client["Thread-1"].send('print ("%s")\n' %(l))
            broadcastSpectateurs('print ("%s")\n' %(l))
    	else:
            conn_client["Thread-2"].send('print ("%s")\n' %(l))
            broadcastSpectateurs('print ("%s")\n' %(l))

""" display the game viewer by the player"""
def displayGame(game, player):
    otherPlayer = (player+1)%2
    displayConfiguration(player, game.boats[player], game.shots[otherPlayer], showBoats=True)
    displayConfiguration(player, [], game.shots[player], showBoats=False)

# j'ai décomposé 
#après avoir joué, le joueur voit seulement la grille adverse ( la portée de son coup)
# puis le joueur suivant voit sa grille affectée par le dernier coup, avant de jouer
def displayPlayerShot(game,player):
    displayConfiguration(player, [], game.shots[player], showBoats=False)

def displayPlayerGame(game,player):
    otherPlayer = (player+1)%2
    displayConfiguration(player, game.boats[player], game.shots[otherPlayer], showBoats=True)


""" Play a new random shot """
def randomNewShot(shots):
    (x,y) = (random.randint(1,10), random.randint(1,10))
    while not isANewShot(x,y,shots):
        (x,y) = (random.randint(1,10), random.randint(1,10))
    return (x,y)


class ThreadClient(threading.Thread):
    '''dérivation d'un objet thread pour gérer la connexion avec un client'''
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn

    def run(self):
         # Dialogue avec le client :
            nom = self.getName()
            over=0
                # Chaque thread possède un nom
            print "len conn client : ", len(conn_client)
            if len(conn_client) >= 2: # dès qu'on a 2 clients, le jeu démarre
                    try :                               #ce try  avec enJeu => permet de déterminer si c'est une nouvelle partie 
                        game=enJeu["game"]

                    except KeyError:
                        boats1 = randomConfiguration()
                        boats2 = randomConfiguration()
                        game = Game(boats1, boats2)
                        enJeu["game"]=game
                        
            	    print ('======================')
            	    
            	    if nom == "Thread-1":
            		    currentPlayer = 0
            		    displayGame(game, currentPlayer)
            		    
            	    if nom== "Thread-2" :
            		    currentPlayer = 1
            		    displayGame(game, currentPlayer)
            	    else :
                        currentPlayer=3
                        
                    if currentPlayer==0 or currentPlayer==1:
            		while gameOver(game) == -1:
            			print ('======================')
            			if currentPlayer == 0:
                                    
                                    try :
            				conn_client["Thread-1"].send('input ("quelle colonne ? ")')
            				msgClient = conn_client["Thread-1"].recv(1024)
                                        if msgClient.upper().find("FIN")!=-1:
                                            over=GiveUp("Thread-1")
                                            break
            				x_char = msgClient.upper()
            				x_char.capitalize()
            				x = ord(x_char)-ord("A")+1
            				conn_client["Thread-1"].send('input ("quelle ligne ? ")')
            				msgClient = conn_client["Thread-1"].recv(1024)
            				if msgClient.upper().find("FIN")!=-1:
                                            over=GiveUp("Thread-1")
                                            break
            				y = int(msgClient)

            			    except socket.error:
                                        del conn_client["Thread-1"]
                                        conn_client["Thread-2"].send("print'JEU EN PAUSE : Adversaire déconnecté'\n")
                                        time.sleep(30) #on laisse 30 secondes à l'adversaire pour se reconnecter.. 
                                        if isInConn_client("Thread-1"):
                                            continue
                                        else :         # sinon on déco l'autre joueur.
                                            conn_client["Thread-2"].send("deconnexion")
                                            del conn_client["Thread-2"]
                                            print " Client Thread-2 deconnecte" 
                                        
            			if currentPlayer == 1 :
                                    
                                    try:
            				conn_client["Thread-2"].send('input ("quelle colonne ? ")')
            				msgClient = conn_client["Thread-2"].recv(1024)
            				if msgClient.upper().find("FIN")!=-1:
                                            over=GiveUp("Thread-2")
                                            break
            				x_char = msgClient.upper()
            				x_char.capitalize()
            				x = ord(x_char)-ord("A")+1
            				conn_client["Thread-2"].send('input ("quelle ligne ? ")')
            				msgClient = conn_client["Thread-2"].recv(1024)
            				if msgClient.upper().find("FIN")!=-1:
                                            over=GiveUp("Thread-2")
                                            break
                                        y = int(msgClient)

                                    except socket.error:
                                        del conn_client["Thread-2"]
                                        conn_client["Thread-1"].send("print'JEU EN PAUSE : Adversaire déconnecté'\n")
                                        time.sleep(30)
                                        if isInConn_client("Thread-2"):
                                            continue
            				else :
                                            conn_client["Thread-1"].send("deconnexion")
                                            del conn_client["Thread-1"]
                                            print " Client Thread-1 deconnecte"
                                            
                                addShot(game, x, y, currentPlayer)
                                broadcastSpectateurs("print'Coup du joueur %s :' \n"%currentPlayer) #à afficher avant les displays pour un peu + de clarté

                                try :
                                    displayPlayerShot(game,currentPlayer)
                                    currentPlayer = (currentPlayer+1)%2
                                    displayPlayerGame(game,currentPlayer)
                                except IndexError:
                                    continue
                                except socket.error:
                                    if currentPlayer==0: 
                                        del conn_client["Thread-1"]
                                        conn_client["Thread-2"].send("print'JEU EN PAUSE : Adversaire déconnecté'\n")
                                        time.sleep(25)
                                        
                                        if isInConn_client("Thread-1"):
                                            displayPlayerShot(game,currentPlayer)
                                            currentPlayer = (currentPlayer+1)%2
                                            displayPlayerGame(game,currentPlayer)
                                            currentPlayer=(currentPlayer+1)%2
                                            continue

                                    if currentPlayer==1:
                                        
                                        del conn_client["Thread-2"]
                                        conn_client["Thread-1"].send("print'JEU EN PAUSE : Adversaire déconnecté'\n")
                                        time.sleep(25)
                                        
                                        if isInConn_client("Thread-2"):
                                            displayPlayerShot(game,currentPlayer)
                                            currentPlayer = (currentPlayer+1)%2
                                            displayPlayerGame(game,currentPlayer)
                                            currentPlayer=(currentPlayer+1)%2
                                            continue


                        del enJeu["game"]# une fois qu'on a game over on supprime cette entrée
                        
                        for client in ["Thread-1","Thread-2"]:
                            try :
                                conn_client[client].send('print("GAME OVER")\n')

                            except KeyError:
                                print "Le client %s est déconnecté!"%client

                        game.shots[0]=[] #fin de partie on remet game.shots "à zero"
            		game.shots[1]=[]    

                        if over==0:
                            if gameOver(game) == 0:
                                score[0]+=1 #mise à jour des scores
            			conn_client["Thread-1"].send('print("You win !")\n')
            			conn_client["Thread-2"].send('print("You loose !")\n')
                            else:
                                score[1]+=1
                                print "OVER:",over# mise à jour des scores
            			conn_client["Thread-2"].send('print("You win !")\n')
            			conn_client["Thread-1"].send('print("You loose !")\n')

                        #envoie les scores
                        print "SCORE : %s - %s "%(score[0],score[1])
                        conn_client["Thread-1"].send("print'SCORE : %s - %s '\n"%(score[0],score[1]))
                        conn_client["Thread-2"].send("print'SCORE : %s - %s '\n"%(score[0],score[1]))

                        #demande s'ils veulent rejouer	
                        conn_client["Thread-1"].send('input("play again ? YES OR NO>>")\n') # 2 'yes' => ça rejoue, 'no'=> deconnexion.
                        conn_client["Thread-2"].send('input("play again ? YES OR NO>>")\n')
                        msgClient = conn_client["Thread-1"].recv(1024)
                        msgClient2 = conn_client["Thread-2"].recv(1024)

                        if msgClient.upper()=='YES' == msgClient2.upper() : # si les 2 joueurs veulent rejouer, ça repart
                            self.run()

                        else : #sinon on demande aux éventuels spectateurs et on remet les scores à 0
                            if msgClient.upper()=='YES':
                                client="Thread-1"
                                other="Thread-2"
                                
                            else :
                                
                                client="Thread-2"
                                other="Thread-1"

                            conn_client[other].send("deconnexion") #on supprime celui qui a dit non !
                            del conn_client[other]
                            print "Client %s déconnecté"%other
                            conn_client[client].send("print'désolé votre adversaire a quitté le jeu..'\n")
                            
                            if len(spectateurs)>=1: # si on a des spectateurs on leur propose de jouer
                                adv=False
                                for spectateur in spectateurs.keys():
                                    spectateurs[spectateur].send('input ("wanna play? yes or no")')
                                    msgSpec=spectateurs[spectateur].recv(1024)
                                    
                                    if msgSpec.upper()=='YES': # si un spectateur est ok on le renomme Thread-1 ou Thread-2 et on relance une partie
                                        adv=True
                                        score[0]=0 
                                        score[1]=0
                                        ThreadClient(spectateurs[spectateur]).setName(other)
                                        conn_client[other]=spectateurs[spectateur]
                                        ThreadClient(spectateurs[spectateur]).run()
                                        del spectateurs[spectateur]
                                        self.run()

                                if adv==False  : # si aucun spectateur n'a voulu joué, on déco 
                                    conn_client[client].send("deconnexion")
                                    del conn_client[client]
                                    print "Client %s déconnecté." %client
                            else :
                                conn_client[client].send("deconnexion")
                                del conn_client[client]

                            score[0]=0 
                            score[1]=0
            else :
                    conn_client[nom].send("print'desole vous etes le seul joueur connecte, En attente dun adversaire...'\n")
            	    #Le premier connecté attend un adversaire, dès qu'un autre client se connecte le jeu démarre et ce dernier commence
   

# Initialisation du serveur - Mise en place du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
try:
    mySocket.bind((HOST, PORT))
    
except socket.error:
    print "La liaison du socket à l'adresse choisie a échoué."
    sys.exit()
    
print "Serveur prêt, en attente de requêtes ..."

mySocket.listen(5)

# Attente et prise en charge des connexions demandées par les clients :

conn_client = {} # dictionnaire des connexions clients

spectateurs={} # dico de spectateurs comme ça il peut y en avoir plusieurs

enJeu={} # va permettre de savoir quand un thread entre dans une partie en pause ..

#tab pour les scores
score=[0]*2

while 1:    
    connexion, adresse = mySocket.accept()
    # Créer un nouvel objet thread pour gérer la connexion :
    th = ThreadClient(connexion)
            
    # Mémoriser la connexion dans le dictionnaire : 
    it = th.getName()
    if (len(conn_client))>= 2: #si on a déjà 2 clients ou +, les prochains sont des spectateurs
        spectateurs[it]=connexion
        spectateurs[it].send("print'vous etes connecte en tant que spectateur sous le nom %s' \n"%it)

    else :
        # redonner les noms Thread-1 / Thread 2 lorsqu'ils sont dispos
        print conn_client
        if isInConn_client("Thread-1")==False:
               print "here"
               th.setName("Thread-1")
        else :
               if isInConn_client("Thread-2")==False:
                      th.setName("Thread-2")
        it= th.getName()
        conn_client[it] = connexion
        conn_client[it].send("print'Vous etes connecte en tant que joueur'\n")

    print "Client %s connecté, adresse IP %s, port %s. \n" %\
           (it, adresse[0], adresse[1])

    th.start()



        
