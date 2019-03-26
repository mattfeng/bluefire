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
save_loc = f"./data/{data_folder}/raw"

cursor = db.cursor()
offset = 0
amt = 100

results = None

while results is None or len(results) > 0:
    cursor.execute(f"SELECT content FROM AStockNewsV1 LIMIT {offset}, {amt};")
    results = cursor.fetchall()

    for idx, row in enumerate(results):
        content, = row
        with open(f"{save_loc}/{offset + idx}.txt", "w") as f:
            f.write(f"{content}\n")

    offset += amt
    print(f"[i] Finished retrieving first {offset} results.")