import json
import sqlite3
import os
import re
import sys


class JSON():

    def dictionary(self, var1):
        return [dict(i) for i in var1]

    def dumping(self, var1):
        var1 = self.dictionary(var1)
        return json.dumps(var1)


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

    def reading_tables(self):
        row = []
        for i in self.table_list:
            row += (self.conn.execute('SELECT * FROM {}'.format(i))).fetchall()
        self.data = self.dumping(row)


class order_execution(SQL):

    def execute(self):
        self.get_details()
        self.connect()
        self.listing_tables()
        self.reading_tables()
        print(self.data)

if __name__ == '__main__':
    obj = order_execution()
    obj.execute()
