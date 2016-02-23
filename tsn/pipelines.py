# from sqlalchemy.orm import sessionmaker
#from models import Deals, db_connect, create_deals_table
from scrapy import signals


import json
import codecs

import psycopg2

from collections import OrderedDict


class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open('data_utf8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class TsnPipeline(object):
    """Tsn pipeline for storing scraped items in the database"""
    def __init__(self):
        self.conn = psycopg2.connect(user="taras",
                                    host="localhost",
                                    dbname="postgres",
                                    password="postgres")


    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        if not item["url"]:
            print "no item url"

        item["headline"] = item["headline"].encode('utf-8')
        item["url"] = item["url"].encode('utf-8')
        item["date"] = item["date"].encode('utf-8')
            
        cur = self.conn.cursor()

        cur.execute('INSERT INTO items(headline, url, date) VALUES(%s, %s, %s)',(item["headline"], item["url"], item["date"]))

        self.conn.commit()
        return item