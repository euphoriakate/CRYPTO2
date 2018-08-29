from DataPuller import DataPuller
import requests
import logging
import copy
import json

logging.getLogger(__name__)


class DPSEMRushTA(DataPuller):

    def __init__(self):
        self.url_main = 'https://api.semrush.com/analytics/ta/v1'
        self.headers = {'Content-Type': "application/json"}
        self.key = '935b97f54ac6b811e379181d53814bcb'
        self.url_plain = 'https://ta.semrush.com/'

    def generate_token(self, payload):

        payload_token = copy.deepcopy(payload)
        payload_token['type'] = 'traffic_sources'
        r = requests.get(self.url_plain + '/bl', params=payload_token)

        return r.json()['token']

    def get_data_api(self, json_data):

        res = requests.post(self.url_main, json=json_data, headers=self.headers)
        print(res.url)

        return res.json()['data']['summary']['items']

    def get_data(self, payload_main, headers):

        payload = {
            'key': self.key
        }

        payload.update(payload_main)
        res = requests.get(self.url_plain, params=payload, headers=headers)

        return res.json()



    def get_domain_summary(self, domain_list, api, month=None):

        if api:
            if month is None:
                data = {'query':
                            '{summary(actions:{domains:' + domain_list + ',}){items{bounce_rate, domain, rank, report_date, visits, users, direct, referral, social, search, paid, time_on_site}}}'}
            else:
                data = {'query':
                            '{summary(actions:{domains:' + domain_list + ',hp:{date:"' + month + '"},}){items{bounce_rate, domain, rank, report_date, visits, users, direct, referral, social, search, paid, time_on_site}}}'}

            return self.get_data_api(data)

        else:
            domain_list = json.loads(domain_list)
            domain = domain_list

            payload = {
                            'type': 'history',
                            'domain': domain,
                            'limit': 12,
                            'offset': 0,
                            'key': self.key
                        }

            token = self.generate_token(payload)

            headers = {
                'Authorization': 'Bearer ' + token
            }

            return self.get_data(payload, headers)

