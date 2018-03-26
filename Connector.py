from config import config
import psycopg2


class Connector:

    def __init__(self):
        """ Connect to the PostgreSQL database server """
        try:
            #read connection parameter
            params = config()
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**params)
            # create a cursor
            self.cur = self.conn.cursor()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


    def handle(self, item):
        '''
        if item == 'N/A':
            return None
        elif not item:
            return 0
        elif item:
            return 1
        else:
            return item
            '''
        return item

    def insert(self, schema, table, columns, data):
        """ insert a new vendor into the vendors table """
        row = ()
        for i in data:
            row = row + (self.handle(i),)
        values_s = ','.join(['%s' for x in columns])

        print(row)
        columns_name = ','.join([str(x) for x in columns])

        sql = 'INSERT INTO ' + schema + '.' + table + '(' + columns_name + """)
                 VALUES(""" + values_s + """);"""

        #sql = """INSERT INTO cryptocompare.coin(id, code, short_name, full_name, algorithm, proof_type, is_trading, premined_value, fully_premined, total_coin_supply, total_coins_free_float, sponsored, url)
        #             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"""

        print(sql, row)

        try:
            print('Try execute')
            self.cur.execute(sql, row)
            print('Executed!')
            # commit the changes to the database
            self.conn.commit()
            # close communication with the database
            #self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        #finally:
        #    if self.conn is not None:
        #        self.conn.close()

    def select(self, schema, table, columns=None):
        if columns is not None:
            columns_to_select = ''.join(columns)
        else:
            columns_to_select = '*'
        print(columns_to_select)
        sql = 'select ' + columns_to_select + ' from ' + schema + '.' + table + ' limit 20'
        print(sql)
        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close(self):
        self.conn.close()
        print('Connection has been closed.')

