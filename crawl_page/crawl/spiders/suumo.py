from pathlib import Path
from check_page_source.format import format_html_page_source
from resources.mysql_contextmanager import connect_mysql
from sqlalchemy import text
from crawl.items import SuumoItem
from pprint import pprint

import scrapy
import functools
import functools

MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "database": "suumo",
    "user": "admin",
    "password": "admin123",
}

valid_columns = [
    "id", "電話番号", "家賃", "管理費_共益費", "敷金", "礼金", "保証金", 
    "敷引_償却", "所在地", "駅徒歩", "間取り", "専有面積", "築年数", "階", 
    "向き", "建物種別", "間取り詳細", "構造", "階建", "築年月", "エネルギー消費性能", 
    "断熱性能", "目安光熱費", "損保", "駐車場", "入居", "取引態様", "条件", 
    "取り扱い店舗物件コード", "SUUMO物件コード", "総戸数", "情報更新日", "次回更新日", 
    "契約期間", "保証会社", "ほか諸費用", "備考"
]

class QuotesSpider(scrapy.Spider):
    name = "suumo"

    def start_requests(self):
        try:
            with connect_mysql(MYSQL_CONFIG) as engine:
                with engine.connect() as conn:
                    links_not_crawled = conn.execute(text(
                        """SELECT id, url FROM links_from_suumo WHERE crawled = 0;"""
                        # """SELECT id, url FROM links_from_suumo WHERE crawled = 0 LIMIT 1;"""
                    )).fetchall() # [(id, url), ...]

            for id, url in links_not_crawled:
                yield scrapy.Request(
                    url=url, 
                    callback=functools.partial(self.parse, id=id)
                )

        except Exception as e:
            print(f'⁉️ {e}')

    def parse(self, response, id):
        data = {}

        def safe_extract(selector):
            txt = selector.xpath("string()").get()
            return txt.strip().replace("\t", "") if txt else ""

        try:
            id_data = {'id': id}
            data.update(id_data)

            renting_price = safe_extract(response.css('.property_view_note-emphasis'))
            others_price_container = response.css(".property_view_note-list span:not([class]), .property_view_note-list span[class='']")
            others_price_list_str = [safe_extract(price).replace("\xa0", "") for price in others_price_container] # '敷金:\xa0-'
            others_price_list_dict = {key.replace("・", "_"): value for key, value in [others_price.split(':') for others_price in others_price_list_str]} # ["管理費・共益費: ..."] -> {"管理費_共益費": "..."}
            price_data = {
                '家賃': renting_price,
                **others_price_list_dict
            }
            # update price
            data.update(price_data)

            phone_number = safe_extract(response.css('.viewform_advance_shop-cal-number'))
            phone_data = {'電話番号': phone_number}
            # update phone number
            data.update(phone_data)

            building_info_container = response.css('table.property_view_table')
            titles = [safe_extract(th) for th in building_info_container.css("th")]
            values = [safe_extract(td) for td in building_info_container.css("td")]
            building_info_data = dict(zip(titles, values))
            # update data building info
            data.update(building_info_data)

            room_info_container = response.css('table.data_table')
            titles = [safe_extract(th) for th in room_info_container.css("th")]
            values = [safe_extract(td) for td in room_info_container.css("td")]
            room_info_data = dict(zip(titles, values))
            # update data room info
            data.update(room_info_data)

            data_valid = SuumoItem({key: value for key, value in data.items() if key in valid_columns})

            yield data_valid

        except Exception as e:
            print(f'⁉️ {e}')
        