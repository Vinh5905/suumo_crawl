# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class SuumoItem(scrapy.Item):
    id = scrapy.Field(required=True)

    電話番号 = scrapy.Field(required=True)            # Phone number

    家賃 = scrapy.Field(required=True)               # Rent (monthly base rent fee)
    管理費_共益費 = scrapy.Field()                      # Maintenance / common service fee
    敷金 = scrapy.Field()                            # Security deposit (refundable in principle)
    礼金 = scrapy.Field()                            # Key money (non-refundable gratuity fee)
    保証金 = scrapy.Field()                          # Guarantee money (similar to deposit, may vary by region)
    敷引_償却 = scrapy.Field()                        # Non-refundable portion of deposit / depreciation fee

    所在地 = scrapy.Field(required=True)              # Property address
    駅徒歩 = scrapy.Field()                           # Walking distance to the nearest station
    間取り = scrapy.Field(required=True)              # Floor plan (layout, e.g., 1LDK)
    専有面積 = scrapy.Field(required=True)            # Exclusive floor area (m²)
    築年数 = scrapy.Field(required=True)              # Building age (years since built)
    階 = scrapy.Field(required=True)                  # Floor number of the unit
    向き = scrapy.Field(required=True)                # Direction the unit faces (e.g., South)
    建物種別 = scrapy.Field(required=True)            # Building type (e.g., apartment, house)

    間取り詳細 = scrapy.Field()                      # Detailed floor plan
    構造 = scrapy.Field()                            # Building structure (e.g., RC, steel)
    階建 = scrapy.Field()                            # Total number of floors in building
    築年月 = scrapy.Field()                          # Construction year and month
    エネルギー消費性能 = scrapy.Field()                # Energy consumption performance
    断熱性能 = scrapy.Field()                         # Thermal insulation performance
    目安光熱費 = scrapy.Field()                       # Estimated monthly utility cost
    損保 = scrapy.Field()                            # Fire/house insurance details
    駐車場 = scrapy.Field()                          # Parking availability and fee
    入居 = scrapy.Field()                            # Available move-in date
    取引態様 = scrapy.Field()                        # Transaction type
    条件 = scrapy.Field()                            # Special conditions (e.g., females only)
    取り扱い店舗物件コード = scrapy.Field()             # Handling store property code
    SUUMO物件コード = scrapy.Field()                  # SUUMO property code
    総戸数 = scrapy.Field()                          # Total number of units in building
    情報更新日 = scrapy.Field()                       # Date of last information update
    次回更新日 = scrapy.Field()                       # Next scheduled update date
    契約期間 = scrapy.Field()                        # Contract period (e.g., 2 years)
    保証会社 = scrapy.Field()                        # Guarantee company information
    ほか諸費用 = scrapy.Field()                       # Other miscellaneous costs
    備考 = scrapy.Field()                            # Additional remarks / notes

    create_at = scrapy.Field()