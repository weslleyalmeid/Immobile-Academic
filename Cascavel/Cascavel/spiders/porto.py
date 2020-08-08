import scrapy


class PortoSpider(scrapy.Spider):
    name = 'porto'
    start_urls = [
        'https://www.portoseguroimobiliaria.com/filtros/locacao/apartamentos/todos/col/1',
        'https://www.portoseguroimobiliaria.com/filtros/locacao/casas/todos/col/1'
        ]


    def parse(self, response):

        items = response.css('div.div-block-21-portoseguro1')

        for item in items:
            url = item.css('a::attr(href)').get()
            # self.log(url)
            yield scrapy.Request(url=url, callback=self.parse_detail)
            # import ipdb; ipdb.set_trace()

        next_page = response.xpath('//a[@data-ix="passar-pagians"]/b/parent::a/following-sibling::a')
        if next_page:
            next_url = next_page.xpath('@href').get()
            # self.log(next_url)
            # import ipdb; ipdb.set_trace()
            yield scrapy.Request(url=next_url, callback=self.parse)
    
    def parse_detail(self, response):
        

        cidade = 'Cascavel'
        bairro = response.xpath('//div[@class="div-block-51"]//div[contains(text(), "Bairro")]/following-sibling::div/text()').get()
        comodos = ''
        garagem = response.xpath('//div[@class="div-block-53"]//div[contains(text(), "Garagem")]/preceding-sibling::div/div/text()').get() 
        suites = response.xpath('//div[@class="div-block-53"]//div[contains(text(), "Suites")]/preceding-sibling::div/div/text()').get() 
        quartos = response.xpath('//div[@class="div-block-53"]//div[contains(text(), "Quarto")]/preceding-sibling::div/div/text()').get()
        metragem = response.xpath('//div[@class="div-block-53"]//div[contains(text(), "Área Útil")]/preceding-sibling::div/div/text()').get()
        if metragem is None:
            metragem = response.xpath('//div[@class="div-block-53"]//div[contains(text(), "Área Total")]/preceding-sibling::div/div/text()').get()
        banheiro = response.xpath('//div[contains(text(), "Banheiro")]/preceding-sibling::div/div/text()').get()
        preco = response.xpath('//div[contains(text(), "Valor Locação")]/text()').get()
        
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
