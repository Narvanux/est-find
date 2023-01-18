import requests
from back.session import read_session
from json import JSONDecodeError
import sys

class GetSearch():
    def __init__(self) -> None:
        self.base_url = "https://sonaveeb.ee/searchwordfrag/unif/"
        self.headers = {
        "Cookie": f"JSESSIONID={read_session()}",
        }
    
    def search(self, word):
        self.word = word
        self.response = requests.request("GET", self.base_url + self.word, headers=self.headers)

        self.resp_dict = {}
        
        try:
            self.resp_dict = self.response.json()
        except JSONDecodeError:
            print('Response could not be serialized')
            sys.exit()

        autocomplete = self.resp_dict['prefWords']
        forms = self.resp_dict['formWords']
        returnal = [
            [autocomplete, len(autocomplete)],
            [forms, len(forms)]
        ]
        return returnal
