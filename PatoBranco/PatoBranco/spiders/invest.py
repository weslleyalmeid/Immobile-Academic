# -*- coding: utf-8 -*-
import scrapy


class InvestSpider(scrapy.Spider):
    name = 'invest'
    start_urls = [
        'http://www.investimoveispatobranco.com.br/filtro/locacao/apartamentos/pato-branco/todos/todos/todos/1/lin/1/',
        'http://www.investimoveispatobranco.com.br/filtro/locacao/casas/pato-branco/todos/todos/todos/1/lin/1'
        ]

    def parse(self, response):
        items = response.xpath('//div[@class="div-block-31"]/a')

        for item in items:
            url = item.xpath('./@href').extract_first()
            self.log(url)
            yield scrapy.Request(url=url, callback=self.parse_detail)

        

    def parse_detail(self, response):

        #TODO detalhes
        bairro = response.css('#detalhes::text').extract_first()
        comodos =  response.xpath('//div[contains(text(), "Comodos")]/following-sibling::div/text()').extract_first()
        garagem =  response.xpath('//div[contains(text(), "Garagem")]/following-sibling::div/text()').extract_first()
        suites = response.xpath('//div[contains(text(), "Suites")]/following-sibling::div/text()').extract_first()
        quartos = response.xpath('//div[contains(text(), "Quarto")]/following-sibling::div/text()').extract_first()
        metragem = response.xpath('//div[contains(text(), "Área Construída")]/following-sibling::div/text()').extract_first()
        banheiro = response.xpath('//div[contains(text(), "Banheiros")]/following-sibling::div/text()').extract_first()
        preco = response.xpath('//div[contains(text(), "Valor")]/span/text()').extract_first()
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