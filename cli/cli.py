from back.collector import SearchCollector
from back.word_getter import WordGetter
import sys

from rich.console import Console
from rich.table import Table

class Cli():
    def __init__(self, args):
        self.args = args
        self.con = Console(highlight=False)
        
    def cli_handle(self):
        self.search_word()
        self.handle_word_response()

    def search_word(self):
        self.word = self.args['specific_word']
        self.get_word_id()
        if self.search_response['response-type'] == None:
            self.con.print("Word doesn't exist!", style='red bold')
            sys.exit()
        elif self.search_response['response-type'] == 'list':
            self.con.print('There are several options:', style='rgb(77,166,255)')
            for index, item in enumerate(self.search_response['word-list']):
                self.con.print(f'{str(index + 1)}. {item}', style='rgb(255,221,51)')
            choice = self.con.input('[rgb(77,166,255)]Choose one option: ')
            try:
                ch = int(choice)
                if ch in range(1, len(self.search_response['word-list']) + 1):
                    self.word = self.search_response['word-list'][ch - 1]
                    self.get_word_id()
                    self.get_by_lang()
                else:
                    self.con.print("Incorrect option!", style='red bold')
            except ValueError:
                self.con.print("Incorrect option!", style='red bold')
                sys.exit()
        else:
            self.get_by_lang()
    
    def handle_word_response(self):
        self.con.print()
        self.con.rule(self.word, style='red', align='center')
        if self.wg_return['meaning-panels'] != None:
            for i in self.wg_return['meaning-panels']:
                if i['definition'] == None and i['original-definition'] == None and i['examples'] == None and i['synonyms'] == None:
                    pass
                elif i['definition'] == None and i['original-definition'] == None:
                    self.con.print(f"\n{i['number']}.", style = 'rgb(255,221,51)')
                else:
                    self.con.print(f"\n{i['number']}.", style = 'rgb(255,221,51)', end = ' ')
                def_combined = ''
                if i['original-definition'] != None: 
                    self.con.print(f"{i['original-definition']}", style='rgb(77,166,255)')
                if i['definition'] != None:
                    for x in i['definition']:
                        def_combined = def_combined + x + ', '
                    self.con.print(def_combined.rstrip(', '), style='rgb(89,179,0)')
                if i['synonyms'] != None:
                    self.con.print(', '.join(i['synonyms']), style='rgb(128,255,128)')
                if i['examples'] != None:
                    for x in i['examples']:
                        self.con.print(x, style='rgb(77,255,255)')

        if self.wg_return['short-forms'] != None:
            self.con.print()
            table = Table(title='Forms', show_header=False, style='rgb(255,221,51)', min_width=16)
            for x in self.wg_return['short-forms']:
                table.add_row(x[0], x[1])
            self.con.print(table)
        
    def get_word_id(self):
        sc = SearchCollector(self.args)
        self.search_response = sc.get_search(self.word)

    def get_by_lang(self):
        wg = WordGetter(self.search_response['word-id'], self.search_response['lang'], self.args)
        self.wg_return = wg.search()
