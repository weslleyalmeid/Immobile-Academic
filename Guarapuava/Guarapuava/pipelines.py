import os.path
import sqlite3
import re

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class GuarapuavaPipeline:

    def process_item(self, item, spider):
        
        if spider.name == 'imperium':
            spider.log(f'####################### {spider.name} #######################')

            if item['bairro']:
                item['bairro'] = item['bairro'].strip()

            if item['garagem']:
                item['garagem'] = re.search(r'\d+', item['garagem']).group()
                item['garagem'] = int(item['garagem'])
            else:
                item['garagem'] = 0

            if item['suites'] is not None:
                
                if 'sendo' in item['suites']:
                    try:
                        item['suites'] = re.search(r'\d+ [S, s]u[i, í]tes?', item['suites']).group()
                        item['suites'] = int(re.findall(r'\d+', item['suites'])[0])
                        item['quartos'] = int(re.findall(r'^\d+', item['quartos'].strip())[0])
                        item['quartos'] = item['quartos'] - item['suites']
                    except:
                        item['quartos'] = 1
                else:
                    item['suites'] = 0
                    try:
                        item['quartos'] = int(re.findall(r'^\d+', item['garagem'].strip())[0])
                    except:
                        item['quartos'] = 1


            if item['metragem']:
                item['metragem'] = re.search(r'[1-9]\d*(,\d+)?', item['metragem']).group()
                item['metragem'] = float(item['metragem'].replace(',', '.'))

            if item['banheiro']:
                item['banheiro'] = int(re.findall(r'^\d+', item['banheiro'].strip())[0])
            else:
                item['banheiro'] = 1

            if item['preco']:
                item['preco'] = item['preco'].replace('.', '').replace(',', '.')
                item['preco'] = float(re.search(r'[1-9](\d+)?(.\d+)?',  item['preco']).group())
                    

            if item['comodos']:
                item['comodos'] = int(item['comodos'].strip())

            tables = 'cidade, bairro, comodos, garagem, suites, quartos, metragem, banheiro, preco'
            values = ':cidade, :bairro, :comodos, :garagem, :suites, :quartos, :metragem, :banheiro, :preco'
            insert = f'insert into imobiliaria({tables}) values ({values})'

            self.conn.execute(insert, item)
            self.conn.commit()

            return item

    def create_table(self):
        result = self.conn.execute(
            'select name from sqlite_master where type = "table" and name = "imobiliaria"'
        )

        try:
            value = next(result)

        except StopIteration as ex:
            create_table = """
                create table imobiliaria(id integer primary key,
                cidade text,
                bairro text,
                comodos int,
                garagem int,
                suites int,
                quartos text,
                metragem text,
                banheiro text,
                preco text
                )
            """.replace('\n', '')

            self.conn.execute(create_table)

    def open_spider(self, spider):
        # criar bando de dados e se conectar
        CURRENT_DIR = os.path.abspath('')
        ROOT_DIR = os.path.dirname(CURRENT_DIR)
        DATA_DIR = os.path.join(ROOT_DIR, 'data')
        BASE = os.path.join(DATA_DIR, 'database.db')
        self.conn = sqlite3.connect(BASE)
        self.create_table()

    def close_spider(self, spider):
        # fechando o banco de dados
        self.conn.close()