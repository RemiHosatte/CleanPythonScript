# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sqlite3, subprocess, time, datetime
from bluepy.btle import Scanner, Peripheral, ADDR_TYPE_PUBLIC, ADDR_TYPE_RANDOM, AssignedNumbers

adresseMontre = "f9:eb:97:ee:2f:88"
cccid = AssignedNumbers.client_characteristic_configuration
hr =  AssignedNumbers.heart_rate
hrm = AssignedNumbers.heart_rate_measurement

#Creation d'un objet Peripheral
p = Peripheral()
try:
    #Connection au peripherique en passant son adresse en parametre
    p.connect(adresseMontre, addrType=ADDR_TYPE_RANDOM)
#Gestion des deconnexions
except:
    print "Erreur de connexion"
    print "Reconnexion ..."
    #Ecrase la connexion
    subprocess.Popen(['sudo', 'hcitool', 'ledc','64'])
    time.sleep(2)
    print '...'
    #Tentative de connexion
    p.connect(adresseMontre, addrType=ADDR_TYPE_RANDOM)
    print "..."

print "Connected "

#Le handle 32 correspond a la caracteristique Heart Rate Measurement
#\1\0 permet d'activer les notifications pour les montres MIO
p.writeCharacteristic(32, '\1\0')

while True:
    p.waitForNotifications(3.)
