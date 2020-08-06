import scrapy


class PortoSpider(scrapy.Spider):
    name = 'porto'
    start_urls = ['https://www.portoseguroimobiliaria.com/filtros/locacao/apartamentos/todos/col/1']

    def parse(self, response):

        items = response.css('a.link-block-219-portoseguro1')

        for item in items:
            url = item.css('a::attr(href)').get()
            print(url)

            # import ipdb; ipdb.set_trace()
