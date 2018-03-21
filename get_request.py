import requests
import pprint



def get_request(request):
    response = requests.get(request).json()
    return response


def get_coin_list():
    coin_list_url = 'https://min-api.cryptocompare.com/data/all/coinlist'
    coin_list_url = get_request(coin_list_url)['Data']

