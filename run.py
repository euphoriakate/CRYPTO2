import pprint
from cryptoCompare import cryptoCompare


#pprint.pprint(cryptoCompare_old.get_price(from_currency='ETH', to_currency='KICK'))

if __name__ == '__main__':
    cryptoCompare = cryptoCompare()
    #pprint.pprint(cryptoCompare.get_coin_info())
    #pprint.pprint(cryptoCompare.get_coin_price('BTC', 'USD', 'CoinBase'))
    #pprint.pprint(cryptoCompare.get_coin_multiprice('BTC,ETH,LTC', 'USD,KICK'))
    #pprint.pprint(cryptoCompare.get_coin_pricemultifull())
    pprint.pprint(cryptoCompare.get_avg('ETH', 'BTC', exchange='Kraken'))


