import scrapy

CONT = 1

class TomazoniSpider(scrapy.Spider):
    name = 'tomazoni'    

    def start_requests(self):
        url = 'http://tomazoni.com.br/filtro/locacao/apartamentos/undefined/todos-bairros/?busca=1'

        form_data = {
            'busca': '1',
            'cat1': ' 2.locacao',
            'cat3': '4.apartamentos',
            'cidade': '',
            'bairro': '',
            'valormedio': ''
        }

        yield scrapy.FormRequest(url, callback=self.parse, method='POST', formdata=form_data)
        
        # scrapy.FormRequest(url, method='POST', formdata=form_data)
        # response.xpath('//a[@class="link-block-2 w-inline-block"]/@href')

    def parse(self, response):
        items = response.xpath('//a[@class="link-block-2 w-inline-block"]')

        for item in items:
            url = item.xpath('./@href').extract_first()
            form_data = {
                'busca': '1',
                'cat1': ' 2.locacao',
                'cat3': '4.apartamentos',
                'cidade': '',
                'bairro': '',
                'valormedio': ''
            }
            yield scrapy.Request(url=url, callback=self.parse_detail)

        #TODO next page
        next_page = response.xpath('//a[@data-ix="passar-pagians"]/@href').extract()
        
        global CONT
        page = f'?p={CONT + 1}'

        try:
            if next_page[CONT] == page:
                next_url = f'http://tomazoni.com.br/filtro/locacao/apartamentos/undefined/todos-bairros/?p={CONT + 1}'
                CONT += 1
                yield scrapy.Request(url= next_url, callback= self.parse)
        
        except:
            pass

    def parse_detail(self, response):

        cidade = 'Francisco Beltrao'
        bairro = response.xpath('//span[contains(text(), "Ref")]/parent::div/text()').get()
        comodos = response.xpath('//div[contains(text(), "Comodos")]/preceding-sibling::div/text()').get()
        garagem = response.xpath('//div[contains(text(), "Garagem")]/preceding-sibling::div/text()').get()
        suites = response.xpath('//div[contains(text(), "Suite")]/preceding-sibling::div/text()').get()
        quartos = response.xpath('//div[contains(text(), "Quarto")]/preceding-sibling::div/text()').get()
        metragem = response.xpath('//div[contains(text(), "Área Construída")]/preceding-sibling::div/text()').get()
        banheiro = response.xpath('//div[contains(text(), "Banheiro")]/preceding-sibling::div/text()').get()
        preco = response.xpath('//span[contains(text(), "Valor Líquido:")]/parent::div/text()').get()

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