# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os.path
import sqlite3
import re


class FranciscobeltraoPipeline:

    def process_item(self, item, spider):
        if spider.name == 'casaril':
            spider.log(
                f'**************** {spider.name} ****************')

            if item['bairro']:
                item['bairro'] = item['bairro'].replace('Bairro:', '')
                item['bairro'] = item['bairro'].strip()

            if item['garagem']:
                try:
                    item['garagem'] = re.search(r'\d+ vaga(s?) de garagem', item['garagem']).group()
                    item['garagem'] = re.search(r'\d+', item['garagem']).group()
                    item['garagem'] = int(item['garagem'].strip())
                except:
                    item['garagem'] = 0

            if item['suites']:
                item['suites'] = int(
                    re.search(r' \d+', item['suites']).group().strip())
            
            if item['quartos']:
                item['quartos'] = int(
                    re.search(r' \d+', item['quartos']).group().strip())
            
            if item['metragem']:
                item['metragem'] = int(
                    re.search(r'[1-9]+(\d+)?', item['metragem']).group())

            if item['banheiro']:
                item['banheiro'] = int(
                    re.search(r'\d+', item['banheiro']).group())

            if item['preco']:
                item['preco'] = item['preco'].replace(
                    '.', '').replace(',', '.')
                item['preco'] = float(
                    re.search(r'[1-9](\d+)?(.\d+)?',  item['preco']).group())
                    

            if item['comodos'] is not None:
                item['comodos'] = int(item['comodos'].strip())

            tables = 'cidade, bairro, comodos, garagem, suites, quartos, metragem, banheiro, preco'
            values = ':cidade, :bairro, :comodos, :garagem, :suites, :quartos, :metragem, :banheiro, :preco'
            insert = f'insert into imobiliaria({tables}) values ({values})'

            self.conn.execute(insert, item)
            self.conn.commit()

            return item


        if spider.name == 'tomazoni':
            spider.log(
                f'**************** {spider.name} ****************')
            if item['bairro']:
                item['bairro'] = item['bairro'].replace('-', '').strip()

            if item['garagem']:
                item['garagem'] = int(item['garagem'])
            else:
                item['garagem'] = 0

            if item['suites']:
                item['suites'] = int(item['suites'])
            else:
                item['suites'] = 0

            if item['quartos']:
                item['quartos'] = int(item['quartos'])

            if item['metragem']:
                item['metragem'] = float(item['metragem'].replace(',', '.'))
            
            if item['banheiro']:
                item['banheiro'] = int(item['banheiro'])

            if item['preco']:
                item['preco'] = item['preco'].replace('.', '').replace(',', '.')
                item['preco'] = float(re.search(r'[1-9](\d+)?(.\d+)?',  item['preco']).group())

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