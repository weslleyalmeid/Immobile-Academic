# -*- coding: utf-8 -*-
import scrapy


class MorettiSpider(scrapy.Spider):
    name = 'moretti'
    start_urls = [
                    'https://www.moretti.imb.br/locacao/apartamentos//',
                    'https://www.moretti.imb.br/locacao/casas/'
                ]

    def parse(self, response):
        items = response.xpath(
            '//div[@class="col-md-12 has_prop_slider  listing_wrapper property_unit_type2"]')

        for item in items:
            url = item.xpath('./@data-modal-link').extract_first()
            yield scrapy.Request(url= url, callback=self.parse_detail)

        #TODO next page
        next_page = response.xpath('//li[@class="roundright"]/a/@href')

        if next_page:
            yield scrapy.Request(url= next_page.extract_first(), callback= self.parse)

        

    def parse_detail(self, response):

        #TODO detalhes
        bairro = response.xpath('//strong[text()="Bairro:"]/following-sibling::a/text()').extract_first()
        comodos = response.xpath('//strong[text()="Cômodos:"]/parent::div/text()').extract_first()
        garagem = response.xpath('//strong[text()="Vagas de Garagam:"]/parent::div/text()').extract_first()
        suites = response.xpath('//strong[text()="Número de Suítes:"]/parent::div/text()').extract_first()
        quartos = response.xpath('//strong[text()="Quartos:"]/parent::div/text()').extract_first()
        metragem = response.xpath('//strong[text()="Metragem:"]/parent::div/text()').extract_first()
        banheiro = response.xpath('//strong[text()="Banheiros:"]/parent::div/text()').extract_first()
        preco = response.xpath('//strong[text()="Preço:"]/parent::div/text()').extract_first()
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