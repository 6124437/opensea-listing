import requests
from settings import *
from math import pow
import time

class OpenSea():
    def __init__(self,key,contract_address,collection_size,database):
        self.key = key
        self.contract_address = contract_address
        self.collection_size = collection_size
        self.database = database
        self.database_cursor = self.database.cursor()

        # Create the list with all urls to GET
        self.base_url = "https://api.opensea.io/wyvern/v1/orders?asset_contract_address=" + contract_address + "&bundled=false&sale_kind=0&include_bundled=false&limit=20&offset=0&order_by=created_date&order_direction=desc"
        self.url_list = []
        self.get_all_urls()


    def get_all_urls(self):
        url = self.base_url
        # Loop over all token ids
        for i in range(self.collection_size + 1):
            url = url + "&token_ids=" + str(i)

            # Save the url to the list if max query size is reached or last token id is reached
            if (i+1) % MAX_QUERY_SIZE == 0 or i == self.collection_size:
                self.url_list.append(url)
                url = self.base_url

    def get_listings(self,url):
        headers = {"X-API-KEY": self.key}
        response = requests.request("GET", url, headers=headers)

        return response.json()

    def register_new_records(self,tokenId,orderId,currentPrice,listingTime,expirationTime):

        pass

    def process_record(self,record):

        # save all variables
        orderId = record["id"]
        listingTime = record["listing_time"]
        expirationTime = record["expiration_time"]
        tokenId = record["asset"]["token_id"]
        symbol = record["payment_token_contract"]["symbol"]
        price = record["current_price"]

        print(orderId, tokenId)

        # check if record exists
        self.database_cursor.execute("SELECT * FROM '" + LISTINGTABLE + "' where order_id = '" + str(orderId) + "'")        
        rows = self.database_cursor.fetchall()
        if len(rows) == 0:

        # insert into database
            insertStatement = "INSERT INTO '" + LISTINGTABLE + "' (order_id, listing_time, expiration_time, token_id, symbol, price) VALUES( '" + str(orderId) + "', '" + str(listingTime) + "', '" + str(expirationTime) + "', '" + str(tokenId) + "', '" + str(symbol) + "', '" + str(price) + "');"
            self.database_cursor.execute(insertStatement)

    def run(self):
        for url in self.url_list:

            while True:
                listings = self.get_listings(url)
                try:
                    for listing in listings['orders']:
                        self.process_record(listing)
                        self.database.commit()
                except KeyError:
                    print(listings['detail'] + " Continuing in " + API_SLEEP_INTERVAL " seconds.")
                    time.sleep(API_SLEEP_INTERVAL)
                    continue
                break