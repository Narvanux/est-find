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
        source = requests.request("GET", self.website + str(self.word), headers=self.headers).text

        # with open('index.html', 'w') as f:
        #     f.write(source)
        
        # with open('index.html', 'r') as f:
        #     source = f.read()
        
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
        if self.args['definition'] or self.args['translate'] != '' or self.args['examples'] or self.args['synonyms']:
            panels = self.soup.find_all('section', class_='level-3-panel meaning-panel d-flex flex-row')
            # print(panels)
            panel_list = []

            limit = 0
            if self.args['limit'] <= 0 or self.args['limit'] > len(panels):
                limit = len(panels)
            else:
                limit = self.args['limit']
            
            for panel in panels[0:limit]:
                panel_dict = {}
                if panel.find('strong', class_='definition-value') == None:
                    panel_dict['number'] = '1'
                else:
                    panel_dict['number'] = panel.find('strong', class_='definition-value').text
                if self.args['definition']:
                    panel_dict['original-definition'] = panel.find('span', class_='definition-value').text
                else:
                    panel_dict['original-definition'] = None
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
                                pass
                                # panel_dict['definition'] = None
                else:
                    panel_dict['definition'] = None

                exas = panel.find('div', class_='dependence-group')
                if exas != None and self.args['examples']:
                    exa_out = []
                    for exa in exas.find_all('div', class_='usage-item'):
                        exa_out.append(exa.find('span', class_='example-text-value').text)
                    panel_dict['examples'] = exa_out
                else:
                    panel_dict['examples'] = None

                synoms = panel.find('div', class_='synonyms')
                if synoms != None and self.args['synonyms']:
                    syn_out = []
                    for syn in synoms.find_all('span', class_="text-nowrap mr-1"):
                        syn_out.append(syn.find('a').find('span', recursive=False).find('span', recursive=False).text)
                    panel_dict['synonyms'] = syn_out
                else:
                    panel_dict['synonyms'] = None

                panel_list.append(panel_dict)
            
            return panel_list
        else:
            return None

    def get_short_forms(self):
        if self.args['forms'] != False:
            sf_table_elem = self.soup.find(class_='morphology-panel')
            sf_table = []
            for tb_row in sf_table_elem.find_all('tr'):
                row = []            
                for elem in tb_row.find_all('td'):
                    wds = []
                    for i in elem.find_all('span', class_='form-value-field'):
                        wds.append(i.text)
                    row.append(', '.join(wds))
                sf_table.append(row)
            return sf_table
        else:
            return None
