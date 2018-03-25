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
        if item == 'N/A':
            return None
        elif item == False:
            return 0
        elif item == True:
            return 1
        else:
            return item

    def insert(self, schema, table, data):
        """ insert a new vendor into the vendors table """
        row = ()
        for i in data:
            row = row + (self.handle(i),)
        print (row)
        sql = 'INSERT INTO ' + schema + """.""" + table + """(id, code, short_name, full_name, algorithm, proof_type, premined_value, fully_premined, total_coin_supply, total_coins_free_float, sponsored, url)
                 VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"""

        #sql = """INSERT INTO cryptocompare.coin(id, code, short_name, full_name, algorithm, proof_type, is_trading, premined_value, fully_premined, total_coin_supply, total_coins_free_float, sponsored, url)
        #             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"""

        #print(sql)

        try:

            self.cur.execute(sql, row)
            # commit the changes to the database
            self.conn.commit()
            # close communication with the database
            #self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        #finally:
        #    if self.conn is not None:
        #        self.conn.close()

    def close(self):
        self.conn.close()
        print('Connection has been closed.')
