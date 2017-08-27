
adressTable = ["50:8c:b1:6a:02:f7","d4:36:39:db:13:da","50:8c:b1:69:d2:d1","50:8c:b1:69:f9:45","d4:36:39:db:3b:9d"]
compteur = 0
#Creation et demarrage differents threads en fonction des adresses insérées dans la liste adressTable.
for adress in adressTable:
    thread_[compteur] =  MultiplesConnexion(adress)
    thread_[compteur].start()
    compteur += 1
    
#Declaration d'une classe pour le threading
class MultiplesConnexion(Thread):
	#Constructeur qui prend en parametre l'adresse du peripherique a connecter
	def __init__(self, adresse):
		#Initialisation du thread
		Thread.__init__(self)
		self.adresse = adresse

	def run(self):

			#Creation d'un objet Peripheral
			p = Peripheral()
			try:
				#Connection au peripherique en passant son adresse en parametre
				p.connect(self.adresse)
			except:
				print "Erreur connexion"
				subprocess.Popen(['sudo', 'hcitool', 'ledc','64'])
				subprocess.Popen(['sudo', 'hcitool', 'ledc','65'])
				time.sleep(2)
				p.connect(self.adresse)
            #Le peripherique est connecté on peut maintenant lui communiquer/recupérer des valeurs.
			print("Connect devices : " + str(self.adresse))
