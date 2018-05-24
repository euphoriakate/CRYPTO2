import datetime
import logging

logging.getLogger(__name__)


class SHSemrush:

    def __init__(self, connection, data_puller):
        self.conn = connection
        self.schema = 'semrush'
        self.keyword_table = 'keyword_search_volume'
        self.keyword_table_columns = ('report_dt', 'keyword', 'database', 'search_volume')
        self.url_table = 'url_attendance'
        self.url_table_columns = ('report_dt', 'country', 'domain', 'rank', 'organic_traffic',
                                  'adwords_traffic', 'db_code')
        self.data_puller = data_puller

    def insert_keyword_search_volume(self):

        keyword_rows = self.conn.select('public', 'keyword_for_check', ['keyword'])
        keyword_list = [keyword_row[0] for keyword_row in keyword_rows]

        rows_to_insert = ()

        for keyword in keyword_list:
            data = self.data_puller.get_keyword_statistic(keyword)
            rows_count = data.count('\n')

            for i in range(1, rows_count):
                list_of_row_values = data.split('\n')[i].strip().split(';')
                list_of_row_values.insert(0, str(datetime.datetime.now()))
                row = tuple(list_of_row_values)
                rows_to_insert = rows_to_insert + (row,)

        if len(rows_to_insert) != 0:
            return self.conn.insert(self.schema, self.keyword_table, self.keyword_table_columns, rows_to_insert)
        else:
            logging.error('There are nothing to insert to ' + self.schema + '.' + self.keyword_table)
            pass

    def insert_url_attendace(self):

        url_rows = self.conn.select('public', 'url_for_check_v', ['url', 'db_code'])
        url_code_list = [[url_row[0], url_row[1]] for url_row in url_rows]

        for url in url_code_list:
            rows_to_insert = ()
            data = self.data_puller.get_url_attendance(url[0])

            rows_count = data.count('\n')

            for i in range(1, rows_count):
                list_of_row_values = data.split('\n')[i].strip().split(';')
                list_of_row_values[0] = str(datetime.datetime.strptime(str(list_of_row_values[0]), '%Y%m%d'))
                row = tuple(list_of_row_values) + tuple([url[1]])
                rows_to_insert = rows_to_insert + (row,)

            if len(rows_to_insert) != 0:
                self.conn.insert(self.schema, self.url_table, self.url_table_columns, rows_to_insert)
            else:
                logging.error('There are nothing to insert to ' + self.schema + '.' + self.keyword_table)
