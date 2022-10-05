
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os
# a scrapy spider that crawls the BBC website and saves the articles to files
class MySpider(CrawlSpider)