import scrapy


class ImperiumSpider(scrapy.Spider):
    name = 'imperium'
    start_urls = ['https://www.imperiumimoveis.com.br/busca?operacao=locacao&tipo-\
    imovel=6&cidade=45&bairro=&valor-min=&valor-max=&area-min=&area-max=&garagens=&dormitorios=']

    def parse(self, response):
        items = response.xpath('//a[@class="card-description-new-imoveis"]')

        for item in items:
            url = item.xpath('./@href').get()
            # self.log(url)
            yield scrapy.Request(url= url, callback= self.parse_detail)

        next_page = response.xpath('//a[@rel="next"]/@href')
        if next_page:
            url = f'https://imobiliarioparana.com.br{next_page.extract_first()}'
            self.log(' ########## MUDOU ############')
            yield scrapy.Request(url, callback=self.parse)



    def parse_detail(self, response):

        cidade = 'Umuarama'
        bairro = ''
        comodos = ''
        garagem = response.xpath('//div[@id="home"]/p/text()').get()
        suites = response.xpath('//div[@id="home"]/p/text()').get()
        quartos = response.xpath('//div[@id="home"]//i[@class="fas fa-bed"]/parent::span/text()').get()
        metragem = response.xpath('//div[@id="home"]//i[@class="fas fa-ruler-horizontal"]/parent::span/text()').get()
        banheiro = response.xpath('//div[@id="home"]/p/text()').get()
        preco = response.xpath('//span[@class="strong"][contains(text(), "R$")]/text()').get()

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