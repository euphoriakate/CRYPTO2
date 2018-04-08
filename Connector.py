from config import config
import psycopg2
import logging

logging.getLogger(__name__)


class Connector:

    def __init__(self, db_name):
        """ Connect to the PostgreSQL database server """
        try:
            # start logging
            logging.info('Try to get database ' + db_name + ' params...')
            # read connection parameter
            params = config(db_name)
            print(params)
            # connect to the PostgreSQL server
            logging.info('Try to connect to database ' + db_name)
            self.conn = psycopg2.connect(**params)
            logging.info('Connection to ' + db_name + ' has been successfully established')
            # create a cursor
            self.cur = self.conn.cursor()

        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)

    def insert(self, schema, table, columns, data):
        """ insert a new vendor into the vendors table """
        columns_name = ','.join([str(x) for x in columns])
        pattern_string = ','.join(['%s' for x in columns])
        args_str = b','.join(self.cur.mogrify('('+pattern_string+')', x) for x in data).decode()
        sql = 'INSERT INTO ' + schema + '.' + table + '(' + columns_name + """)
                         VALUES """ + args_str
        print(sql)
        try:
            logging.info('Try to execute script')
            logging.info(sql)
            self.cur.execute(sql)
            # commit the changes to the database
            self.conn.commit()
            logging.info('Executed!')
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)

    def select(self, schema, table, columns=None):
        if columns is not None:
            columns_to_select = ','.join(columns)
        else:
            columns_to_select = '*'
        sql = 'select ' + columns_to_select + ' from ' + schema + '.' + table
        logging.info(sql)
        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
            return data
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close(self):
        self.conn.close()
        logging.info('Connection has been closed')
