from dotenv import load_dotenv
import os
from settings import *
import time 
import sqlite3

from scraperarity import *
from opensea import *

if __name__ == '__main__':


    # Connect to rarity database
    database = sqlite3.connect(DATABASE)
    cursor = database.cursor()


    running = True
    load_dotenv()
    key = os.environ.get('openseaAPI')
    opensea = OpenSea(key,'0x7e6bc952d4b4bd814853301bee48e99891424de0',9999,database)



    # If table doesn't exist, create it.
    try:
        cursor.execute("SELECT * FROM '" + TABLENAME + "'")
    except sqlite3.OperationalError:
        cursor.execute("CREATE TABLE '" + TABLENAME + "' (token_id INTEGER PRIMARY KEY, rarity_rank INTEGER NOT NULL);")
        cursor.execute("SELECT * FROM '" + TABLENAME + "'")
    
    # # If table isn't completed, fill it.
    # rows = cursor.fetchall()
    # if len(rows) != 10000:
    #     scraper = ScrapeRarity(TABLENAME,10,cursor)
    #     scraper.scrapeCollection()
    
    cursor.execute("SELECT * FROM '" + TABLENAME + "'")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

 
    # Check listing table, create a new one if it doesn't exist.
    try:
        cursor.execute("SELECT * FROM '" + LISTINGTABLE + "'")
    except sqlite3.OperationalError:
        cursor.execute("CREATE TABLE '" + LISTINGTABLE + "' (order_id INTEGER PRIMARY KEY, listing_time INTEGER NOT NULL, expiration_time INTEGER NOT NULL, token_id INTEGER NOT NULL, symbol STRING NOT NULL, price INTEGER NOT NULL);")
        cursor.execute("SELECT * FROM '" + LISTINGTABLE + "'")   

    # Infinite loop to get listings if running is TRUE
    while True:
        if running:
            opensea.run()
            time.sleep(API_SLEEP_INTERVAL)

