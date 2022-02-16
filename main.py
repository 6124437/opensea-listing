from dotenv import load_dotenv
import os
from settings import *
import time 
import sqlite3

from scraperarity import *
from opensea import *

if __name__ == '__main__':




    running = True
    load_dotenv()
    key = os.environ.get('openseaAPI')
    opensea = OpenSea(key,'0x7e6bc952d4b4bd814853301bee48e99891424de0',9999)


    # Check database
    database = sqlite3.connect(DATABASE)
    cursor = database.cursor()
    try:
        cursor.execute("SELECT * FROM '" + TABLENAME + "'")
    except sqlite3.OperationalError:
        cursor.execute("CREATE TABLE '" + TABLENAME + "' (token_id INTEGER PRIMARY KEY, rarity_rank INTEGER NOT NULL);")
        cursor.execute("SELECT * FROM '" + TABLENAME + "'")
    

    rows = cursor.fetchall()
    if len(rows) != 10000:

        scraper = ScrapeRarity(TABLENAME,10,cursor)
        scraper.scrapeCollection()
    
    cursor.execute("SELECT * FROM '" + TABLENAME + "'")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


    # # Infinite loop to get listings if running is TRUE
    # while True:
    #     if running:
    #         opensea.get_all_listings()
    #         time.sleep(API_SLEEP_INTERVAL)

