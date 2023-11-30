# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter



class FredScrapingPipeline:
    def process_item(self, item, spider):
        return item




class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='At070077&',  # add your password here if you have one set
            database='freddatabase'
        )

        # Create cursor, used to execute commands
        self.cur = self.conn.cursor()

     ## create fredData table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS fredData(
            id int NOT NULL auto_increment, 
            title VARCHAR(255),
            date VARCHAR(255),
            url VARCHAR(255),
            Source VARCHAR(255),
            Description text,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        
        self.cur.execute("""
            INSERT INTO fredData (
                title,
                date,
                url,
                Source,
                Description
            ) VALUES (%s, %s, %s, %s, %s)
        """, (
            item.get('title'),
            item.get('date'),
            item.get('url'),
            item.get('Source'),
            item.get('Description')
        ))

        # Execute insert of data into the database
        self.conn.commit()
        return item


    def close_spider(self, spider):
        # Close cursor & connection to the database
        self.cur.close()
        self.conn.close()
