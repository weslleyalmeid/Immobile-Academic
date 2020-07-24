import scrapy
from urllib.parse import urljoin


class GralhaazulSpider(scrapy.Spider):
    name = 'gralhaazul'

    start_urls = ['http://www.imobiliariagralhaazul.com.br/imoveis/para-alugar/apartamento+casa+sobrado']

    def parse(self, response):
        items = response.css('div.card-listing > a')

        for item in items:
            base_url = 'http://www.imobiliariagralhaazul.com.br'
            relative_url =item.css('a::attr(href)').get()
            url = urljoin(base_url, relative_url)
            # self.log(url)
            yield scrapy.Request(url= url, callback= self.parse_detail)

        next_page = response.css('a.btn-next::attr(href)').get()

        if next_page:
            base_url = 'http://www.imobiliariagralhaazul.com.br'
            url = urljoin(base_url, next_page)
            # self.log('############' + url + '##################')
            yield scrapy.Request(url= url, callback=self.parse, dont_filter=False)


    def parse_detail(self, response):

        cidade = 'Guarapuava'
        bairro = response.css('span.first-line + span::text').get()
        comodos = ''
        garagem = response.css('i.ga-garage-03 + span::text').get()
        suites = response.css('i.ga-bathroom-03 + span::text').get()
        quartos = response.css('i.ga-bedrooms-02 + span::text').get()
        metragem = response.css('i.ga-ruler-02 + span::text').get()
        banheiro = response.css('i.ga-bathroom-04 + span::text').get()
        preco = response.css('p.price span:last-child::text').get()
        if preco is None:
            preco = response.css('p.total-price span:last-child::text').get()

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
