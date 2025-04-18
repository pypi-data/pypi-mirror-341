import scrapy

class RDProjectItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    organization = scrapy.Field()
    link = scrapy.Field()
    source = scrapy.Field()