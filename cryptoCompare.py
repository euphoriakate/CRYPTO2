from DataPuller import DataPuller
import requests

class cryptoCompare(DataPuller):

    def __init__(self):

        self.coin_url = 'https://min-api.cryptocompare.com/data/all/coinlist'
        self.price_url = 'https://min-api.cryptocompare.com/data/price'

    def get_coin_info(self):
        return self.json_data_obtain(self.coin_url)['Data']

    def get_coin_price(self, from_currency = ['BTC'], to_currency = 'KICK,USD'):
        payload = {'fsym': from_currency, 'tsyms': to_currency}

        r = requests.get(self.price_url, params=payload) #.json()
        print(r.url)

        return self.json_data_obtain(url=self.price_url, param=payload)
