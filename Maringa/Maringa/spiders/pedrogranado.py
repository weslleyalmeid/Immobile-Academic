import scrapy


class PedrogranadoSpider(scrapy.Spider):
    name = 'pedrogranado'
    start_urls = ['https://www.pedrogranado.com.br/pesquisa-de-imoveis/?locacao_venda=L&id_cidade%5B%5D=35&id_tipo_imovel%5B%5D=6&id_tipo_imovel%5B%5D=8&id_tipo_imovel%5B%5D=10&id_tipo_imovel%5B%5D=31&id_tipo_imovel%5B%5D=12&id_tipo_imovel%5B%5D=13&finalidade=&dormitorio=&garagem=&vmi=&vma=&ordem=1']

    def parse(self, response):

        items = response.css('a.btn-dark') 
        for item in items:
            url = item.css('a::attr(href)').get()
            self.log(url)
            response.follow(, callback= self.parse_detail)


    def parse_detail(response):

        cidade = 'Maringa'
        # bairro = response.xpath('//h3/a [last()]/text()').get()
        comodos = ''
        # garagem = response.css('i.fa-car + br + div::text').get()
        # suites = response.css('i.fa-bath + br + span::text').get()
        # quartos = response.css('i.fa-bed + br + div::text').get()
        # metragem = response.xpath('//strong[contains(text(), "Área útil") or contains(text(), "Área construída")]/following-sibling::span/text()').get() 
        # banheiro = response.css('i.fa-shower + br + div::text').get()
        # preco = response.xpath('//strong[contains(text(), "Valor aluguel")]/following-sibling::span/text()').get()
        
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
