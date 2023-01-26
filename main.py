from cli.cli import Cli
from cli.search_cli import SearchCli
import argparse
from back.session import get_cookie
from back.cookie_status import cookie_expired
from rich.console import Console

def handle_args():
    parser = argparse.ArgumentParser("Gets pages from Sõnaveeb")
    parser.add_argument('-s', '--search', help='get search result for specified query', default='')
    parser.add_argument('-w', '--specific-word', type=str, help='specify the exact word you want to get', default='')
    parser.add_argument('-t', '--translate', type=str, help='language you want to translate word into', default='')
    parser.add_argument('-sn', '--synonyms', action='store_true', help='show synonims of this word', default='')
    parser.add_argument('-e', '--examples', action='store_true', help="show examples of this word's usage", default=False)
    parser.add_argument('-f', '--forms', action='store_true', help='display main forms of the word', default=False)
    parser.add_argument('-v', '--variation', type=int, help='preffered variation of the input', default=1)
    parser.add_argument('-l', '--limit', type=int, help='limit amount of panels shown', default=0)
    parser.add_argument('-d', '--definition', action='store_true', help='show definition of the word', default=False)
    parser.add_argument('-u', '--upgrade-cookies', action='store_true', help='upgrade the cookie in back/jsession.txt', default=False)
    return vars(parser.parse_args())

def main():
    args = handle_args()
    con = Console()
    no_cookie = cookie_expired()
    if no_cookie:
        con.print('Automatically updating cookie data!', style='rgb(77,166,255)')
        get_cookie()
    
    query_not_specified = args['search'] == '' and args['specific_word'] == ''
    if args['upgrade_cookies'] == True:
        get_cookie()
        con.print('Cookies upgraded!', style='rgb(77,166,255)')
    elif len(args) == 0 or query_not_specified:
        pass #launch tui
    elif args['search'] != '':
        sc = SearchCli(args)
        sc.search_cli_handle()
    elif args['specific_word'] != '':
        cli = Cli(args)
        cli.cli_handle()
    else:
        con.print('Error!', style='red')

if __name__ == "__main__":
    main()
