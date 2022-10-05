import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import os

class MySpider(CrawlSpider):
    name = 'bbccrawl'
    allowed_domains = ['bbc.com']
    start_urls = ['https://www.bbc.com/']
    COUNT_MAX = 150
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': COUNT_MAX
    }
    visited = []


    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        # Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # extract any link inside domain, follow any other link but callback to check if it's an article
        Rule(callback='parse_article', follow=True),
    )

    def parse_article(self, response): 
        page = response.url.split('/')[-1].replace('-','_')
        article = response.xpath('//article').get()
        # print("RESPONSE ARTICLE")
        # print(article)
        # print("RESPONSE ARTICLE")


        #if there are more articles it's some kind of /news page so you can skip it
        if len(response.xpath('//article').getall()) > 1:
            print('SKIPPING', response.url)
            with open('tutorial/output/wrong.txt', 'w+') as f:
                f.write(response.url + '\n')
            return
        title = response.xpath('//article//header//text()').get()
        if title is None:
            title = response.xpath('//article//h1//text()').get()
            print('NEW TITLE', title)
        # print("RESPONSE TITLE")
        # print(title)
        # print("RESPONSE TITLE")
        body = response.xpath('//article/div[contains(@data-component, "text-block")]').getall()
        # text_body = body.xpath('//text()')
        # print("RESPONSE body text")
        # print(text_body)
        # print("RESPONSE body text")
        # body = response.xpath('//article/p/text()').getall()
        # print("RESPONSE BODY")
        # for div in body:
        #     print(div)
            
        #     p = scrapy.Selector(text=div).xpath('.//p//text()')
        #     print(p)
        # print("RESPONSE BODY")
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        filename = os.path.join(fileDir, f'tutorial/output/{page}.html')
        # filename = f'output/article-{page}.html'
        if title is None:
            #very wrong page probably
            with open('tutorial/output/wrong.txt', 'w+') as f:
                f.write(response.url + '\n')
            return

        with open(filename, 'w+') as f:
            f.write(title + '\n\n')
            for div in body:
                p = scrapy.Selector(text=div).xpath('.//p//text()').get()
                f.write(p + '\n')
            # f.write(response.body)
        self.log(f'Saved file {filename}')
        self.visited.append(response.url)
        print('visited\n')
        print(self.visited)
        # return response.follow(url, self.parse_additional_page, cb_kwargs=dict(item=item))

    # def parse_additional_page(self, response, item):
    #     item['additional_data'] = response.xpath('//p[@id="additional_data"]/text()').get()
    #     return item