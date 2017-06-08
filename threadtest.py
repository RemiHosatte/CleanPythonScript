# -*- coding: utf-8 -*-
#Appel de la librairie bluepy avec les differents modules
from bluepy.btle import Scanner, Peripheral, ADDR_TYPE_PUBLIC, ADDR_TYPE_RANDOM
#Import du module thread
from threading import Thread
#Import du module time pour phase de test
import time
#Declaration d'une classe pour le threading
class MultiplesConnexion(Thread):
	#Constructeur qui prend en parametre l'adresse du peripherique a connecter
	def __init__(self, adresse):
		#Init du thread
		Thread.__init__(self)
		self.adresse = adresse

	def run(self):

			#Creation d'un objet Peripheral
			p = Peripheral()
			#Connection au peripherique en passant son adresse en parametre
			p.connect(self.adresse)
			print("Connect devices : " + str(self.adresse))
			#Retourne la liste des characteristiques du peripherique
			chrs = p.getCharacteristics()
			#Parcours de la liste
			for chr in chrs:
					print chr.getHandle()
					#Si le handle correspond a 18 on envoie les données au peripherique
					#18 Correspond au handle permettantde dialoguer avec le HM10 (WRITE,READ,NOTIF)
					if chr.getHandle() == 18:
						while True:
							#Boucle infinie ou l'on envoie en boucle les données
							chr.write("81B4H")
							print "Data Send"
							time.sleep(1)

			"""On peut raccourcir le code en utilisant la methode writeCharacteristic()
			sur l'objet Peripheral avec comme parametre (18,données)
			"""

# Création des threads
#Chercher pour se connecter automatiquement a partir d'une liste (base de données ?)
#Exemple de liste dans le script multiplev1.py
thread_4 = MultiplesConnexion("50:8c:b1:69:d2:d1")
thread_5 = MultiplesConnexion("d4:36:39:db:3b:9d")

thread_4.start()
thread_5.start()


#A FAIRE:
#Reagir en cas erreur de connexion
"""Elle sont tous le temps au fait que les peripherique sont deja connectés
Utilisation de la commande: sudo hciconfig hci0 down et up pour deconnecter les peripherique"""
