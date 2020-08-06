from selenium.webdriver.firefox.options import Options
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import Firefox, Chrome
from scrapy.selector import Selector
from urllib.parse import urljoin
from time import sleep
import scrapy




class ImovelwebSpider(scrapy.Spider):
    name = 'imovelweb'
    start_urls = ['https://www.imovelweb.com.br/apartamentos-aluguel-cascavel-pr.html']

    def __init__(self):
        options = Options()
        options.headless = False
        # self.driver = Firefox(options= options)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = Chrome(options)

    def start_requests(self):
        url = self.start_urls[0]
        yield SeleniumRequest(url=url, callback=self.parse, wait_time= 3)


    def parse(self, response):
        items = response.css('a.go-to-posting')
        
        for item in items:
            relative_url = item.css('a::attr(href)').get()
            base_url = 'https://www.imovelweb.com.br/'
            url = urljoin(base_url, relative_url)
            self.log(url)
            self.driver.get(url)
            sleep(7)
            response = Selector(text= self.driver.page_source.encode('utf-8'))
            yield self.parse_detail(response)
            

    def parse_detail(self, response):
        

        cidade = 'Cascavel'
        bairro = response.css('.title-location > span::text').get()
        comodos = ''
        garagem = response.xpath('//i[contains(@class, "icon-f-cochera")]/parent::li/b/text()').get()
        suites = response.xpath('//i[contains(@class, "icon-f-toilete")]/parent::li/b/text()').get()
        quartos = response.xpath('//i[contains(@class, "icon-f-dormitorio")]/parent::li/b/text()').get()
        metragem = response.xpath('//i[contains(@class, "icon-f-scubierta")]/parent::li/b/text()').get()
        if metragem is None:
            metragem = response.xpath('//i[contains(@class, "icon-f-stotal")]/parent::li/b/text()').get()
        banheiro = response.xpath('//i[contains(@class, "icon-f-bano")]/parent::li/b/text()').get()
        preco = response.xpath('//div[contains(text(), "Aluguel")]/following-sibling::div/span/text()').get()
        
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
