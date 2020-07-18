# -*- coding: utf-8 -*-
# from scrapy.http import FormRequest
import scrapy


class BelamoradaSpider(scrapy.Spider):
    name = 'belamorada'

    def start_requests(self):
        url='http://imobiliariabelamorada.com.br/filtro/locacao/apartamentos/pato-branco-pr/?busca=1'
        formdata={
            'cat1': '2.locacao', 
            'cat3': '4.apartamentos', 
            'cidade': '5362.pato-branco-pr', 
            'valor':'', 
            'cod':''
        }
        yield scrapy.FormRequest(url, callback=self.parse, formdata=formdata, method='POST')

    def parse(self, response):
        items = response.xpath('//img[@class="image"]/parent::a')

        for item in items:
            url = item.xpath('./@href').extract_first()
            # self.log(f'############# {url} ##################')
            yield scrapy.Request(url=url, callback=self.parse_detail)

    
    def parse_detail(self, response):

        #TODO detalhes
        bairro = response.xpath('//div[@id="detalhes"]/div[@class="heading-2"]/text()').get()
        
        comodos = response.xpath('//div[@class="w-row"]/div/div[contains(text(), "Comodos")]\
                                    /parent::div/following-sibling::div/div/text()').get()
        
    

        quartos = response.xpath('//div[@class="w-row"]/div/div[contains(text(), "Quartos")]\
                                    /parent::div/following-sibling::div/div/text()').get()

        try:
            metragem = response.xpath(
                '//div[@class="w-row"]/div/div[contains(text(), "Área Total")]\
                    /parent::div/following-sibling::div/div/text()').get()
        except:
            metragem = response.xpath(
                '//div[@class="w-row"]/div/div[contains(text(), "Área Construída")]\
                    /parent::div/following-sibling::div/div/text()').get()

        banheiro = response.xpath('//div[contains(text(), "Banheiro")]/\
                                    parent::div/following-sibling::div/div/text()').get()

        try:
            suites = response.xpath('//div[contains(text(), "Suites")]/\
                                    parent::div/following-sibling::div/div/text()').get()
        except:
            suites = 0

        preco = response.xpath('//div[contains(text(), "Valor Locação:")]/span/text()').get()
        
        try:
            garagem = response.xpath('//div[contains(text(), "Garagem")]\
                    /parent::div/following-sibling::div/div/text()').get()
        except:
            garagem = 0

        cidade = 'Pato Branco'

        yield{
            'bairro': bairro,
            'comodos': comodos,
            'garagem': garagem,
            'suites': suites,
            'quartos': quartos,
            'metragem': metragem,
            'banheiro': banheiro,
            'preco': preco,
            'cidade': cidade
        }
