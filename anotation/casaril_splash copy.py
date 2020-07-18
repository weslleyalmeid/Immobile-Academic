# -*- coding: utf-8 -*-
from scrapy_splash import SplashRequest
import scrapy


class CasarilSpider(scrapy.Spider):
    name = 'casaril'
    start_urls = ['http://www.casarilimoveis.com.br/imoveis/locacao/?tipo=Apart,Casa,Sobrado/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse, args= {"wait": 1})

    def parse(self, response):
        items = response.xpath('//a[@class="mask"]')
        for item in items:
            self.log('###########################################################')
            url = item.xpath('./@href').extract_first()
            # yield scrapy.Request(url= url, callback=self.parse_detail)

        # #TODO next page
        # next_page = response.xpath('//li[@class="roundright"]/a/@href')

        # if next_page:
        #     yield scrapy.Request(url= next_page.extract_first(), callback= self.parse)

        

    # def parse_detail(self, response):

    #     #TODO detalhes
    #     bairro = response.xpath('//strong[text()="Bairro:"]/following-sibling::a/text()').extract_first()
    #     comodos = response.xpath('//strong[text()="Cômodos:"]/parent::div/text()').extract_first()
    #     garagem = response.xpath('//strong[text()="Vagas de Garagam:"]/parent::div/text()').extract_first()
    #     suites = response.xpath('//strong[text()="Número de Suítes:"]/parent::div/text()').extract_first()
    #     quartos = response.xpath('//strong[text()="Quartos:"]/parent::div/text()').extract_first()
    #     metragem = response.xpath('//strong[text()="Metragem:"]/parent::div/text()').extract_first()
    #     banheiro = response.xpath('//strong[text()="Banheiros:"]/parent::div/text()').extract_first()
    #     preco = response.xpath('//strong[text()="Preço:"]/parent::div/text()').extract_first()

    #     yield{
    #         'bairro': bairro,
    #         'comodos': comodos,
    #         'garagem': garagem,
    #         'suites': suites,
    #         'quartos': quartos,
    #         'metragem': metragem,
    #         'banheiro': banheiro,
    #         'preco': preco
    #     }
