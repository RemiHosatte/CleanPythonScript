#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3


conn = sqlite3.connect('DatabaseIOT.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS MONTREWITHTIME (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
TIME REAL NOT NULL,
BPM INTEGER  NOT NULL,
RRINTERVAL REAL NOT NULL
);""")

cursor.execute("""
INSERT INTO MONTREWITHTIME(BPM, TIME, RRINTERVAL)
VALUES(?, datetime('now'), ?)""", (85, 750.55))
conn.commit()

cursor.execute("""
SELECT ID, date(TIME), BPM, RRINTERVAL
FROM MONTREWITHTIME;""")
conn.commit()

for row in cursor:
   print "ID = ", row[0]
   print "TIME = ", row[1]
   print "BPM = ", row[2]
   print "RR = ", row[3], "\n"

conn.close()
