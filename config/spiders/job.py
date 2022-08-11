import scrapy


class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['quera.org']
    start_urls = ['https://quera.org/magnet/jobs']

    def parse(self, response):
        pass
