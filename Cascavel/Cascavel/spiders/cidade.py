import scrapy
from scrapy_selenium import SeleniumRequest
from urllib.parse import urljoin
import re

class CidadeSpider(scrapy.Spider):
    name = 'cidade'
    start_urls = ['https://www.imobiliariacidade.com.br/imoveis/apartamento-casa-residencial-sobrado-locacao-cascavel-pagina-1']

    def start_requests(self):
        url = self.start_urls[0]
        yield SeleniumRequest(url=url, callback=self.parse, wait_time= 3)

    def parse(self, response):
        
        items = response.css('a.list__item')

        for item in items:
            self.log('################# OBTENDO ITEMS ########################')
            relative_url = item.css('a::attr(href)').get()
            base_url = 'https://www.imobiliariacidade.com.br'
            url = urljoin(base_url, relative_url)
            yield SeleniumRequest(
                        url=url,
                        callback=self.parse_detail,
                        wait_time=2
                    )

        relative_url = response.css('a.list__next-btn::attr(href)').get()
        base_url = 'https://www.imobiliariacidade.com.br'
        next_page = urljoin(base_url, relative_url)
        if next_page:
            aux = int(re.search(r'\d+', next_page).group())
            if aux < 20:
                yield SeleniumRequest(url=next_page, callback=self.parse, wait_time= 3)


    def parse_detail(self, response):

        cidade = 'Cascavel'
        bairro = response.css('div.ficha__adress::text').get()
        comodos = ''
        garagem = response.xpath('//span[contains(.,"vagas")]/text()').get()
        suites = response.xpath('//span[contains(.,"suite")]/text()').get()
        quartos = response.xpath('//span[contains(.,"quarto")]/text()').get()
        metragem = response.xpath('//span[contains(.,"útil" ) or contains(., "total")]/text()').get()
        banheiro = response.xpath('//div[@class="jetgrid"]//div[contains(text(),"BWC" )]/following-sibling::div/text()').get()
        preco = response.css('div.ficha__valor-numero::text').get()
        
        yield {
            'cidade': cidade,
            'bairro': bairro,
            'comodos': comodos,
            'garagem': garagem,
            'suites': suites,
            'quartos': quartos,
            'metragem': metragem,
            'banheiro': banheiro,
            'preco': preco
        }
