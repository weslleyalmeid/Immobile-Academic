import scrapy
from urllib.parse import urljoin
from scrapy_selenium import SeleniumRequest


class LokatellSpider(scrapy.Spider):
    name = 'lokatell'
    start_urls = ['https://www.lokatell.com.br/imoveis/casa-residencial-apartamento-kitinete-sobrado-locacao-cascavel-pagina-{NUM}?ord=imovelvalor&ascdesc=desc'.format(NUM=x) for x in range(1,11)]

    def parse(self, response):

        items = response.css('div.ui__card a')
        for item in items:
            self.log('################# OBTENDO ITEMS ########################')
            relative_url = item.css('a::attr(href)').get()
            base_url = 'https://www.lokatell.com.br'
            url = urljoin(base_url, relative_url)
            self.log(url)
            yield scrapy.Request(url=url, callback=self.parse_detail)
        
    def parse_detail(self, response):

        cidade = 'Cascavel'
        bairro = response.css('div.card__address::text').get()
        comodos = ''
        garagem = response.xpath('//div[contains(@class, "card__infos")]//img[@alt="garagem icone"]/parent::div/text() [2]').get()
        suites = response.xpath('//div[contains(@class, "card__infos")]//img[@alt="suite icone"]/parent::div/text() [2]').get()
        quartos = response.xpath('//div[contains(@class, "card__infos")]//img[@alt="quarto icone"]/parent::div/text() [2]').get()
        metragem = response.xpath('//div[contains(@class, "card__infos")]//img[@alt="area icone"]/parent::div/text() [2]').get()
        banheiro = response.xpath('//div[contains(@class, "card__infos")]//img[@alt="banheiro icone"]/parent::div/text() [2]').get()
        preco = response.xpath('//span[contains(text(), "Aluguel")]/following-sibling::span/text()').get()
        
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
