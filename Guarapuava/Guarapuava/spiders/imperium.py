import scrapy


class ImperiumSpider(scrapy.Spider):
    name = 'imperium'

    def start_requests(self):
        url = ['https://www.imperiumimoveis.com.br/busca?operacao=locacao&tipo-\
    imovel=6&cidade=45&bairro=&valor-min=&valor-max=&area-min=&area-max=&garagens=&dormitorios=']
        formdata={
            'operacao': 'locacao',
            'tipo-imovel': '6',
            'cidade': '45',
            'bairro': '',
            'valor-min': '',
            'valor-max': '',
            'area-min': '',
            'area-max': '',
            'garagens': '',
            'dormitorios': '',
            'page': '2'
        }
        yield scrapy.FormRequest(url, callback=self.parse, formdata=formdata, method='POST')

    def parse(self, response):
        # items = response.xpath('//div[@class="info hidden-xs"]/a[@class="detalhe-link"]')

        # for item in items:
        #     url = item.xpath('./@href').get()
        #     # self.log(url)
        #     yield scrapy.Request(url= url, callback= self.parse_detail)

        next_page = response.xpath('//a[@rel="next"]/@href')
        if next_page:

            url = f'https://www.imperiumimoveis.com.br{next_page.extract_first()}'
            self.log(' ########################## MUDOU ###############################')
            yield scrapy.Request(url, callback=self.parse, dont_filter=False)


    def parse_detail(self, response):

        cidade = 'Guarapuava'
        bairro = response.xpath('//div[@id="informacao"]/span[contains(text(), "Bairro")]/span/text()').get()
        comodos = ''
        garagem = response.css('.detalhe-garagem::text').get()
        suites = response.css('.detalhe-quarto::text').get()
        quartos = response.css('.detalhe-quarto::text').get() 
        metragem = response.xpath('//span[contains(text(), "Área Útil")]/text()').get()
        banheiro = response.css('.detalhe-banheiro::text').get()
        preco = response.xpath('//span[@class="detalhe-item"][contains(text(), "Aluguel")]/span/text()').get()

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
