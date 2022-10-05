import scrapy
from scrapy.linkextractors import LinkExtractor
#article
#   1 header
#   any p


class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://www.bbc.com/news']

    def parse(self, response):
        print('important!!!!!!!')
        print(response)

        # for article in response.xpath('//article').get():
        #     yield {'title': article.xpath('//header').get(), 'body': article.xpath('//p').getAll() }

        # for title in response.css('.oxy-post-title'):
        #     yield {'title': title.css('::text').get()}
        for link in LinkExtractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse)
        # for next_page in response.css('a.next'):
        #     yield response.follow(next_page, self.parse)