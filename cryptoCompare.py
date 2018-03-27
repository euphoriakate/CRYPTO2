from DataPuller import DataPuller
import requests
import datetime

class cryptoCompare(DataPuller):

    def __init__(self):

        self.url_coin = 'https://min-api.cryptocompare.com/data/all/coinlist'
        self.url_price = 'https://min-api.cryptocompare.com/data/price'
        self.url_pricemulti = 'https://min-api.cryptocompare.com/data/pricemulti'
        self.url_pricemultifull = 'https://min-api.cryptocompare.com/data/pricemultifull'
        self.url_generate_avg = 'https://min-api.cryptocompare.com/data/generateAvg'
        self.url_price_historical = 'https://min-api.cryptocompare.com/data/pricehistorical'

    def get_coin_info(self):
        '''
        Get general info for all the coins available on the website.
        Get coin list example https://www.cryptocompare.com/api/data/coinlist/
        '''
        return self.json_data_obtain(self.url_coin)['Data']

    def get_coin_price(self, from_currency='BTC', to_currency='KICK,USD,ETH', exchange=None, multiprice=False, full=False, avg=None, date=None):
        '''
                Get the latest price for a list of one or more currencies. Really fast, 20-60 ms. Cached each 10 seconds.
                Documentation at https://min-api.cryptocompare.com/.
                Examples:
                            https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=XMR,ETH,ZEC, REP
                            https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR&e=Coinbase
        '''
        if avg:
            url_for_request = self.url_generate_avg
            fs = 'fsym'
            ts = 'tsym'
        elif multiprice:
                url_for_request = self.url_pricemultifull if full else self.url_pricemulti
                fs = 'fsyms'
                ts = 'tsyms'
        elif date is not None:
            url_for_request = self.url_price_historical
            fs = 'fsym'
            ts = 'tsyms'

        else:
            url_for_request = self.url_price
            fs = 'fsym'
            ts = 'tsyms'

        #print(url_for_request)

        payload = {
            fs: from_currency,
            ts: to_currency,
            'e': exchange
        }

        r = requests.get(url_for_request, params=payload)
        print(r.url)

        return self.json_data_obtain(url=url_for_request, param=payload)

    def get_coin_pricemulti(self, from_currency='BTC', to_currency='KICK', exchange=None):
        '''
        Get a matrix of currency prices.
        :param from_currency:
        :param to_currency:
        :param exchange:
        :return:
        Examples:
                https://min-api.cryptocompare.com/data/pricemulti?fsyms=ETH,DASH,REP&tsyms=BTC,USD,EUR,XMR&e=Coinbase
                https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC,ETH&tsyms=USD
        '''
        print('get_coin_pricemulti')
        return self.get_coin_price(from_currency, to_currency, exchange, multiprice=True)

    def get_coin_pricemultifull(self, from_currency='BTC', to_currency='KICK', exchange=None):
        '''
        Get all the current trading info (price, vol, open, high, low etc) of any list of cryptocurrencies in any other currency that you need.
        If the crypto does not trade directly into the toSymbol requested, BTC will be used for conversion.
        This API also returns Display values for all the fields.If the opposite pair trades we invert it (eg.: BTC-XMR).
        :param from_currency:
        :param to_currency:
        :param exchange:
        :return:

        Examples:
                    https://min-api.cryptocompare.com/data/pricemultifull?fsyms=REP,ETH,DASH&tsyms=BTC,USD,EUR,XMR&e=Coinbase
                    https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH&tsyms=USD
        '''
        return self.get_coin_price(from_currency, to_currency, exchange, multiprice=True, full=True)

    def get_avg(self, from_currency='BTC', to_currency='USD', exchange='Bitfinex'):
        '''
        Compute the current trading info (price, vol, open, high, low etc) of the requested pair as a volume weighted average based on the markets requested.
        :param from_currency:
        :param to_currency:
        :param exchange:
        :return:

        Examples:
                https://min-api.cryptocompare.com/data/generateAvg?fsym=BTC&tsym=USD&e=Coinbase,Bitfinex
        '''

        return self.get_coin_price(from_currency, to_currency, exchange, avg=True)


    def get_dayAvg(self, ):
        '''
        Get day average price. The values are based on hourly vwap data and the average can be calculated in different waysIt uses BTC conversion if data is not available because the coin is not trading in the specified currency.
        If tryConversion is set to false it will give you the direct data. If no toTS is given it will automatically do the current day.
        Also for different timezones use the UTCHourDiff paramThe calculation types are: HourVWAP - a VWAP of the hourly close price,MidHighLow - the average between the 24 H high and low.
        VolFVolT - the total volume from / the total volume to (only avilable with tryConversion set to false so only for direct trades but the value should be the most accurate price)
        :return:
        '''

        pass

    def get_price_historical(self,from_currency,to_currency,date,exchange=None):
        ts = int(datetime.datetime.strptime(date, '%d/%m/%Y').timestamp())
        return self.get_coin_price(from_currency,to_currency,exchange,ts)




