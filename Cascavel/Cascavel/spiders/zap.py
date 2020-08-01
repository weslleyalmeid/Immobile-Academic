import scrapy


class ZapSpider(scrapy.Spider):
    name = 'zap'
    start_urls = ['https://www.zapimoveis.com.br/aluguel/apartamentos/pr+cascavel/?pagina=1&onde=,Paran%C3%A1,Cascavel,,,,BR%3EParana%3ENULL%3ECascavel,-24.9577771,-53.45951119999999&transacao=Aluguel&tipo=Im%C3%B3vel%20usado&tipoUnidade=Residencial,Apartamento']

    def parse(self, response):

        items = response.css('div.ui__card a')
        for item in items:
            self.log('################# OBTENDO ITEMS ########################')
            relative_url = item.css('a::attr(href)').get()
            base_url = 'https://www.lokatell.com.br'
            url = urljoin(base_url, relative_url)
            self.log(url)
            yield scrapy.Request(url=url, callback=self.parse_detail)
        
    def parse_detail(self, response):

        cidade = 'Cascavel'
        bairro = response.css('div.card__address::text').get()
        comodos = ''
        garagem = response.xpath('//div[contains(@class, "card__infos")]//img[@alt="garagem icone"]/parent::div/text() [2]').get()
        suites = response.xpath('//div[contains(@class, "card__infos")]//img[@alt="suite icone"]/parent::div/text() [2]').get()
        quartos = response.xpath('//div[contains(@class, "card__infos")]//img[@alt="quarto icone"]/parent::div/text() [2]').get()
        metragem = response.xpath('//div[contains(@class, "card__infos")]//img[@alt="area icone"]/parent::div/text() [2]').get()
        banheiro = response.xpath('//div[contains(@class, "card__infos")]//img[@alt="banheiro icone"]/parent::div/text() [2]').get()
        preco = response.xpath('//span[contains(text(), "Aluguel")]/following-sibling::span/text()').get()
        
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
