import scrapy
from urllib.parse import urljoin


class LeloSpider(scrapy.Spider):
    name = 'lelo'

    start_urls = ['https://leloimoveis.com.br/imoveis/casa-residencial-apartamento-kitinet-sobrado-locacao']

    def parse(self, response):
        
        items = response.xpath('//a[@class="list__card-link"]')
        
        for item in items:
            url = item.xpath('./@href').get()
            self.log(url)

    def parse_detail(self, response):
        # import ipdb; ipdb.set_trace()
        cidade = 'Maringa'
        bairro = response.xpath('//h3/a [last()]/text()').get()
        comodos = ''
        # garagem = response.xpath('//div[@class="card__cps-label"][contains(text(),"Garagem")]/following-sibling::div/text()').get()
        # suites = response.xpath('//div[@class="card__cps-label"][contains(text(),"Suíte")]/following-sibling::div/text()').get()
        # quartos = response.xpath('//div[@class="card__cps-label"][contains(text(),"Quartos")]/following-sibling::div/text()').get()
        # metragem = response.css('p.card__highlights::text').get()
        # banheiro = response.xpath('//div[@class="card__cps-label"][contains(text(),"BWC Social")]/following-sibling::div/text()').get()
        # preco = response.css('dd.card__price-value::text').get()
        # import ipdb; ipdb.set_trace()
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
