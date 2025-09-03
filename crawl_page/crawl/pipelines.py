# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy import text
from scrapy.exceptions import DropItem
from resources.mysql_contextmanager import connect_mysql

MYSQL_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "database": "suumo",
    "user": "admin",
    "password": "admin123",
}

class SuumoPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Validation
        for field_name, field_meta in item.fields.items():
            value = adapter.get(field_name)

            # If field has 'required=True' but no data -> raise error
            if field_meta.get("required") and not value:
                raise DropItem(f"❌ Drop item {adapter.get('id')} because validation field `{field_name}`.")

        # Insert to MySQL
        try: 
            with connect_mysql(MYSQL_CONFIG) as engine:
                with engine.connect() as conn:
                    # Create table suumo properties
                    conn.execute(text("""
                        CREATE TABLE IF NOT EXISTS suumo_properties (
                            id INT PRIMARY KEY,
                            電話番号 TEXT NOT NULL,

                            家賃 TEXT NOT NULL,
                            管理費_共益費 TEXT,
                            敷金 TEXT,
                            礼金 TEXT,
                            保証金 TEXT,
                            敷引_償却 TEXT,

                            所在地 TEXT NOT NULL,
                            駅徒歩 TEXT,
                            間取り TEXT NOT NULL,
                            専有面積 TEXT NOT NULL,
                            築年数 TEXT NOT NULL,
                            階 TEXT NOT NULL,
                            向き TEXT NOT NULL,
                            建物種別 TEXT NOT NULL,

                            間取り詳細 TEXT,
                            構造 TEXT,
                            階建 TEXT,
                            築年月 TEXT,
                            エネルギー消費性能 TEXT,
                            断熱性能 TEXT,
                            目安光熱費 TEXT,
                            損保 TEXT,
                            駐車場 TEXT,
                            入居 TEXT,
                            取引態様 TEXT,
                            条件 TEXT,
                            取り扱い店舗物件コード TEXT,
                            SUUMO物件コード TEXT,
                            総戸数 TEXT,
                            情報更新日 TEXT,
                            次回更新日 TEXT,
                            契約期間 TEXT,
                            保証会社 TEXT,
                            ほか諸費用 TEXT,
                            備考 TEXT,

                            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """))

                    # Insert data (using multiple way)
                    fields = list(adapter.keys())
                    placeholders = ", ".join([f":{field}" for field in fields])
                    columns = ", ".join(fields)

                    query = text(f"""
                        INSERT INTO suumo_properties ({columns})
                        VALUES ({placeholders})
                    """)
                    conn.execute(query, {field: adapter.get(field) for field in fields})

                    conn.commit()
            
            spider.logger.info(f'✅ Success: Get data id={adapter.get("id")} successfully!!')

            return item
        
        except Exception as e:
            raise DropItem(f"❌ Drop item {adapter.get('id')} because: {e}.")
