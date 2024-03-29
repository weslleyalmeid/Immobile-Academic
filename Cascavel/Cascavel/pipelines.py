# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os.path
import sqlite3
import re

class CascavelPipeline:
    def process_item(self, item, spider):

        if spider.name == 'cidade':
            spider.log(f'####################### {spider.name} #######################')

            try:
                item['bairro'] = re.search(r'- \w+( .*)? -', item['bairro']).group()
                item['bairro'] = item['bairro'].replace('-', '').strip()
            except:
                item['bairro'] = None

            if item['garagem']:
                item['garagem'] = int(re.search(r'\d+', item['garagem']).group())

            if item['suites']:
                item['suites'] = int(re.search(r'\d+', item['suites']).group())

            if item['quartos']:
                item['quartos'] = int(re.search(r'\d+', item['quartos']).group())

            if item['metragem']:
                item['metragem'] = item['metragem'].replace(',', '.')
                item['metragem'] = float(re.search(r'[1-9]\d+(.\d+)?', item['metragem']).group())

            if item['banheiro']:
                item['banheiro'] = int(item['banheiro'].strip())

            if item['preco']:
                item['preco'] = item['preco'].replace('.', '').replace(',', '.')
                try:
                    item['preco'] = float(re.search(r'[1-9](\d+)?(.\d+)?',  item['preco']).group())
                except:
                    item['preco'] = None

            tables = 'cidade, bairro, comodos, garagem, suites, quartos, metragem, banheiro, preco'
            values = ':cidade, :bairro, :comodos, :garagem, :suites, :quartos, :metragem, :banheiro, :preco'
            insert = f'insert into imobiliaria({tables}) values ({values})'

            self.conn.execute(insert, item)
            self.conn.commit()
            return item   


        if spider.name == 'lokatell':
            spider.log(f'####################### {spider.name} #######################')

            try:
                item['bairro'] = item['bairro'].strip()
                item['bairro'] = re.search(r'.* -', item['bairro']).group()
                item['bairro'] = item['bairro'].replace('-', '').strip()
            except:
                item['bairro'] = None

            if item['garagem'] and 'Não' not in item['garagem']:
                item['garagem'] = item['garagem'].strip()
                item['garagem'] = int(re.search(r'\d+', item['garagem']).group())
            else:
                item['garagem'] = None

            if item['suites']:
                item['suites'] = item['suites'].strip()
                item['suites'] = int(re.search(r'\d+', item['suites']).group())

            if item['quartos']:
                item['quartos'] = item['quartos'].strip()
                item['quartos'] = int(re.search(r'\d+', item['quartos']).group())

            if item['metragem']:
                item['metragem'] = item['metragem'].strip()
                item['metragem'] = item['metragem'].replace(',', '.')
                item['metragem'] = float(re.search(r'[1-9]\d+(.\d+)?', item['metragem']).group())

            if item['banheiro']:
                item['banheiro'] = item['banheiro'].strip()
                item['banheiro'] = float(re.search(r'\d+', item['banheiro']).group())

            if item['preco']:
                item['preco'] = item['preco'].strip()
                item['preco'] = item['preco'].replace('.', '').replace(',', '.')
                try:
                    item['preco'] = float(re.search(r'[1-9](\d+)?(.\d+)?', item['preco']).group())
                except:
                    item['preco'] = None

            tables = 'cidade, bairro, comodos, garagem, suites, quartos, metragem, banheiro, preco'
            values = ':cidade, :bairro, :comodos, :garagem, :suites, :quartos, :metragem, :banheiro, :preco'
            insert = f'insert into imobiliaria({tables}) values ({values})'

            self.conn.execute(insert, item)
            self.conn.commit()
            return item   


        if spider.name == 'imovelweb':
            spider.log(f'####################### {spider.name} #######################')

            try:
                item['bairro'] = item['bairro'].strip()
                item['bairro'] = re.search(r', .*,', item['bairro']).group()
                item['bairro'] = item['bairro'].replace(',', '').strip()
            except:
                item['bairro'] = None


            if item['garagem']:
                item['garagem'] = int(item['garagem'])


            if item['suites']:
                item['suites'] = int(item['suites'])


            if item['quartos']:
                item['quartos'] = int(item['quartos'])


            if item['metragem']:
                item['metragem'] = item['metragem'].strip()
                item['metragem'] = item['metragem'].replace(',', '.')
                item['metragem'] = float(re.search(r'[1-9]\d+(.\d+)?', item['metragem']).group())


            if item['banheiro']:
                item['banheiro'] = int(item['banheiro'])
            

            if item['preco']:
                item['preco'] = item['preco'].strip()
                item['preco'] = item['preco'].replace('.', '').replace(',', '.')
                try:
                    item['preco'] = float(re.search(r'[1-9](\d+)?(.\d+)?',  item['preco']).group())
                except:
                    item['preco'] = None

            # tables = 'cidade, bairro, comodos, garagem, suites, quartos, metragem, banheiro, preco'
            # values = ':cidade, :bairro, :comodos, :garagem, :suites, :quartos, :metragem, :banheiro, :preco'
            # insert = f'insert into imobiliaria({tables}) values ({values})'

            # self.conn.execute(insert, item)
            # self.conn.commit()
            return item

        
        if spider.name == 'porto':
            spider.log(f'####################### {spider.name} #######################')

            if item['bairro']:
                item['bairro'] = item['bairro'].strip()
                # item['bairro'] = re.search(r', .*,', item['bairro']).group()
                # item['bairro'] = item['bairro'].replace(',', '').strip()


            if item['garagem']:
                item['garagem'] = int(item['garagem'].strip())


            if item['suites']:
                item['suites'] = int(item['suites'].strip())


            if item['quartos']:
                item['quartos'] = int(item['quartos'].strip())


            if item['metragem']:
                item['metragem'] = item['metragem'].strip()
                item['metragem'] = item['metragem'].replace(',', '.')
                item['metragem'] = float(re.search(r'[1-9]\d+(.\d+)?', item['metragem']).group())


            if item['banheiro']:
                item['banheiro'] = int(item['banheiro'].strip())
            

            if item['preco']:
                item['preco'] = item['preco'].strip()
                item['preco'] = item['preco'].replace('.', '').replace(',', '.')
                try:
                    item['preco'] = float(re.search(r'[1-9](\d+)?(.\d+)?',  item['preco']).group())
                except:
                    item['preco'] = None

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
