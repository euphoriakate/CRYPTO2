import requests
import pprint
import DataPuller




class CryptoCompare(DataPuller):





    def get_coin_list():
        coin_list_url = 'https://min-api.cryptocompare.com/data/all/coinlist'
        coin_list = get_request(coin_list_url)['Data']
        return coin_list


    def get_price(from_currency = 'BTC', to_currency = 'USD'):

        if isinstance(list, to_currency):
            to_currency_string = ''
            for i in to_currency:
                if to_currency_string == '':
                    to_currency_string = to_currency_string + i
                else:
                    to_currency_string = to_currency_string + ',' + i

            price_url = 'https://min-api.cryptocompare.com/data/price?fsym=' + from_currency + '&tsyms=' + to_currency

        price_url = 'https://min-api.cryptocompare.com/data/price?fsym=' + from_currency + '&tsyms=' + to_currency
        print (price_url)
        price = get_request(price_url)
        return price

'''

https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD,EUR

https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD,EUR&extraParams=your_app_name

https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=XMR,ETH,ZEC&extraParams=your_app_name

https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=XMR,REP,ZEC&extraParams=your_app_name

https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR&e=Coinbase&extraParams=your_app_name
'''
#from_cur=None. to_cur=None. exchange_name=None

#https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD
#https://min-api.cryptocompare.com/data/price?fsym=BTC?tsyms=USD

#https://min-api.cryptocompare.com/data/price?fsym=BTC?tsyms=ETH