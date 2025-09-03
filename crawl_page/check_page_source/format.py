from bs4 import BeautifulSoup
import json
import requests


def format_html_page_source(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')

    page_source_formatted = soup.prettify()

    with open('./check_page_source/formatted.html', 'w') as file:
        file.write(page_source_formatted)

if __name__ == '__main__':
    # with open(DATA_PATH_FUNC('thegioididong', 'l2_20250402-105034.json')) as file:
    #     data = json.load(file)
    
    # page_source = data['page_source']
    # format_html_page_source(page_source)
    response = requests.get('https://suumo.jp/jj/chintai/ichiran/FR301FC001/?fw2=&mt=9999999&cn=9999999&ta=27&et=9999999&sc=27123&shkr1=03&ar=060&bs=040&ct=9999999&shkr3=03&shkr2=03&srch_navi=1&mb=0&shkr4=03&cb=0.0')
    format_html_page_source(response.text)