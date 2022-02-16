
import requests
from settings import *
class OpenSea():
    def __init__(self,key,contract_address,collection_size):
        self.key = key
        self.contract_address = contract_address
        self.collection_size = collection_size
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
        return response.text

    def get_all_listings(self):
        for url in self.url_list:
            self.get_listings(url)



# url = base_url
# # for i in range(collection_items+1):
# for i in range(40):
#     url = url + "&token_ids=" + str(i)
#     print(i+1, (i+1) % 30)
#     if (i+1) % MAX_QUERY_SIZE == 0:
        
     
    

# headers = {"X-API-KEY": APIKEY}

# response = requests.request("GET", url, headers=headers)

# print(response.text)