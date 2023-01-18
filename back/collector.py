import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class SearchCollector():

    def __init__(self, args):
        self.ua = UserAgent()
        self.args = args
        self.headers = {
            'User-Agent': self.ua.random
        }
        self.website = 'https://sonaveeb.ee/search/unif/dlall/dsall/'
    
    def get_search(self, word):
        site = requests.get(url=self.website + word, headers=self.headers)
        soup = BeautifulSoup(site.text, 'html.parser')
        list_elems = soup.find_all('li', class_='homonym-list-item')
        
        if len(list_elems) == 0:
            elem = soup.find('div', class_='word-details').find('span', class_='h1 mt-4 ml-3 d-inline-block')
            if elem != None and 'Ei leidnud midagi.' in elem.text:
                self.returnal = {
                    'response-type': None
                }
            else:
                elem = soup.find('div', class_='word-details').find('span').parent
                forms = elem.find_all('a', class_='word-form')
                word_list = []
                for i in forms:
                    word_list.append(i.attrs['data-word'])
                self.returnal = {
                    'response-type': 'list',
                    'word-list': word_list
                }
        else:
            variation = 0
            if self.args['variation'] > 0 and self.args['variation'] <= len(list_elems):
                variation = self.args['variation']
            else:
                print('Variation number out of bounds. Automatically set value to 1')
                variation = 1

            self.returnal = {
                'response-type': 'word',
                'lang': list_elems[variation - 1].find('span', class_='lang-code').text,
                'word-id': int(list_elems[variation - 1].find(attrs={'name': 'word-id'}).attrs['value'])
            }
        
        return self.returnal