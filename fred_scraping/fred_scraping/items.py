# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class FredScrapingItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    Source = scrapy.Field()
    Description = scrapy.Field()
    date = scrapy.Field()  

    
