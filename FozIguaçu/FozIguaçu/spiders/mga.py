import scrapy
from urllib.parse import urljoin

class MgaSpider(scrapy.Spider):
    name = 'mga'
    start_urls = ['https://www.mgaimobiliaria.com.br/imoveis/para-alugar/apartamento+casa+sobrado/foz-do-iguacu/']

    def parse(self, response):
        
        items = response.css('div.card-listing > a')
        for item in items:
            relative_url = item.css('a::attr(href)').get()
            base_url = 'https://www.mgaimobiliaria.com.br'
            next_url = urljoin(base_url, relative_url)
            self.log(next_url)
            # yield scrapy.Request(url= next_url, callback= self.parse_detail)

        next_page = response.css('a.btn-next')

        if next_page:
            relative_url = next_page.css('a::attr(href)').get()
            base_url = 'https://www.mgaimobiliaria.com.br'
            next_url = urljoin(base_url, relative_url)
            yield scrapy.Request(url= next_url, callback=self.parse)