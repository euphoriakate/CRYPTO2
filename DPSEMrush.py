from DataPuller import DataPuller
import requests
import datetime
import logging

logging.getLogger(__name__)


class DPSEMRush(DataPuller):

    def __init__(self):
        self.url_main = 'http://api.semrush.com/' # ?key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX&type=domain_ranks&export_columns=Db,Dn,Rk,Or,Ot,Oc,Ad,At,Ac,Sv,Sh&domain=seobook.com&database=us
        self.url_price = 'https://min-api.cryptocompare.com/data/price'
        self.api_key = '935b97f54ac6b811e379181d53814bcb'

    def get_url_attendance(self):

        payload = {
                    'key': self.api_key,
                    'type': 'domain_ranks',
                    'export_columns': 'Dt,Db,Dn,Rk,Ot,At',
                    'domain': 'seobook.com',
                    #'database': 'us,se'
                   }

        url_for_request = self.url_main
        r = requests.get(url_for_request, params=payload)
        print(r.url)
        return r
