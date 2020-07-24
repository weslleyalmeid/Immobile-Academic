#Curso de Scrapy

### 1 - Intro Scrapy

Criar um arquivo e faça algo nessa estruta:

 ```py
class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://blog.scrapinghub.com']

    def parse(self, response):
        for title in response.css('.post-header>h2'):
            yield {'title': title.css('a ::text').get()}

        for next_page in response.css('a.next-posts-link'):
            yield response.follow(next_page, self.parse 
```
para executar o código

    scrapy runspider my_project.py  

### 2- Iniciar um projeto

    scrapy startproject nome_projeto 

### 3 - Criar um Spider

    scrapy genspider nome_class_spider url_project 

### 4 - Executar o Scrapy modo projeto

    scrapy crawl nome_class_spider 

### 5 - Executar e salvar o arquivo

    scrapy crawl nome_class_spider -o arquivo.formato 

### 6 - Comandos úteis

#### verificar o conteúdo html do elemento seletor
    
    response.get()
    response.extract() 
    response.extract_first() 

#### Verificar o texto de uma pesquisa xpath

    response.xpath('tag/.text()').extract() ou .extract_first() 

#### Xpath contains

    response.xpath('//tag[contains(@attr, '')]') 
    response.xpath('//tag[contains(text(), 'ipsum')]') 

#### Scrapy shell - aceitar a página em pt-br

```py
from scrapy import Request

req = Request('url', headers={'Accept-Language':'pt-br'})
fetch(req)
# response ativado a partir do fetch
```

#### Scrapy FormResquest
 
```py
from scrapy.http import FormRequest
def start_requests(self):
    url='http://imobiliariabelamorada.com.br/filtro/locacao/\
        apartamentos/pato-branco-pr/?busca=1'
    formdata={
        'cat1': '2.locacao', 
        'cat3': '4.apartamentos', 
        'cidade': '5362.pato-branco-pr', 
        'valor':'', 
        'cod':''
    }
    yield FormRequest(url, callback=self.parse, formdata=formdata, method='POST')
```

#### Alterar o robots.txt na class Spider:
```py
    def start_requests(self):
        
        url = 'https://www.almeidaw.com.br'
        form_data = {
            'cat1': '2.locacao',
        }
        # comando que subscreve ROBOTSTXT_OBEY do settings
        meta = {'dont_obey_robotstxt':'False'}
        yield scrapy.FormRequest(url=url, callback=self.parse, formdata=form_data ,method='POST', meta= meta)

```

#### Start requests completo:
```py

    def start_requests(self):
        
        url = 'https://www.jlo.com/todos/todos/1'

        # headers disponíveis no network
        headers = {
            'Accept': 'text/html,aation/signed-exchange;v=b3;q=9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '77',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': '__utmc=226286; __utmz=226LNAD',
            'Host': 'www.jlosso.com.br',
            'Origin': 'https://www.jlosso.com.br',
            'Referer': 'https://www.jlosso.com.br/home',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }

        # form de request
        form_data = {
            'cat1': '2.locacao',
            'cat3': '4.carros',
            'valormedio': '',
            'codigo': '',
            'cidade': '5166.pato'
        }
        
        # desativa o robots.txt
        meta = {'dont_obey_robotstxt':'False'}

        yield scrapy.FormRequest(
                        url=url,
                        callback=self.parse,
                        formdata=form_data,
                        method='POST',
                        headers= headers,
                        meta= meta
                    )
```

####  FormResquest Shell
exemplo básico de funcionamento:
~~~shell
scrapy shell
~~~

~~~shell
url='http://imobiliariabelamorada.com.br/filtro/locacao/ \
    apartamentos/pato-branco-pr/?busca=1'
~~~
 
**Passando form**
~~~shell
formdata={
    'cat1': '2.locacao', 
    'cat3': '4.apartamentos', 
    'cidade': '5362.pato-branco-pr', 
    'valor':'', 
    'cod':''
    } 
~~~

~~~shell
fetch(scrapy.FormRequest(url, formdata=formdata, method='POST'))
~~~

**Passando headers no shell**
~~~shell
scrapy shell -s USER_AGENT='custom user agent' 'http://www.example.com'
scrapy shell -s ROBOTSTXT_OBEY='False' 'http://www.example.com'
~~~
ou
~~~shell
url = 'http://www.example.com'
request = scrapy.Request(url, headers={'User-Agent': 'Mybot'})
fetch(request)
~~~

#### Execuntando scrapy em html localhost

**Shell**
~~~shell
    scrapy shell local/name/page
~~~
**Server local**
1. Abra o terminal na pasta onde consta o arquivo .html
    ~~~shell
        python -m http.server <port>
    ~~~
    obs.: A porta default é a 8000, porém, você pode alterar inserindo outro número valor

2. Vá até o local host e clique no arquivo.html

3. Executando scrapy localhost
    ~~~shell
        scrapy shell http://0.0.0.0:8000/arquivo.html
    ~~~
    obs.: No caso de genspider
    ~~~shell
        scrapy genspider name localhost
    ~~~


#### Passar argumento category

~~~shell
    scrapy crawl projeto -a category=nome_elemento
~~~

#### Ajustar o start_request

    Nesse método é onde faz o callback para o parse, caso seja passado algum argumento,
    é necessário fazer a verificação e/ou alteração do resquet.

#### Scrapy command line - List spiders

    scrapy list

#### Lista de pseudo-classes

**Irmão anterior**
        
    preceding-sibling::tag

**Irmão posterior**
    
    following-sibling::tag

**Pai**
   
    parent::tag

**Obter text dentro da tag css**

    response.css('mytag::text') -> Obter texto apenas do nó selecionado.
    response.css('mytag ::text') -> Obter texto do nó selecionado e seus nós filhos.

