import os.path
import sqlite3
import re

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class UmuaramaPipeline:
    def process_item(self, item, spider):

        if spider.name == 'parana':

            if 'garagem' or 'Garagem' or 'garagens' in item['garagem']:
                try:
                    item['garagem'] = re.search(r'\d+ (vagas de )?[g, G]aragem', item['garagem']).group()
                    item['garagem'] = int(re.search(r'\d+', item['garagem']).group())
                except:
                    item['garagem'] = 1
            else:
                item['garagem'] = 0

            
            if 'Suíte' or 'suite' or 'suíte' in item['suites']:
                item['suites'] = 1
                if item['quartos']:
                    item['quartos'] = int(item['quartos'].strip()) - 1
                else:
                    item['quartos'] = 1
            elif item['quartos']:
                item['suites'] = 0
                item['quartos'] = int(item['quartos'].strip())
            else:
                item['suites'] = 0
                item['quartos'] = 2

            if item['metragem']:
                item['metragem'] = float(item['metragem'].strip())
                                
            try:
                item['banheiro'] = re.search(r'\d+ Bwc', item['banheiro']).group()
                item['banheiro'] = int(re.search(r'\d+', item['banheiro']).group().strip())
            except:
                try:
                    item['banheiro'] = re.search(r'\d+ [B, b]anheiro', item['banheiro']).group()
                    item['banheiro'] = int(re.search(r'\d+', item['banheiro']).group())
                except:
                    item['banheiro'] = 1

            if item['preco']:
                item['preco'] = item['preco'].replace('.', '').replace(',', '.')
                item['preco'] = float(re.search(r'[1-9](\d+)?(.\d+)?',  item['preco']).group())


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