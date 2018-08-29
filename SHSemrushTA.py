import datetime
import logging
from dateutil.relativedelta import relativedelta
from functools import reduce

logging.getLogger(__name__)


def coalesce(*arg):
  return reduce(lambda x, y: x if x is not None else y, arg)

class SHSemrushTA:

    def __init__(self, connection, data_puller):
        self.conn = connection
        self.schema = 'semrush'
        self.summary_table = 'traffic_summary'
        self.summary_table_columns_api = ('report_dt',
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
        self.summary_table_columns = ('report_dt',
                                      'domain',
                                      'device',
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
        self.summary_table_keywords_api = ('report_date',
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

        self.summary_table_keywords = ('date',
                                       'domain',
                                       'device',
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

    def insert_traffic_summary(self, api):

        url_rows = self.conn.select('public', 'url_for_check_v', ['url', 'db_code'])
        url_code_list = [[url_row[0].replace('https://', '')
                                    .replace('http://', '')
                                    .replace('/', '')
                                    .replace('www.', ''), url_row[1]] for url_row in url_rows]

        rows_to_insert = ()

        max_month = self.conn.select_group_by(self.schema, self.summary_table, columns='report_dt', agr_function='max')[0][0]
        max_month = coalesce(max_month, datetime.datetime(year=2016, month=1, day=1))
        #month_to_load = max_month + relativedelta(months=1)
        print(max_month)

        for url in url_code_list:

            if api:

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
            else:
                rows_to_insert = ()
                data = self.data_puller.get_domain_summary(str([url[0]]).replace('\'', '"'), api=False)



                device_list = ['mobile', 'desktop']

                for device in device_list:
                    if device in data.keys():
                        for date_instance in data[device]['items']:
                            if date_instance['date'] > max_month.strftime('%Y-%m-%d'):
                                row = ()
                                for keyword in self.summary_table_keywords:

                                    if keyword == 'device':
                                        row = row + (device,)
                                    else:
                                        row = row + (date_instance[keyword],)
                                row = row + (url[1],)

                                rows_to_insert = rows_to_insert + (row,)
                

            if len(rows_to_insert) != 0:
                self.conn.insert(self.schema, self.summary_table, self.summary_table_columns, rows_to_insert)
            else:
                logging.error('There are nothing to insert to ' + self.schema + '.' + self.summary_table)


    def insert_traffic_summary_history(self, api):

        url_rows = self.conn.select('public', 'url_for_check_v', ['url', 'db_code'])
        url_code_list = [
            [url_row[0].replace('https://', '').replace('http://', '').replace('/', '').replace('www.', ''),
             url_row[1]] for url_row in url_rows]

        if api:

            end_flg = 0
            today = datetime.datetime.today()
            month = datetime.datetime(today.year, today.month, 1) + relativedelta(months=-1)

            while end_flg == 0:
                rows_to_insert = ()
                print(str(month).replace(' 00:00:00', ''))

                for url in url_code_list:

                    print(url)
                    data = self.data_puller.get_domain_summary(str([url[0]]).replace('\'', '"'), month=str(month)
                                                                            .replace(' 00:00:00', ''))

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

        else:
            for url in url_code_list:

                rows_to_insert = ()
                data = self.data_puller.get_domain_summary(str([url[0]]).replace('\'', '"'), api=False)

                device_list = ['mobile', 'desktop']

                for device in device_list:
                    if device in data.keys():
                        for date_instance in data[device]['items']:

                            row = ()
                            for keyword in self.summary_table_keywords:

                                if keyword == 'device':
                                    row = row + (device,)
                                else:
                                    row = row + (date_instance[keyword],)
                            row = row + (url[1],)

                            rows_to_insert = rows_to_insert + (row,)

                if len(rows_to_insert) != 0:
                    self.conn.insert(self.schema, self.summary_table, self.summary_table_columns, rows_to_insert)
                else:
                    logging.error('There are nothing to insert to ' + self.schema + '.' + self.summary_table)

'''
import requests
import pprint


url = 'https://ta.semrush.com/?type=social_sources&limit=100&offset=0&key=935b97f54ac6b811e379181d53814bcb&domain=amazon.com'
url = 'https://ta.semrush.com/?type=geo&limit=256&offset=0&key=935b97f54ac6b811e379181d53814bcb&domain=amazon.com'
url = 'https://ta.semrush.com/?type=referral_sources&limit=100&offset=0&key=935b97f54ac6b811e379181d53814bcb&domain=amazon.com'
#url = 'https://ta.semrush.com/?type=search_sources&limit=100&offset=0&key=935b97f54ac6b811e379181d53814bcb&domain=amazon.com'
#url = 'https://ta.semrush.com/?type=history&limit=12&offset=0&key=935b97f54ac6b811e379181d53814bcb&domain=amazon.com'
#url = 'https://ru.semrush.com/analytics/traffic/overview/amazon.com'
url = 'https://ta.semrush.com/?type=history&limit=12&offset=0&key=935b97f54ac6b811e379181d53814bcb&domain=coinex.com'

url_token = 'https://ta.semrush.com/bl?type=traffic_sources&key=935b97f54ac6b811e379181d53814bcb&domain=coinex.com'
r = requests.get(url_token)
token = r.json()['token']
pprint.pprint(token)

r = requests.get(url, headers={'Authorization': 'Bearer ' + token })

pprint.pprint(r.json())
'''