#!/usr/bin/env python
# -*- coding:utf-8 -*-
#include <stdio.h>
#include <stdlib.h>

import socket
import main
from game import *
import  random
import time
from sys import argv

hote = argv[1]
port = 40000

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

msg_a_envoyer = b""
while msg_a_envoyer.upper()!=b"NO": #si on veut pas rejouer -> deoonnexion
    msg_a_envoyer = msg_a_envoyer.encode()
    connexion_avec_serveur.send(msg_a_envoyer)
    while 1:
		msg_recu =connexion_avec_serveur.recv(2048)
		if msg_recu.find("quelle colonne ? ")!=-1:
			msg_a_envoyer = input("quelle colonne ? ")
			break
		elif msg_recu.find('quelle ligne ?')!=-1:
			msg_a_envoyer = input ("quelle ligne ? ")
			break
                elif msg_recu.find('play again')!=-1:
                        msg_a_envoyer = input("play again ? YES OR NO")
                        break
                elif msg_recu.find("deconnexion")!=-1:
                        msg_a_envoyer=b"No"
                        break
                elif msg_recu.find("wanna play? yes or no")!=-1:
                        msg_a_envoyer=input("wanna play? yes or no")
                        break
                    
		else:
			exec(msg_recu)
print("Fermeture de la connexion")
connexion_avec_serveur.send('print"Fermeture de la connexion"')
connexion_avec_serveur.close()
