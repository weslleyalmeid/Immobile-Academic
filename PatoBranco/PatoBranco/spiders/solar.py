# -*- coding: utf-8 -*-
import scrapy


class SolarSpider(scrapy.Spider):
    name = 'solar'
    start_urls = [
        'https://solar.imb.br/locacao/locacao-apartamentos/',
        'https://solar.imb.br/locacao/locacao-casas'
        ]

    def parse(self, response):
        items = response.xpath('//div[@class="item-image"]/a')

        for item in items:
            url = item.xpath('./@href').extract_first()
            # self.log(f'########################## {url} ########################')
            yield scrapy.Request(url= url, callback=self.parse_detail)

        #TODO next page
        next_page = response.css('a[title="Próximo"]::attr(href)')

        if next_page:
            yield scrapy.Request(url= next_page.extract_first(), callback= self.parse)

        

    def parse_detail(self, response):

        #TODO detalhes
        bairro = response.xpath('//td[contains(text(), "Apartamento:")]/following-sibling::td/text()').extract_first()
        comodos = response.xpath('//strong[text()="Cômodos:"]/parent::div/text()').extract_first()
        
        try:
            garagem = response.xpath('//td[contains(text(), "Vagas")]/following-sibling::td/text()')[1].get()
        except:
            garagem = 0

        
        suites = response.xpath('//td[contains(text(), "Dormitório")]/following-sibling::td/text()')[1].get()
        quartos = response.xpath('//td[contains(text(), "Dormitório")]/following-sibling::td/text()')[1].get()
        try:
            metragem = response.xpath('//td[contains(text(), "Área Útil")]/following-sibling::td/text()')[1].get()
        except:
            metragem = '70 M²'
        banheiro = response.xpath('//td[contains(text(), "Banheiro")]/following-sibling::td/text()')[1].get()
        preco = response.xpath('//td[contains(text(), "Valor de Locação")]/following-sibling::td/b/text()').get()
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