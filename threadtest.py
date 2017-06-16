# -*- coding: utf-8 -*-
#!/usr/bin/env python

#Appel de la libraire sqlite
import sqlite3
#Appel de la librairie bluepy avec les differents modules
from bluepy.btle import Scanner, Peripheral, ADDR_TYPE_PUBLIC, ADDR_TYPE_RANDOM
#Import du module thread
from threading import Thread
#Import du module time pour phase de test
import time
#Librairie pour l'execution des commandes
import subprocess

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
			try:
				#Connection au peripherique en passant son adresse en parametre
				p.connect(self.adresse)
			except:
				#Si erreur (MARCHE MAL)
				print "Erreur co"
				subprocess.Popen(['sudo', 'hcitool', 'ledc','64'])
				subprocess.Popen(['sudo', 'hcitool', 'ledc','65'])
				time.sleep(2)
				p.connect(self.adresse)

			print("Connect devices : " + str(self.adresse))
			#Retourne la liste des characteristiques du peripherique
			chrs = p.getCharacteristics()
			#Parcours de la liste
			for chr in chrs:
					#print chr.getHandle()
					#Si le handle correspond a 18 on envoie les données au peripherique
					#18 Correspond au handle permettantde dialoguer avec le HM10 (WRITE,READ,NOTIF)
					if chr.getHandle() == 18:
						while True:
							#Recuperation des données via une Base de données sqlite3
							"""Toutes les secondes (time.sleep(1))
							On recupere la DERNIERE ligne de la table MONTRE qui correspond
							a la derniere valeur que la montre a envoyée et que l'on a
							inseré dans la bases de données
							time.sleep permet ici de regler la frequence d'envoi des données
							aux devices de visualisation
							"""
							conn = sqlite3.connect('DatabaseIOT.db')
							cursor = conn.cursor()

							cursor.execute("""
							SELECT BPM, RRINTERVAL
							FROM MONTREWITHTIME
							WHERE ID = (SELECT MAX(ID)  FROM MONTREWITHTIME);""")

							conn.commit()
							watchDataSQLite = cursor.fetchone()
							print(str(watchDataSQLite))

							conn.close()

							#Boucle infinie ou l'on envoie en boucle les données
							chr.write(str(watchDataSQLite))
							print "Data Send on " + str(self.adresse)
							time.sleep(1)

			"""On peut raccourcir le code en utilisant la methode writeCharacteristic()
			sur l'objet Peripheral avec comme parametre (18,données)
			"""

# Création des threads
#Chercher pour se connecter automatiquement a partir d'une liste (base de données ?)
#Exemple de liste dans le script multiplev1.py
thread_1 = MultiplesConnexion("50:8c:b1:6a:02:f7")
thread_2 = MultiplesConnexion("d4:36:39:db:13:da")
thread_3 = MultiplesConnexion("50:8c:b1:69:d2:d1")
thread_4 = MultiplesConnexion("50:8c:b1:69:f9:45")
thread_5 = MultiplesConnexion("d4:36:39:db:3b:9d")

#thread_1.start()
#thread_2.start()
thread_3.start()
#thread_4.start()
thread_5.start()



#A FAIRE:
#Reagir en cas erreur de connexion
"""Elle sont toutes du au fait que les peripherique sont deja connectés
Utilisation de la commande: sudo hciconfig hci0 down et up pour deconnecter les peripherique
Voir hciconfig hci0 reset qui combine les deux (Faire cette commande a l'execution du script ? voir delai)"""
