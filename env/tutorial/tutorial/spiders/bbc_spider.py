import scrapy
import os

class BbcSpider(scrapy.Spider):
    name = "bbc"
    root = 'https://www.bbc.com/'
    urls = [
            'https://www.bbc.com/news'
        ]

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_page1)

    def parse_page1(self, response):
        once = True
        for url in response.css('a.gs-c-promo-heading::attr(href)').getall():
            if once :
                print('found url', url)
                yield scrapy.Request(self.root + url, callback=self.parse_article)
                # once = False

    def parse_article(self, response): 
        # print("RESPONSE")
        # print(response.body)
        # print("RESPONSE")
        page = response.url.split('/')[-1].replace('-','_')
        # page = page.replace(':')
        articles = response.xpath('//article').getall()
        
        print(page, response.url)
        if len(articles) > 1:
            print('SKIPPING', response.url)
            with open('tutorial/output/wrong.txt', 'w+') as f:
                f.write(response.url + '\n')
            return

        article = scrapy.Selector(text=articles[0])
        # title = response.xpath('//article//header//text()').get()
        title = article.xpath('//header//text()').get()
        if title is None:
            title = article.xpath('//h1//text()').get()
            print('NEW TITLE', title)
        # print("RESPONSE TITLE")
        # print(title)
        # print("RESPONSE TITLE")
        body = article.xpath('.//div[contains(@data-component, "text-block")]').getall()
        # text_body = body.xpath('//text()')
        print("RESPONSE body text")
        print(body)
        print("RESPONSE body text")
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
                print('div\n')
                print(div)
                p = scrapy.Selector(text=div).xpath('.//p//text()').get()
                print(p)
                f.write(p + '\n')
        self.log(f'Saved file {filename}')