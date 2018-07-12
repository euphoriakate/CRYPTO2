from DataPuller import DataPuller
import requests
import datetime
import logging
import pprint

logging.getLogger(__name__)


class DPSEMRushTA(DataPuller):

    def __init__(self):
        self.url_main = 'https://api.semrush.com/analytics/ta/v1'
        self.headers = {'Content-Type': "application/json"}

    def get_data(self, json_data):

        res = requests.post(self.url_main, json=json_data, headers=self.headers)
        return res.json()['data']['summary']['items']

    def get_domain_summary(self, domain_list, month=None):
        if month is None:
            data = {'query':
                        '{summary(actions:{domains:' + domain_list + ',}){items{bounce_rate, domain, rank, report_date, visits, users, direct, referral, social, search, paid, time_on_site}}}'}
        else:
            data = {'query':
                        '{summary(actions:{domains:' + domain_list + ',hp:{date:"' + month + '"},}){items{bounce_rate, domain, rank, report_date, visits, users, direct, referral, social, search, paid, time_on_site}}}'}
        print(data)
        return self.get_data(data)