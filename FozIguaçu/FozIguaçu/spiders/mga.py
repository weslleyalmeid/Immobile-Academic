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
            # self.log(next_url)
            yield scrapy.Request(url= next_url, callback= self.parse_detail)

        next_page = response.css('a.btn-next')

        if next_page:
            relative_url = next_page.css('a::attr(href)').get()
            base_url = 'https://www.mgaimobiliaria.com.br'
            next_url = urljoin(base_url, relative_url)
            yield scrapy.Request(url= next_url, callback=self.parse)

    def parse_detail(self, response):

        cidade = 'Foz Do Iguacu'
        bairro = response.css('span.first-line + span::text').get()
        comodos = ''
        garagem = response.css('i.ga-garage-03 + span::text').get()
        suites = response.css('i.ga-bathroom-03 + span::text').get()
        quartos = response.css('i.ga-bedrooms-02 + span::text').get()
        metragem = response.css('i.ga-ruler-02 + span::text').get()
        banheiro = response.css('i.ga-bathroom-04 + span::text').get()
        preco = response.xpath('//p[@class=("total-price" or "price")]/span[last()]/text()').get()


        yield{
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