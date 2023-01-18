from back.search import GetSearch
import sys

class SearchCli():
    
    def __init__(self, args) -> None:
        self.args = args
        self.word = self.args['search']

    def search_cli_handle(self):
        self.search_word()

    def search_word(self):
        gs = GetSearch()
        res = gs.search(self.word)
        no_results = res[0][1] == 0 and res[1][1] == 0
        if no_results == True:
            print('No search results!')
            sys.exit()

        print('Results:')
        print('1. Autocomplete options:')
        if res[0][1] == 0:
            print('No such options')
        else:
            for index, item in enumerate(res[0][0]):
                print(f'\t{index + 1}. {item}')
        print('2. Form options:')
        if res[1][1] == 0:
            print('No such options')
        else:
            for index, item in enumerate(res[1][0]):
                print(f'\t{index + 1}. {item}')
