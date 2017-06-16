# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sqlite3
from bluepy.btle import Scanner, Peripheral, ADDR_TYPE_PUBLIC, ADDR_TYPE_RANDOM, AssignedNumbers
import subprocess, time, datetime


#Sript de connexion a la montre
adresseMontre = "f9:eb:97:ee:2f:88"
#Creation d'un objet Peripheral
p = Peripheral()

try:
    #Connection au peripherique en passant son adresse en parametre
    p.connect(adresseMontre, addrType=ADDR_TYPE_RANDOM)

except:
    #Si erreur (DONT WORK)
    print "Erreur de connexion"
    print "Reconnexion ..."
    subprocess.Popen(['sudo', 'hcitool', 'ledc','64'])

    time.sleep(2)
    print '...'
    p.connect(adresseMontre, addrType=ADDR_TYPE_RANDOM)
    print "..."

cccid = AssignedNumbers.client_characteristic_configuration
hr =  AssignedNumbers.heart_rate
hrm = AssignedNumbers.heart_rate_measurement

print hrm
print "Connected"
print " "
#Le handle 32 permet d'activer les notifications
#\1\0 permet d'activer les notifications voir doc Bluetooth
p.writeCharacteristic(32, '\1\0')


def print_hr(cHandle, data):
    #Connexion a la base de données
    conn = sqlite3.connect('DatabaseIOT.db')

    #Decomposition de data
    bpm = ord(data[1])
    rr = ord(data[2])
    rr2 = ord(data[3])

    #Conversion en binaire des valeurs de RR
    rr = '{:08b}'.format(rr)
    rr2 ='{:08b}'.format(rr2)

    #Inversion des deux valeurs
    rrFromWatch = float(int(rr2+rr,2))

    #Conversion du RR en millisecondes
    rrInMs = (rrFromWatch / 1024) * 1000

    #Insertion des données dans la BDD
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO MONTREWITHTIME(BPM, TIME, RRINTERVAL)
    VALUES(?, datetime('now'), ?)""", (bpm, round(rrInMs,2)))
    conn.commit()
    conn.close()

    #round permet de definir le nombre de chiffre derriere la virgule
    print "RR in ms: "+str(round(rrInMs,2))
    print "BPM: " +str(bpm)


p.delegate.handleNotification = print_hr


while True:
    p.waitForNotifications(3.)
