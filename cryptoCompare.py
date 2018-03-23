from DataPuller import DataPuller
import requests


class cryptoCompare(DataPuller):

    def __init__(self):

        self.coin_url = 'https://min-api.cryptocompare.com/data/all/coinlist'
        self.price_url = 'https://min-api.cryptocompare.com/data/price'
        self.multiprice_url = 'https://min-api.cryptocompare.com/data/multiprice'

    def get_coin_info(self):
        return self.json_data_obtain(self.coin_url)['Data']

    def get_coin_price(self, from_currency='BTC', to_currency='KICK,USD,ETH', exchange=None, multiprice=False):
        payload = {
                   'fsym': from_currency,
                   'tsyms': to_currency,
                   'e': exchange
                   }
        url_for_request = self.multiprice_url if multiprice else self.price_url

        r = requests.get(url_for_request, params=payload)
        print(r.url)

        return self.json_data_obtain(url=url_for_request, param=payload)

    def get_coin_multiprice(self, from_currency='BTC', to_currency='KICK', exchange=None):
        self.get_coin_price(from_currency, to_currency, exchange, multiprice=True)