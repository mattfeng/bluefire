#!/usr/bin/env python

import mysql.connector
import sys

HOST = "bluefireai-ext.c4ijumbxcwap.ap-southeast-1.rds.amazonaws.com"
USER = "scraper_user"
PASS = "c9sZrtGW"
DBNAME = "scraper_db"

if len(sys.argv) != 2:
    print("Usage: ./retrieve.py <data folder>")
    quit()

db = mysql.connector.connect(
    host=HOST,
    user=USER,
    passwd=PASS,
    database=DBNAME
)

data_folder = sys.argv[1]
save_loc = f"./data/{data_folder}/raw/"

cursor = db.cursor()
cursor.execute("SELECT * FROM AStockNewsV0;")

results = cursor.fetchall()

for row in results:
    print(row)