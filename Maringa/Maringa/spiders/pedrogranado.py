from urllib.parse import urljoin
import scrapy


class PedrogranadoSpider(scrapy.Spider):
    name = 'pedrogranado'
    start_urls = ['https://www.pedrogranado.com.br/pesquisa-de-imoveis/?locacao_venda=L&id_cidade%5B%5D=35&id_tipo_imovel%5B%5D=6&id_tipo_imovel%5B%5D=8&id_tipo_imovel%5B%5D=10&id_tipo_imovel%5B%5D=31&id_tipo_imovel%5B%5D=12&id_tipo_imovel%5B%5D=13&finalidade=&dormitorio=&garagem=&vmi=&vma=&ordem=1']

    def parse(self, response):

        # self.log(response.url)
        items = response.css('a.btn-dark') 
        for item in items:
            url_relative = item.css('a::attr(href)').get()
            url_absolute = 'https://www.pedrogranado.com.br/'
            url = urljoin(url_absolute, url_relative)
            # self.log(url)
            yield scrapy.Request(url= url, callback= self.parse_detail)

        next_url = response.xpath('//a[@class= "page-link"] [contains(text(), "Próxima")]')
        if next_url:
            url_relative = next_url.xpath('./@href').get()
            url_absolute = 'https://www.pedrogranado.com.br/'
            page_url = urljoin(url_absolute, url_relative)
            # import ipdb; ipdb.set_trace()
            try:
                yield scrapy.Request(url= page_url, callback= self.parse)
            except:
                pass


    def parse_detail(self, response):
        # import ipdb; ipdb.set_trace()
        cidade = 'Maringa'
        bairro = response.xpath('//h3/a [last()]/text()').get()
        comodos = ''
        garagem = response.css('i.fa-car + br + div::text').get()
        suites = response.css('i.fa-bath + br + span::text').get()
        quartos = response.css('i.fa-bed + br + div::text').get()
        metragem = response.xpath('//strong[contains(text(), "Área útil") or contains(text(), "Área construída")]/following-sibling::span/text()').get() 
        banheiro = response.css('i.fa-shower + br + div::text').get()
        preco = response.xpath('//strong[contains(text(), "Valor aluguel")]/following-sibling::span/text()').get()
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
