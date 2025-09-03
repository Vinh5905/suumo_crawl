from pathlib import Path
from check_page_source.format import format_html_page_source
from resources.mysql_contextmanager import connect_mysql
from sqlalchemy import text

import scrapy
import functools

MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "database": "suumo",
    "user": "admin",
    "password": "admin123",
}

def get_link_page(page_num):
    base_link = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?fw2=&mt=9999999&cn=9999999&ta=27&et=9999999&sc=27123&shkr1=03&ar=060&bs=040&ct=9999999&shkr3=03&shkr2=03&srch_navi=1&mb=0&shkr4=03&cb=0.0'
    if page_num == 1: 
        # Keep origin because page 1 is as same as base link
        return f'{base_link}'
    else: 
        return f'{base_link}&page={page_num}'

class QuotesSpider(scrapy.Spider):
    name = "suumo"

    def start_requests(self):
        for page_num in range(1, 80):
            page_url = get_link_page(page_num)
            yield scrapy.Request(
                url=page_url, 
                callback=functools.partial(self.parse, page_num=page_num)
            )

    def parse(self, response, page_num):
        try:
            container_element = response.css('div#js-bukkenList')
            links = container_element.css('div.cassetteitem-item a.js-cassette_link_href::attr(href)').getall()

            if len(links) == 0:
                return ValueError(f'Page num {page_num} do not have any links!! (May be the last page)')
            
            full_links = ['https://suumo.jp' + link for link in links]

            with connect_mysql(MYSQL_CONFIG) as engine:
                with engine.connect() as conn:
                    # create table if not exists
                    conn.execute(text("""
                            CREATE TABLE IF NOT EXISTS links_from_suumo (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                url TEXT NOT NULL,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                crawled BOOLEAN NOT NULL DEFAULT FALSE
                            )
                        """))
            
                    # insert multiple links
                    conn.execute(
                        text("""INSERT INTO links_from_suumo (url) VALUES (:url)"""),
                        [{"url": link} for link in full_links]
                    )
                    conn.commit() 

            print(f'✅ Get {len(full_links)} links from page {page_num} successfully!!')

        except Exception as e:
            print(f'⁉️ {e}')
        