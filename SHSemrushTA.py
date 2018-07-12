import datetime
import logging
from dateutil.relativedelta import relativedelta

logging.getLogger(__name__)


class SHSemrushTA:

    def __init__(self, connection, data_puller):
        self.conn = connection
        self.schema = 'semrush'
        self.summary_table = 'traffic_summary'
        self.summary_table_columns = ('report_dt',
                                      'domain',
                                      'users',
                                      'visits',
                                      'time_on_site',
                                      'search',
                                      'social',
                                      'direct',
                                      'paid',
                                      'referral',
                                      'bounce_rate',
                                      'rank',
                                      'db_code')
        self.summary_table_keywords = ('report_date',
                                      'domain',
                                      'users',
                                      'visits',
                                      'time_on_site',
                                      'search',
                                      'social',
                                      'direct',
                                      'paid',
                                      'referral',
                                      'bounce_rate',
                                      'rank')


        self.data_puller = data_puller

    def insert_traffic_summary(self):

        url_rows = self.conn.select('public', 'url_for_check_v', ['url', 'db_code'])
        url_code_list = [[url_row[0].replace('https://', '').replace('http://', '').replace('/','').replace('www.',''), url_row[1]] for url_row in url_rows]

        rows_to_insert = ()

        for url in url_code_list:

            print(url)
            data = self.data_puller.get_domain_summary(str([url[0]]).replace('\'', '"'))

            if len(data) != 0:
                data_dict = data[0]
                print(data_dict)
                row = ()
                for keyword in self.summary_table_keywords:
                    row = row + (data_dict[keyword],)
                row = row + (url[1],)
                print(row)

                rows_to_insert = rows_to_insert + (row,)

        if len(rows_to_insert) != 0:
            self.conn.insert(self.schema, self.summary_table, self.summary_table_columns, rows_to_insert)
        else:
            logging.error('There are nothing to insert to ' + self.schema + '.' + self.summary_table)

    def insert_traffic_summary_history(self):

        url_rows = self.conn.select('public', 'url_for_check_v', ['url', 'db_code'])
        url_code_list = [
            [url_row[0].replace('https://', '').replace('http://', '').replace('/', '').replace('www.', ''),
             url_row[1]] for url_row in url_rows]

        end_flg = 0
        today = datetime.datetime.today()
        month = datetime.datetime(today.year, today.month, 1) + relativedelta(months=-1)

        while end_flg == 0:
            rows_to_insert = ()
            print(str(month).replace(' 00:00:00', ''))

            for url in url_code_list:

                print(url)
                data = self.data_puller.get_domain_summary(str([url[0]]).replace('\'', '"'), month=str(month).replace(' 00:00:00', ''))

                if len(data) != 0:
                    data_dict = data[0]
                    print(data_dict)
                    row = ()
                    for keyword in self.summary_table_keywords:
                        row = row + (data_dict[keyword],)
                    row = row + (url[1],)
                    print(row)

                    rows_to_insert = rows_to_insert + (row,)

            if len(rows_to_insert) != 0:
                self.conn.insert(self.schema, self.summary_table, self.summary_table_columns, rows_to_insert)
            else:
                logging.info('There are nothing to insert to ' + self.schema + '.' + self.summary_table)
                end_flg = 1

            month = month + relativedelta(months=-1)
