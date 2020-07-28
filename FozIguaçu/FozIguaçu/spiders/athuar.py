import scrapy
from urllib.parse import urljoin

""" 
    Ao percorrer a lista de categorias, de alguma maneira o percorre todas as páginas
    de forma paralela, como o url é o mesmo e só muda o form, de alguma maneira o response
    não avança as páginas seguintes, avançando apenas em uma das categorias.
    Como não consegui resolver, vou executar a extração mudando apenas os elementos categories
"""
CONT = 1
class AthuarSpider(scrapy.Spider):
    name = 'athuar'
    # start_urls = ['http://www.athuarimoveis.com.br/resultado-busca.asp?busca=1#detalhes/']

    def start_requests(self):
        # apto=4, casa=3, kitnet=27, sobrado=12
        # categories = ['4', '3', '27', '12']
        # categories = ['4']
        # categories = ['3']
        # categories = ['27']
        categories = ['12']

        for category in categories:
            url='http://www.athuarimoveis.com.br/resultado-busca.asp?busca=1'

            formdata ={
                'cat1': '2',
                'cat3': category,
                'cidade': '5137',
                'valor': '0',
                'cod': ''
            }
            yield scrapy.FormRequest(url= url, callback=self.parse, formdata=formdata, method='POST')

    def parse(self, response):

        # self.log(f'\n\n\n AQUI {response.url}')
        items = response.xpath('//img[@class="image"]/parent::a')

        for item in items:
            url_item = item.xpath('./@href').extract_first()
            # self.log(f'############# {url_item} ##################')
            yield scrapy.Request(url=url_item, callback=self.parse_detail)

        next_page = response.xpath(f'//a[@data-ix="passar-pagians"]/b/parent::a/following-sibling::a')

        if next_page:
            relative_url = next_page.xpath('./@href').get()
            base_url = 'http://www.athuarimoveis.com.br/'
            next_url = urljoin(base_url, relative_url)
            yield scrapy.Request(url= next_url, callback= self.parse)

        
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
