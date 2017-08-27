def print_hr(cHandle, data):
    #Connexion a la base de données
    conn = sqlite3.connect('DatabaseIOT.db')

    #Decomposition de data
    bpm = ord(data[1])
    rrByteOne = ord(data[2])
    rrByteTwo = ord(data[3])

    #Conversion en binaire des valeurs de RR
    rrByteOne = '{:08b}'.format(rrByteOne)
    rrByteTwo ='{:08b}'.format(rrByteTwo)

    #Inversion des deux valeurs
    rrReverse = float(int(rrByteTwo+rrByteOne,2))

    #Conversion du RR en millisecondes
    rrInMs = (rrReverse / 1024) * 1000

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
