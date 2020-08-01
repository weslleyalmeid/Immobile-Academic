import scrapy
from scrapy.selector import Selector
from selenium.webdriver import Firefox
from time import sleep
from selenium.webdriver.firefox.options import Options

class ZapSpider(scrapy.Spider):
    name = 'zap'
    start_urls = ['https://www.zapimoveis.com.br/aluguel/apartamentos/pr+cascavel/?pagina=1&onde=,Paran%C3%A1,Cascavel,,,,BR%3EParana%3ENULL%3ECascavel,-24.9577771,-53.45951119999999&transacao=Aluguel&tipo=Im%C3%B3vel%20usado&tipoUnidade=Residencial,Apartamento']

    def __init__(self):
        options = Options()
        options.headless = False
        self.driver = Firefox(options= options)
        self.browser = Firefox(options= options)
        for url in self.start_urls:
            self.driver.get(url)
            self.driver.get(url)
            sleep(2)
        
        # import ipdb; ipdb.set_trace()

    def parse(self, response):
        # response = Selector(text=self.driver.page_source.encode('utf-8'))

        window_before = driver.window_handles[0]
        items = self.driver.find_elements_by_css_selector('div.simple-card__box')

        # import ipdb; ipdb.set_trace()
        for item in items:
            self.log('################# OBTENDO ITEMS ########################')
            item.click()
            sleep(3)
            url = self.driver.current_url
            driver.back()
            import ipdb; ipdb.set_trace()
            self.log(url)
            yield scrapy.Request(url=url, callback=self.parse_detail)
        
    def parse_detail(self, response):
        # import ipdb; ipdb.set_trace()

        cidade = 'Cascavel'
        bairro = response.css('span.link::text').get()
        comodos = ''
        garagem = response.css('li.js-parking-spaces span + span::text').get()
        suites = ''
        quartos = response.css('li.js-bedrooms span + span::text').get()
        metragem = response.css('li.js-areas span + span::text').get()
        banheiro = response.css('li.js-bathrooms span + span::text').get()
        preco = response.css('li.price__item--main  strong::text').get()
        # ipdb.set_trace()
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
