from scrapy_selenium import SeleniumRequest
from urllib.parse import urljoin
import scrapy



class ImovelwebSpider(scrapy.Spider):
    name = 'imovelweb'
    start_urls = ['https://www.imovelweb.com.br/apartamentos-aluguel-cascavel-pr.html']


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
            scrapy.Request(url= url, callback= self.parse_detail)
            

    def parse_detail(self, response):
        import ipdb; ipdb.set_trace()

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
