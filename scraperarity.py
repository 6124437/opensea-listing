from selenium import webdriver
from selenium.webdriver.support.ui import Select
# from bs4 import BeautifulSoup
import time
import sqlite3
from settings import *

class ScrapeRarity():
    def __init__(self,collection_name,collection_size,database_cursor):
        self.driver = webdriver.Firefox(executable_path="C:\geckodriver.exe")
        self.collection_name = collection_name
        self.collection_size = collection_size
        self.collection_url = "https://rarity.tools/" + self.collection_name
        self.database_cursor = database_cursor

    def scrapeSingleItem(self,tokenId):
        url = self.collection_url + "/view/" + str(tokenId)
        self.driver.get(url)
        time.sleep(SCRAPER_SLEEP_INTERVAL)
        elements = self.driver.find_elements_by_class_name('whitespace-nowrap')
        for element in elements:
            element_str = str(element.text.encode('ascii','ignore'))
            if "Rarity Rank" in element_str:
                return int(element_str.split('#')[1].strip("'"))

    def scrapeCollection(self):
        for tokenId in range(self.collection_size + 1):
            self.fetchAndWrite(tokenId)


    
    def writeToDatabase(self,tokenId,rarityRank,overwrite):
        self.database_cursor.execute("SELECT * FROM '" + TABLENAME + "' where token_id = '" + str(tokenId) + "'")
        rows = self.database_cursor.fetchall()
        if len(rows) == 0:
            sample = "INSERT INTO '" + TABLENAME + "' (token_id, rarity_rank) VALUES( '" + str(tokenId) + "', '" + str(rarityRank) + ")';"
            print(sample)
            self.database_cursor.execute("INSERT INTO '" + TABLENAME + "' (token_id, rarity_rank) VALUES( '" + str(tokenId) + "', '" + str(rarityRank) + "');")

    def fetchAndWrite(self,tokenId):
        rarity = self.scrapeSingleItem(tokenId)
        self.writeToDatabase(tokenId,rarity,True)

    

    # db = sqlite3.connect(DATABASE)
    # cursor = db.cursor()
    # cursor.execute("SELECT NameVoetbalpoules FROM '" + TABLENAME + "'where NameUnibet = '" + teamName + "'")
    # rows = cursor.fetchall()
    # return str(rows[0][0])
    # db.close()
