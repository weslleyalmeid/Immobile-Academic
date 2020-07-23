import scrapy


class FaaxSpider(scrapy.Spider):
    name = 'faax'

    def start_requests(self):
        
        url = 'https://www.faax.com.br/filtro/locacao/kitinetes--sobrados--apartamentos--casas/guarapuava/todos/todos/1/col/1/DESC'
        form_data = {
            'cat1': '2.locacao',
            'cat3': 'kitinetes--sobrados--apartamentos--casas',
            'cat3select': '3',
            'cat3select': '4',
            'cat3select': '12',
            'cat3select': '27',
            'cidade': '5166.guarapuava',
            'bairro': '',
            'valormedio': '',
            'codigo':''
        }
        yield scrapy.FormRequest(
                        url=url,
                        callback=self.parse,
                        formdata=form_data,
                        method='POST',
                        meta= {'dont_obey_robotstxt':'False'}
                    )

    def parse(self, response):
        
        items = response.xpath('//a[@class="link-block w-inline-block"]')
        
        for item in items:
            url = item.xpath('./@href').get()
            self.log(url)
            yield scrapy.Request(url= url, callback= self.parse_detail)

        next_page = response.xpath('//a[@class="link-10 left w-button"]/@href')
        if next_page:

            url = next_page.extract_first()
            yield scrapy.Request(url, callback=self.parse, dont_filter=False)


    def parse_detail(self, response):

        cidade = 'Guarapuava'
        bairro = response.css('h1.heading-5::text').get()
        comodos = ''
        garagem = response.xpath('//div[contains(text(), "Garagem Coberta")]/preceding-sibling::div/text()').get()
        suites = response.xpath('//div[contains(text(), "Suite")]/preceding-sibling::div/text()').get()
        quartos = response.xpath('//div[contains(text(), "Quarto")]/preceding-sibling::div/text()').get()
        metragem = response.xpath('//div[contains(text(), "Área Útil")]/preceding-sibling::div/text()').get()
        if metragem is None:
            metragem = response.xpath('//div[contains(text(), "Área Total")]/preceding-sibling::div/text()').get()
        banheiro = response.xpath('//div[contains(text(), "Banheiro")]/preceding-sibling::div/text()').get()
        preco = response.xpath('//div[@class="text-block-34"]/p/text()').extract_first()

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