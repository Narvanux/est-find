from back.collector import SearchCollector
from back.word_getter import WordGetter
import sys

class Cli():
    def __init__(self, args):
        self.args = args
        
    def cli_handle(self):
        self.search_word()
        self.handle_word_response()

    def search_word(self):
        self.word = self.args['specific_word']
        self.get_word_id()
        if self.search_response['response-type'] == None:
            print("Word doesn't exist")
            sys.exit()
        elif self.search_response['response-type'] == 'list':
            print('There are similar words:')
            for index, item in enumerate(self.search_response['word-list']):
                print(str(index + 1) + ". " + item)
            choice = input('Choose one option: ')
            try:
                ch = int(choice)
                if ch in range(1, len(self.search_response['word-list']) + 1):
                    self.word = self.search_response['word-list'][ch - 1]
                    self.get_word_id()
                    self.get_by_lang()
                else:
                    print('Incorrect option.')
            except ValueError:
                print('Incorrect option.')
                sys.exit()
        else:
            self.get_by_lang()
    
    def handle_word_response(self):
        pass
        
    def get_word_id(self):
        sc = SearchCollector(self.args)
        self.search_response = sc.get_search(self.word)

    def get_by_lang(self):
        wg = WordGetter(self.search_response['word-id'], self.search_response['lang'], self.args)
        self.wg_return = wg.search()
