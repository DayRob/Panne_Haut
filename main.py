# Declaration des librairies

import requests
import json
import datetime
import math
import time
import smtplib
from email.mime.text import MIMEText

# Declaration variable / dict

info = 0
saison = ""

date = ["01:00:00","04:00:00","07:00:00","10:00:00","13:00:00","16:00:00","19:00:00","22:00:00"]

# Config

configmailsender = "alexis.fireguard@gmail.com"
configmailsendermdp = "Alexis92000"
configmailrecever = "cmvilleroy@gmail.com"



#### SCRIPT ####

response = requests.get("http://www.infoclimat.fr/public-api/gfs/json?_ll=43.29695,5.38107&_auth=VkwHEFYoByUALVNkVSMCKwdvADUKfAgvVysGZVg2BHkHZlQ5UTQGbQVvWidQfwIzUH1UNww7Bz4AY1c3Xy1TL1Y3B2pWPAdgAGtTN1VsAikHKwB9CjQIL1crBmVYMwR5B2ZUMVE6BnoFa1o8UGACKFBkVDAMLAcgAGJXNl8zUzFWMAdrVjQHYABpUzVVegIpBzIAYAo1CGVXZwZpWDIENAdiVDFRYAZlBW5aOlB%2BAjFQYFQwDDEHPABkVzRfMFMvVioHGlZGB3gAL1NzVTACcAcpADUKawhk&_c=476d35b2b550d5c385f42471c9c5fcea")

try:
	while True:

		dateheure = datetime.datetime.now()
		temps = dateheure.strftime("%Y-%m-%d %X")

		
		## Transformation de l'heure actuelle en heure disponible par l'api 
		
		heure = dateheure.strftime("%H")

		heure = int(heure)
		if heure > 22 and heure < 1 :
			heure = "01"
		elif heure > 1 and heure < 4 :
			heure = "04"
		elif heure > 4 and heure < 7 :
			heure = "07"
		elif heure > 7 and heure < 10 :
			heure = "10"
		elif heure > 10 and heure < 13 :
			heure = "13"
		elif heure > 13 and heure < 16 : 
			heure = "16"
		elif heure > 16 and heure < 19 :
			heure = "19"
		elif heure > 19 and heure < 22 :
			heure = "22"

		# Récupération du degrès d'inclinaison en fonction de la saison / heure

		mois = dateheure.strftime("%m")

		if int(mois) >= 0 and int(mois) <= 3:
			saison="hiver"
			degres = {'00':'0','01':'0','02':'0','03':'0','04':'0','05':'0','06':'0','07':'0','08':'0','09':'35','10':'35','11':'30','12':'25','13':'25','14':'30','15':'30','16':'35','17':'0','18':'0','19':'0','20':'0','21':'0','22':'0','23':'0','24':'0'}
			for toto in degres:
				if toto == heure:
					degres_ = degres.get(toto)
					#print(degres_)
		if int(mois) >= 4 and int(mois) <= 6:
			saison="printemps"
			degres = {'00':'0','01':'0','02':'0','03':'0','04':'0','05':'0','06':'0','07':'0','08':'35','09':'30','10':'25','11':'20','12':'15','13':'15','14':'15','15':'20','16':'25','17':'30','18':'35','19':'0','20':'0','21':'0','22':'0','23':'0','24':'0'}
			for toto in degres:
				if toto == heure:
					degres_ = degres.get(toto)
					#print(degres_)
		if int(mois) >= 7 and int(mois) <= 9:
			saison="ete"
			degres = {'00':'0','01':'0','02':'0','03':'0','04':'0','05':'0','06':'0','07':'35','08':'30','09':'25','10':'20','11':'15','12':'15','13':'15','14':'15','15':'15','16':'15','17':'20','18':'25','19':'30','20':'35','21':'0','22':'0','23':'0','24':'0'}
			for toto in degres:
				if toto == heure:
					degres_ = degres.get(toto)
					#print(degres_)
		if int(mois) >= 10 and int(mois) <= 12:
			saison="automne"
			degres = {'00':'0','01':'0','02':'0','03':'0','04':'0','05':'0','06':'0','07':'0','08':'35','09':'30','10':'25','11':'20','12':'15','13':'15','14':'15','15':'20','16':'25','17':'30','18':'35','19':'0','20':'0','21':'0','22':'0','23':'0','24':'0'}
			for toto in degres:
				if toto == heure:
					degres_ = degres.get(toto)
					#print(degres_)
					
		for a in date:

			_temps = dateheure.strftime("%Y-%m-%d ")

			temps = dateheure.strftime("%Y-%m-%d "+heure+":00:00")
			if temps == _temps+a:
				
				data = response.json()

				# On supprime les infos inutiles

				del data['request_state']
				del data["request_key"]
				del data["message"]
				del data["model_run"]
				del data["source"]
				
				# Boucle qui récupère les clés
				
				for k in data.keys():
					valeur = data.get(k)

					# On supprime les infos inutiles
					
					del valeur["temperature"]
					del valeur["humidite"]
					del valeur["pression"]
					del valeur["pluie"]
					del valeur["pluie_convective"]
					del valeur["vent_direction"]
					del valeur["iso_zero"]
					del valeur["risque_neige"]
					del valeur["cape"]
					del valeur["nebulosite"]
					
					if temps == k:
						temps__ = k
					
					# Deuxieme boucle qui récupère les secondes clés
					
				for i in valeur.keys():

					resultat = valeur.get(i)
		
						# Troisieme boucle qui récupère les dernières valeurs
						
					for a in resultat.keys():

						if temps__ == temps:

							if info == 0:
								vent_moyen = resultat.get(a)
								print(vent_moyen)
								info=info+1
							else:
								rafale_max = resultat.get(a)
								if rafale_max > 57:
										
									msg = MIMEText('Votre panneau solaire n\'est plus en securite.\n\nLes rafales de vents sont trop violentes !\nElles atteignent les : '+str(rafale_max)+'km/h\nLe panneau a ete mis en mode securite.\n\nService client ,\nPanne Haut - St Erembert TSTI2d SIN\n\n'+dateheure.strftime("%Y-%m-%d %X"))

									msg['Subject'] = 'ALERTE - Panne Haut'
									msg['From'] = 'alexis.fireguard@gmail.com'
									msg['To'] = 'cmvilleroy@gmail.com'
										
									serveur=smtplib.SMTP("smtp.gmail.com",587)
									serveur.starttls()
									serveur.login(configmailsender,configmailsendermdp)
									serveur.sendmail(configmailsender,configmailrecever,str(msg))
									serveur.quit()
									print(rafale_max)
									info=0
									degres_ = 0
									print(degres_)
								else:
									print(rafale_max)
									info=0
									print(degres_)
				time.sleep(3600)	

except KeyboardInterrupt:
	exit()
