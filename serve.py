from flask import Flask
from flask import render_template
import json
import requests
import smtplib
import datetime
from email.mime.text import MIMEText
import os

#Configuration 
configmailsender = "cmvilleroy@gmail.com"
configmailsendermdp = os.environ['configmailsendermdp']
configmailrecever = "cmvilleroy@gmail.com"
rafale_maximale_admissible = 16

# creates a Flask application, named app
app = Flask(__name__)
# a route where we will display a welcome message via an HTML template

@app.route("/")
def panne_haut():
    response = requests.get("http://www.infoclimat.fr/public-api/gfs/json?_ll=43.29695,5.38107&_auth=VkwHEFYoByUALVNkVSMCKwdvADUKfAgvVysGZVg2BHkHZlQ5UTQGbQVvWidQfwIzUH1UNww7Bz4AY1c3Xy1TL1Y3B2pWPAdgAGtTN1VsAikHKwB9CjQIL1crBmVYMwR5B2ZUMVE$
    response = response.json()
    dates = []
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
    mois = dateheure.strftime("%m")

    if int(mois) >= 0 and int(mois) <= 3:
        saison="hiver"
        degres = {'00':'0','01':'0','02':'0','03':'0','04':'0','05':'0','06':'0','07':'0','08':'0','09':'35','10':'35','11':'30','12':'25','13':'25','14':'30','15':'30','16':'35','17':'0','18':'0','19':'0','20':'0','21':'0','22':'0','23$
        for toto in degres:
            if toto == heure:
                degres_ = degres.get(toto)
                #print(degres_)
                 degres_ = degres.get(toto)
                #print(degres_)
    if int(mois) >= 4 and int(mois) <= 6:
        saison="printemps"
        degres = {'00':'0','01':'0','02':'0','03':'0','04':'0','05':'0','06':'0','07':'0','08':'35','09':'30','10':'25','11':'20','12':'15','13':'15','14':'15','15':'20','16':'25','17':'30','18':'35','19':'0','20':'0','21':'0','22':'0','$
        for toto in degres:
            if toto == heure:
                degres_ = degres.get(toto)
                #print(degres_)
    if int(mois) >= 7 and int(mois) <= 9:
        saison="ete"
        degres = {'00':'0','01':'0','02':'0','03':'0','04':'0','05':'0','06':'0','07':'35','08':'30','09':'25','10':'20','11':'15','12':'15','13':'15','14':'15','15':'15','16':'15','17':'20','18':'25','19':'30','20':'35','21':'0','22':'0$
        for toto in degres:
            if toto == heure:
                degres_ = degres.get(toto)
                #print(degres_)
    if int(mois) >= 10 and int(mois) <= 12:
        saison="automne"
        degres = {'00':'0','01':'0','02':'0','03':'0','04':'0','05':'0','06':'0','07':'0','08':'35','09':'30','10':'25','11':'20','12':'15','13':'15','14':'15','15':'20','16':'25','17':'30','18':'35','19':'0','20':'0','21':'0','22':'0','$
        for toto in degres:
            if toto == heure:
                degres_ = degres.get(toto)
                #print(degres_)
    for key in response.keys():
        if key.startswith('2021'):
            dates.append(key)
    dates_triees = sorted(dates)
    dates_a_afficher = dates[:17]

    rafales_max = []
    for date in dates_a_afficher:
        rafales_max.append(response[date]['vent_rafales']['10m'])

    mise_en_securite = []
    for rafale in rafales_max:
        if rafale >rafale_maximale_admissible:

            msg = MIMEText('Votre panneau solaire n\'est plus en securite.\n\nLes rafales de vents sont trop violentes !\nElles atteignent les : '+str(rafale)+'km/h\nLe panneau a ete mis en mode securite.\n\nService client ,\nPanne Haut $
            msg['Subject'] = 'ALERTE - Panne Haut'
            msg['From'] = configmailsender
            msg['To'] = configmailrecever

            serveur=smtplib.SMTP("smtp.gmail.com",587)
            serveur.starttls()
            serveur.login(configmailsender,configmailsendermdp)
            serveur.sendmail(configmailsender,configmailrecever,str(msg))
            serveur.quit()
            mise_en_securite.append(0)
        else :
            mise_en_securite.append(1)

    return render_template('index.html', rafales_max=json.dumps(rafales_max), dates_a_afficher=json.dumps(dates_a_afficher), mise_en_securite=json.dumps(mise_en_securite))

@app.route('/SomeFunction')
def SomeFunction():
    print('')
    return "Nothing"
# run the applicationhttps://www.infoclimat.fr/public-api/gfs/json?_ll=43.29695,5.38107&_auth=VkwHEFYoByUALVNkVSMCKwdvADUKfAgvVysGZVg2BHkHZlQ5UTQGbQVvWidQfwIzUH1UNww7Bz4AY1c3Xy1TL1Y3B2pWPAdgAGtTN1VsAikHKwB9CjQIL1crBmVYMwR5B2ZUMVE6BnoFa1o$
if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
#response = request.get("http://www.infoclimat.fr/public-api/gfs/json?_ll=43.29695,5.38107&_auth=VkwHEFYoByUALVNkVSMCKwdvADUKfAgvVysGZVg2BHkHZlQ5UTQGbQVvWidQfwIzUH1UNww7Bz4AY1c3Xy1TL1Y3B2pWPAdgAGtTN1VsAikHKwB9CjQIL1crBmVYMwR5B2ZUMVE6BnoF$


