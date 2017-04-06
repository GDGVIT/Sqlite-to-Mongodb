import json
import sqlite3
import os
import re
import sys
import pymongo


class JSON():

    def dictionary(self, var1):
        return [dict(i) for i in var1]

    def dumping(self, var1):
        var1 = self.dictionary(var1)
        # return json.dumps(var1)
        return var1


class SQL(JSON):
    conn = ''
    path = ''
    name_db = ''
    db = ''
    table_list = []
    data = []

    def remove_slash(self, string):
        string = re.sub('/', '', string)
        return string

    def change_dir(self):
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)
        return dname

    def get_details(self):
        self.path = self.change_dir()
        self.name_db = input('Enter the name of the db: ')
        self.name_db = self.remove_slash(self.name_db)

    def connect(self):
        try:
            self.db = sqlite3.connect(os.path.join(self.path, self.name_db))
        except sqlite3.OperationalError as e:
            print(e)
            sys.exit()
        self.conn = self.db
        self.conn.row_factory = sqlite3.Row  # enables column access by name, row[column_name]
        self.conn = self.db.cursor()

    def listing_tables(self):
        self.table_list = self.db.execute('''
			SELECT name FROM sqlite_master WHERE type = 'table';
			''').fetchall()
        self.table_list = [i[0] for i in self.table_list]
        self.table_list = [i for i in self.table_list if i not in ('sqlite_sequence', 'sqlite_stat1')]


class MONGO(SQL):
    client = ''
    ns_db = ''

    def prerequesites(self):
        # try:
        #      os.system('mongod')
        # except Exception as e:
        #    print('Make sure you have installed Mongo db')
        self.client = pymongo.MongoClient()
        self.ns_db = self.client[self.name_db[:-3]]

    def new_collection(self, table, data):
        coll = self.ns_db[table]
        coll.insert(data)

    def reading_tables(self):
        row = []
        for i in self.table_list:
            row += (self.conn.execute('SELECT * FROM {}'.format(i))).fetchall()
            temp = self.dumping(row)
            self.new_collection(i, temp)


class ORDER_EXECUTION(MONGO):

    def execute(self):
        self.get_details()
        self.connect()
        self.listing_tables()
        self.prerequesites()
        self.reading_tables()


if __name__ == '__main__':
    obj = ORDER_EXECUTION()
    obj.execute()
    print('Done importing')
