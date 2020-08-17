import scrapy
from urllib.parse import urljoin


class LeloSpider(scrapy.Spider):
    name = 'lelo'

    start_urls = ['https://leloimoveis.com.br/imoveis/apartamento-locacao']

    def parse(self, response):
        
        items = response.xpath('//a[@class="list__card-link"]')
        
        for item in items:
            url = item.xpath('./@href').get()
            self.log(url)

