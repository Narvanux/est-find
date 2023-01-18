from playwright.sync_api import sync_playwright
from back.get_path import get_path

def write_file(key: str):
    with open(get_path() + 'back/jsession.txt', 'w') as f:
        f.write(key)

def read_session():
    with open(get_path() + 'back/jsession.txt', 'r') as f:
        return f.read().replace('\n', '')

def get_cookie():
    with sync_playwright() as sp:
        browser = sp.firefox.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto('https://sonaveeb.ee')
        jsession = context.cookies()[0]['value']
        write_file(jsession)
