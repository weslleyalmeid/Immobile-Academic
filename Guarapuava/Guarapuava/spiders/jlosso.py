import scrapy

CONT = 1

class JlossoSpider(scrapy.Spider):
    name = 'jlosso'

    start_urls = [
        'https://www.jlosso.com.br/filtro/locacao/apartamentos/guarapuava/todos/todos/1/1',
        'https://www.jlosso.com.br/filtro/locacao/casas/guarapuava/todos/todos/1/1',
        'https://www.jlosso.com.br/filtro/locacao/sobrados/guarapuava/todos/todos/1/1',
        'https://www.jlosso.com.br/filtro/locacao/kitinetes/guarapuava/todos/todos/1/1'
        ]

    def parse(self, response):

        items = response.xpath('//a[@class="div-block-8-update1 w-inline-block"]')
        
        for item in items:
            url = item.xpath('./@href').get()
            # self.log(url)
            yield scrapy.Request(url= url, callback= self.parse_detail)

        global CONT
        next_page = response.xpath(f'//a[@data-ix="passar-pagians"][contains(text(), "{CONT + 1}")]')

        if next_page:
            next_url = next_page.xpath('./@href').get()
            CONT += 1
            yield scrapy.Request(url= next_url, callback= self.parse)
        


    def parse_detail(self, response):

        cidade = 'Guarapuava'
        bairro = response.xpath('//div[@class="text-block-19"][contains(text(), "Bairro")]/following-sibling::div/text()').get()
        comodos = ''
        garagem = response.xpath('//div[@class="text-block-24"][contains(text(), "Garagem Co")]/preceding-sibling::div/div/text()').get()
        suites = response.xpath('//div[@class="text-block-24"][contains(text(), "Suite")]/preceding-sibling::div/div/text()').get()
        quartos = response.xpath('//div[@class="text-block-24"][contains(text(), "Quarto")]/preceding-sibling::div/div/text()').get()
        metragem = response.xpath('//div[@class="text-block-24"][contains(text(), "Área Tota")]/preceding-sibling::div/div/text()').get()
        if metragem is None:
            metragem = response.xpath('//div[@class="text-block-24"][contains(text(), "Área Con")]/preceding-sibling::div/div/text()').get()
            if metragem is None:
                metragem = response.xpath('//div[@class="text-block-24"][contains(text(), "Área Út")]/preceding-sibling::div/div/text()').get()
        
        banheiro = response.xpath('//div[@class="text-block-24"][contains(text(), "Banheiro")]/preceding-sibling::div/div/text()').get()
        preco = response.xpath('//div[@class="text-block-16"]/text()').get()

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
