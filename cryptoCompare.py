import requests
import pprint



def get_request(request):
    response = requests.get(request).json()
    return response


def get_coin_list():
    coin_list_url = 'https://min-api.cryptocompare.com/data/all/coinlist'
    coin_list = get_request(coin_list_url)['Data']
    return coin_list


def get_price(from_currency = 'BTC', to_currency = None):
    price_url = 'https://min-api.cryptocompare.com/data/price/fsym=' + from_currency
    print (price_url)
    price = get_request(price_url)['Data']
    return price

'''

https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD,EUR

https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD,EUR&extraParams=your_app_name

https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=XMR,ETH,ZEC&extraParams=your_app_name

https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=XMR,REP,ZEC&extraParams=your_app_name

https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR&e=Coinbase&extraParams=your_app_name
'''
#from_cur=None. to_cur=None. exchange_name=None