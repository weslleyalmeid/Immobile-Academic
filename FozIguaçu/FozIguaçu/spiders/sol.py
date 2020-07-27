import scrapy
from scrapy_splash import SplashRequest
# debugg
# import ipdb; ipdb.set_trace()

class SolSpider(scrapy.Spider):
    name = 'sol'

    start_urls = ['https://www.solimoveis.com.br/aluguel/apartamento--casa--sobrado/foz-do-iguacu/todos-os-bairros/0-quartos/0-suite-ou-mais/0-vaga/0-banheiro-ou-mais?valorminimo=0&valormaximo=0&pagina={NUM}'.format(NUM=x) for x in range(1,6)]
    # import ipdb; ipdb.set_trace()

    

    def start_requests(self):

        for url in self.start_urls:
            yield SplashRequest(
                url= url,
                callback= self.parse,
                endpoint='render.html',
                args={'wait': 10}
            )


    def parse(self, response):
        items = response.css('div.property-content > a')

        for item in items:
            url =item.css('a::attr(href)').get()
            # self.log(url)
            yield scrapy.Request(url= url, callback= self.parse_detail)

    def parse_detail(self, response):

        cidade = 'Foz Do Iguacu'
        bairro = response.css('div.pull-left h1::text').get()
        comodos = ''
        garagem = response.xpath('//div[@class="row"]//i[@class="flaticon-vehicle"]/parent::li/text() [last()]').get()
        suites = response.xpath('//div[@class="row"]//li[contains(., "Suíte")]/text() [last()]').get()
        quartos = response.xpath('//div[@class="row"]//i[@class="flaticon-bed"]/parent::li/text() [last()]').get()
        metragem = response.xpath('//div[@class="row"]//li[contains(., "Privativo")]/text() [last()]').get()
        banheiro = response.xpath('//div[@class="row"]//li[contains(., "Banheiro")]/text() [last()]').get()
        preco = response.css('div.pull-right h3 span::text').get()

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