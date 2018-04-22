from scrapy import Spider
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

class DemoSpider(Spider):
    name = 'thefuck'
    start_urls= ['http://ipip.net']

    def parse(self, response):
        print('-----------------------------{}'.format(response.meta))
        print self.logger.info(response.xpath('//div[@class="ip_text"]//text()').extract())
