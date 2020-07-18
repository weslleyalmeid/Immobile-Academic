# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from selenium.webdriver import Firefox
from time import sleep
from selenium.webdriver.firefox.options import Options


class CasarilSpider(scrapy.Spider):
    name = 'casaril'
    start_urls = [
        'http://www.casarilimoveis.com.br/imoveis/locacao/?tipo=Apart,Casa,Sobrado']
    page = []

    def __init__(self):
        options = Options()
        options.headless = False
        self.driver = Firefox(options= options)


    def parse(self, response):

        self.driver.get(response.url)

        response = Selector(text=self.driver.page_source.encode('utf-8'))
        
        page = response.xpath('//div[@class="pagination__pages"]/a/@href').extract()

        while page:

            self.driver.get(page[0])
            sleep(3)
            items = self.driver.find_elements_by_xpath('//a[@class="mask"]')

            urls = []
            for item in items:
                self.log(
                    '########################## OBTENDO ITEMS #################################')
                url = item.get_attribute('href')
                urls.append(url)

            for url in urls:
                self.log(
                    '########################## ACESSANDO URLS #################################')
                self.driver.get(url)
                sleep(3)
                response = Selector(text=self.driver.page_source.encode('utf-8'))

                cidade = 'Francisco Beltrao'
                bairro = response.xpath(
                    '//ul[@class="habitation__specs-list"]/li[contains(text(), "Bairro")]/text()').extract_first()
                comodos = response.xpath(
                    '//strong[text()="Cômodos:"]/parent::div/text()').extract_first()
                garagem = response.xpath(
                    '//p/strong[contains(text(), "Observa")]/parent::p/text()')[-1].get()
                suites = response.xpath(
                    '//li[contains(text(), "Suite")]/text()').extract_first()
                quartos = response.xpath(
                    '//li[contains(text(), "dormito")]/text()').extract_first()
                metragem = response.xpath(
                    '//li[contains(text(), "Metragem")]/text()').extract_first()
                banheiro = response.xpath(
                    '//li[contains(text(), "Wc")]/text()').extract_first()
                preco = response.xpath(
                    '//li[@class="is-featured"]/text()').extract_first()

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

            self.log('&&&&&&&&&&&&&&&&&&&&&&&&&&& mudou de página &&&&&&&&&&&&&&&&&&&&&&&&&')
            page.pop(0)
