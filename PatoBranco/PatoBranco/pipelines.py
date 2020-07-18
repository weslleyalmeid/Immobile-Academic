# -*- coding: utf-8 -*-
import os.path
import sqlite3
import re

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

class PatobrancoPipeline:
    def process_item(self, item, spider):

        # todo: imobiliária moretti
        if spider.name == 'moretti':
            spider.log(f'########################## {spider.name} ########################')

            if item['comodos']:
                item['comodos'] = int(item['comodos'].strip())

            if item['garagem'] == 'Sem Garagem':
                item['garagem'] = 0
            elif item['garagem']:
                int(item['garagem'].strip())
            else:
                item['garagem'] = 0

            if item['suites']:
                if '-- : --' in item['suites']:
                    item['suites'] = 0
                else:
                    item['suites'] = int(item['suites'].strip())
            else:
                item['suites'] = 0

            if item['quartos']:
                item['quartos'] = int(item['quartos'].strip())

            if item['metragem']:
                item['metragem'] = float(re.search(r'([1-9]\d+(\.)*\d+)',  item['metragem']).group())

            if item['banheiro']:
                item['banheiro'] = int(item['banheiro'].strip())

            if item['preco']:
                item['preco'] = float(re.search(r'([1-9](\d+)?(\.)*\d+)', item['preco']).group())
                if item['preco'] < 10:
                    item['preco'] = item['preco'] * 1000


            tables = 'bairro, comodos, garagem, suites, quartos, metragem, banheiro, preco, cidade'
            values = ':bairro, :comodos, :garagem, :suites, :quartos, :metragem, :banheiro, :preco, :cidade'
            insert = f'insert into imobiliaria({tables}) values ({values})'
            
            self.conn.execute(insert, item)
            self.conn.commit()

            return item

        # todo: imobiliária invest
        if spider.name == 'invest':
            spider.log(
                f'########################## {spider.name} ########################')

            if item['bairro']:
                item['bairro'] = item['bairro'].replace(
                    'APARTAMENTO', '').replace('BAIRRO', '').replace('CASA', '').strip()

            if item['garagem']:
                item['garagem'] = int(item['garagem'].strip())
            else:
                item['garagem'] = 0

            if item['suites']:
                item['suites'] = int(item['suites'].strip())
            else:
                item['suites'] = 0

            if item['quartos']:
                item['quartos'] = int(item['quartos'].strip())

            if item['metragem']:
                item['metragem'] = float(item['metragem'].replace(',', '.').strip())

            if item['banheiro']:
                item['banheiro'] = int(item['banheiro'].strip())

            if item['preco']:
                item['preco'] = item['preco'].replace('.', '').replace(',', '.')
                item['preco'] = float(re.search(r'([1-9]\d+(\.)*\d+|\d+)',  item['preco']).group())

            if item['comodos'] is not None:
                item['comodos'] = int(item['comodos'].strip())


            tables = 'bairro, comodos, garagem, suites, quartos, metragem, banheiro, preco, cidade'
            values = ':bairro, :comodos, :garagem, :suites, :quartos, :metragem, :banheiro, :preco, :cidade'
            insert = f'insert into imobiliaria({tables}) values ({values})'

            self.conn.execute(insert, item)
            self.conn.commit()

            return item

        # todo: solar
        if spider.name == 'solar':
            spider.log(f'###################### {spider.name} ######################')

            if item['bairro']:
                item['bairro'] = item['bairro'].replace('BAIRRO', 'B')
                item['bairro'] = re.search(r'[B](\s+\w+)?\s\w+', item['bairro']).group()
                item['bairro'] = item['bairro'].replace('B', '').strip()

            if item['garagem']:
                item['garagem'] = re.search(r'\d+', item['garagem']).group()
                item['garagem'] = int(item['garagem'].strip())
            else:
                item['garagem'] = 0

            if 'suíte' in item['suites']:
                quartos = re.findall(r'\(\d+\)+', item['suites'])
                item['suites'] = int(quartos[1].replace('(','').replace(')',''))
                item['quartos'] = int(quartos[0].replace('(','').replace(')','')) - 1
            else:
                item['suites'] = 0
                item['quartos'] = int(re.search(r' \d+', item['quartos']).group().strip())

            if item['metragem']:
                item['metragem'] = int(re.search(r'[1-9]+(\d+)?', item['metragem']).group())

            if item['banheiro']:
                item['banheiro'] = int(re.search(r'[1-9]+(\d+)?', item['banheiro']).group())

            if item['preco']:
                item['preco'] = item['preco'].replace('.', '').replace(',', '.')
                item['preco'] = float(re.search(r'([1-9]\d+(\.)*\d+|\d+)',  item['preco']).group())

            if item['comodos'] is not None:
                item['comodos'] = int(item['comodos'].strip())



            tables = 'bairro, comodos, garagem, suites, quartos, metragem, banheiro, preco, cidade'
            values = ':bairro, :comodos, :garagem, :suites, :quartos, :metragem, :banheiro, :preco, :cidade'
            insert = f'insert into imobiliaria({tables}) values ({values})'

            self.conn.execute(insert, item)
            self.conn.commit()

            return item

         # todo: solar
        
        # todo: bela morada
        if spider.name == 'belamorada':
            spider.log(f'###################### {spider.name} ######################')

            if item['bairro']:
                item['bairro'] = item['bairro'].replace('BAIRRO', 'B')
                item['bairro'] = re.search(r'[B](\s+\w+)?\s\w+', item['bairro']).group()
                item['bairro'] = item['bairro'].replace('B', '').strip()

            if item['garagem']:
                item['garagem'] = int(item['garagem'].strip())
            else:
                item['garagem'] = 0

            if item['suites']:
                item['suites'] = int(item['suites'])
            else:
                item['suites'] = 0

            if item['quartos']:
                item['quartos'] = int(item['quartos'])

            if item['metragem']:
                item['metragem'] = item['metragem'].replace(',', '.')
                item['metragem'] = int(re.search(r'[1-9]+(\d+)?', item['metragem']).group())

            if item['banheiro']:
                item['banheiro'] = int(re.search(r'[1-9]+(\d+)?', item['banheiro']).group())
            else:
                item['banheiro'] = 1

            if item['preco']:
                item['preco'] = item['preco'].replace('.', '').replace(',', '.')
                item['preco'] = float(re.search(r'([1-9]\d+(\.)*\d+|\d+)',  item['preco']).group())

            if item['comodos']:
                item['comodos'] = int(item['comodos'].strip())

            tables = 'bairro, comodos, garagem, suites, quartos, metragem, banheiro, preco, cidade'
            values = ':bairro, :comodos, :garagem, :suites, :quartos, :metragem, :banheiro, :preco, :cidade'
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