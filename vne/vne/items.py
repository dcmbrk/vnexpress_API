import scrapy

class VneItem(scrapy.Item):
    category = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    lead = scrapy.Field()
    date = scrapy.Field()
    main_content = scrapy.Field()
