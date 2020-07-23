import scrapy


class JlossoSpider(scrapy.Spider):
    name = 'jlosso'

    def start_requests(self):
        
        url = 'https://www.jlosso.com.br/filtro/locacao/apartamentos/guarapuava/todos/todos/1/1'

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '77',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': '__utmc=226889286; __utmz=226889286.1595244362.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); ASPSESSIONIDCGACRSQB=AKMFMPACMJJABPLAPDKNENLH; _fbp=fb.2.1595505010680.1494509037; ASPSESSIONIDAEABTTRD=PINDKJPDKFANOLPGENCCIBMB; __utma=226889286.1140735861.1595244362.1595505010.1595508317.3; __utmb=226889286.3.10.1595508317; ASPSESSIONIDAEACSSQA=IBNNIFMADGHEBALIJNLILNAD',
            'Host': 'www.jlosso.com.br',
            'Origin': 'https://www.jlosso.com.br',
            'Referer': 'https://www.jlosso.com.br/home',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }


        form_data = {
            'cat1': '2.locacao',
            'cat3': '4.apartamentos',
            'valormedio': '',
            'codigo': '',
            'cidade': '5166.guarapuava'
        }

        yield scrapy.FormRequest(
                        url=url,
                        callback=self.parse,
                        formdata=form_data,
                        method='POST',
                        headers= headers,
                        meta= {'dont_obey_robotstxt':'False'}
                    )

    def parse(self, response):
        
        items = response.xpath('//a[@class="div-block-8-update1 w-inline-block"]')
        
        for item in items:
            url = item.xpath('./@href').get()
            self.log(url)
            yield scrapy.Request(url= url, callback= self.parse_detail)

        # next_page = response.xpath('//a[@class="link-10 left w-button"]/@href')
        # if next_page:

        #     url = next_page.extract_first()
        #     yield scrapy.Request(url, callback=self.parse, dont_filter=False)


    def parse_detail(self, response):

        cidade = 'Guarapuava'
        bairro = response.xpath('//div[@class="text-block-19"][contains(text(), "Bairro")]/following-sibling::div/text()').get()
        comodos = ''
        garagem = response.xpath('//div[@class="text-block-24"][contains(text(), "Garagem Co")]/preceding-sibling::div/div/text()').get()
        suites = response.xpath('//div[@class="text-block-24"][contains(text(), "Suite")]/preceding-sibling::div/div/text()').get()
        quartos = response.xpath('//div[@class="text-block-24"][contains(text(), "Quarto")]/preceding-sibling::div/div/text()').get()
        metragem = response.xpath('//div[@class="text-block-24"][contains(text(), "Área Con")]/preceding-sibling::div/div/text()').get()
        banheiro = response.xpath('//div[@class="text-block-24"][contains(text(), "Banheiro")]/preceding-sibling::div/div/text()').get()
        preco = response.xpath('//div[@class="text-block-16"]/text()').get()

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
