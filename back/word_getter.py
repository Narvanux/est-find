import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from back.session import read_session

class WordGetter():

    def __init__(self, word, lang, args):
        self.jsession = read_session()
        self.ua = UserAgent()
        self.args = args
        self.headers = {
            'User-Agent': self.ua.random,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "X-Requested-With": "XMLHttpRequest",
            "DNT": "1",
            "Connection": "keep-alive",
            "Cookie": f"JSESSIONID={self.jsession}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }
        self.website = 'https://sonaveeb.ee/worddetails/unif/'
        self.lang = lang
        self.word = word
        self.args = args

    def search(self):
        # source = requests.request("GET", self.website + str(self.word), headers=self.headers).text

        # with open('index.html', 'w') as f:
        #     f.write(source)
        
        with open('index.html', 'r') as f:
            source = f.read()
        
        self.soup = BeautifulSoup(source, 'html.parser')
        self.word_types = [] 
        type_raw = self.soup.find('div', 'content-title').find_all('span', 'my-1')
        for i in type_raw:
            self.word_types.append(i.text)
        self.returnal = {}
        self.returnal['meaning-panels'] = self.get_meaning_panels()
        self.returnal['short-forms'] = self.get_short_forms()
        return self.returnal
    
    def get_meaning_panels(self):
        panels = self.soup.find_all('section', class_='level-3-panel meaning-panel d-flex flex-row')
        panel_list = []

        limit = 0
        if self.args['limit'] <= 0 or self.args['limit'] > len(panels):
            limit = len(panels)
        else:
            limit = self.args['limit']
        
        for panel in panels[0:limit]:
            panel_dict = {}
            panel_dict['number'] = panel.find('strong', class_='definition-value').text
            panel_dict['original-definition'] = panel.find('span', class_='definition-value').text
            match = panel.find('div', class_='matches')
            if match != None and self.args['translate'] != '':
                for trans in match.find('div', class_='additional-meta').find_all(recursive=False):
                    if trans.find('span', class_='lang-code') != None:
                        if trans.find('span', class_='lang-code').text == self.args['translate']:
                            txt = []
                            words = trans.find_all('span', class_='mr-1')
                            for word in words:
                                txt.append(word.find('a', recursive=False).find('span', recursive=False).find('span', recursive=False).text)
                            panel_dict['definition'] = txt
                        else:
                            panel_dict['definition'] = None
            else:
                panel_dict['definition'] = None
            panel_list.append(panel_dict)
        
        return panel_list

    def get_short_forms(self):
        if self.args['short_forms'] != False:
            sf_table_elem = self.soup.find(class_='morphology-panel')
            sf_table = []
            for tb_row in sf_table_elem.find_all('tr'):
                row = []            
                for elem in tb_row.find_all('td'):
                    row.append(elem.find('span', class_='form-value-field').text)
                sf_table.append(row)
            return sf_table
        else:
            return None
