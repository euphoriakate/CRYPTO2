from DataPuller import DataPuller
import requests
import datetime
import logging
import pprint

logging.getLogger(__name__)


class DPSEMRush(DataPuller):

    def __init__(self):
        self.url_main = 'http://api.semrush.com/'
        self.api_key = '935b97f54ac6b811e379181d53814bcb'

    def get_data(self, payload_addition):


        payload = {
            'key': self.api_key,
            #'export_columns': 'Dt,Db,Dn,Rk,Ot,At'
        }

        payload.update(payload_addition)
        url_for_request = self.url_main
        r = requests.get(url_for_request, params=payload)
        print(r.url)
        #pprint.pprint(r.text)
        return r.text

    def get_url_attendance(self, domain):
        additional_payload = {'type': 'domain_ranks',
                              'domain': domain,
                              'export_columns': 'Dt,Db,Dn,Rk,Ot,At'}
        return self.get_data(additional_payload)

    def get_keyword_statistic(self, keyword, database=None):

        additional_payload = {'type': 'phrase_all',
                              'phrase': keyword,
                              'export_columns': 'Ph,Db,Nq'}
        return self.get_data(additional_payload)


