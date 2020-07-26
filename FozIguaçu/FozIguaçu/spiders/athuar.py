import scrapy
from urllib.parse import urljoin


CONT = 1
class AthuarSpider(scrapy.Spider):
    name = 'athuar'
    # start_urls = ['http://www.athuarimoveis.com.br/resultado-busca.asp?busca=1#detalhes/']

    # def start_requests(self):
    #     # apto=4, casa=3, kitnet=27, sobrado=12
    #     # categories = ['4', '3', '27', '12']
    #     categories = ['4', '3']
    #     # categories = ['4']
    #     # categories = ['3']
    #     # categories = ['27']
    #     # categories = ['12']

    #     for category in categories:
    #         url='http://www.athuarimoveis.com.br/resultado-busca.asp?busca=1'
    #         global CONT
    #         CONT = 1
    #         formdata ={
    #             'cat1': '2',
    #             'cat3': category,
    #             'cidade': '5137',
    #             'valor': '0',
    #             'cod': ''
    #         }
    #         yield scrapy.FormRequest(url= url, callback=self.parse, formdata=formdata, method='POST')

    def start_requests(self):
        # apto=4, casa=3, kitnet=27, sobrado=12
        # categories = ['4', '3', '27', '12']

        url = [
            'http://www.athuarimoveis.com.br/resultado-busca.asp?busca=1',
            'http://www.athuarimoveis.com.br/resultado-busca.asp?busca=1',
            'http://www.athuarimoveis.com.br/resultado-busca.asp?busca=1',
            'http://www.athuarimoveis.com.br/resultado-busca.asp?busca=1'
        ]

        apto ={
                'cat1': '2',
                'cat3': '4',
                'cidade': '5137',
                'valor': '0',
                'cod': ''
            }

        casa ={
                'cat1': '2',
                'cat3': '3',
                'cidade': '5137',
                'valor': '0',
                'cod': ''
            }

        kit ={
                'cat1': '2',
                'cat3': '27',
                'cidade': '5137',
                'valor': '0',
                'cod': ''
            }

        sob ={
                'cat1': '2',
                'cat3': '12',
                'cidade': '5137',
                'valor': '0',
                'cod': ''
            }

        items = {}
        items.update(pos1 = [url[0], apto])
        items.update(pos2 = [url[1], casa])
        items.update(pos3 = [url[2], kit])
        items.update(pos4 = [url[3], sob])

        for item in items:
            global CONT
            CONT = 1
            yield scrapy.FormRequest(url=items[item][0], callback=self.parse, formdata=items[item][1], method='POST')

    def parse(self, response):
        items = response.xpath('//img[@class="image"]/parent::a')

        for item in items:
            url_item = item.xpath('./@href').extract_first()
            self.log(f'############# {url_item} ##################')
            # yield scrapy.Request(url=url_item, callback=self.parse_detail)

        # global CONT
        # next_page = response.xpath(f'//a[@data-ix="passar-pagians"][contains(text(), "{CONT + 1}")]')

        # if next_page:
        #     relative_url = next_page.xpath('./@href').get()
        #     base_url = 'http://www.athuarimoveis.com.br/'
        #     next_url = urljoin(base_url, relative_url)
        #     CONT += 1
        #     yield scrapy.Request(url= next_url, callback= self.parse)

        self.log('\n\n\n')
    def parse_detail(self, response):

        cidade = 'Foz Do Iguacu'
        bairro = response.xpath('//h3[contains(text(), "Endereço")]/following-sibling::div[1]/text()').get()
        comodos = ''
        garagem = response.xpath('//div[contains(text(), "Garagem Coberta")]/parent::div/following-sibling::div/div/text()').get()
        if garagem is None:
            garagem = response.xpath('//div[contains(text(), "Garagem Des")]/parent::div/following-sibling::div/div/text()').get()

        suites = response.xpath('//div[contains(text(), "Suite")]/parent::div/following-sibling::div/div/text()').get()
        quartos = response.xpath('//div[contains(text(), "Quartos")]/parent::div/following-sibling::div/div/text()').get()
      
        metragem = response.xpath('//div[@class="div-block-detalhes-3"]//\
            div[contains(text(), "Área Total")]/parent::div/following-sibling::div/div/text()').get()
        if metragem is None:
            metragem = response.xpath('//div[@class="div-block-detalhes-3"]//\
            div[contains(text(), "Área Út")]/parent::div/following-sibling::div/div/text()').get()
            
            if metragem is None:
                metragem = response.xpath('//div[@class="div-block-detalhes-3"]//\
                div[contains(text(), "Área Pri")]/parent::div/following-sibling::div/div/text()').get()
            
        banheiro = response.xpath('//div[contains(text(), "Banheiros")]/parent::div/following-sibling::div/div/text()').get()
        preco = response.xpath('//div[contains(text(), "Valor")]/span/text()').get()


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
