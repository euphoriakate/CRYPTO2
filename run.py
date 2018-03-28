import pprint
from cryptoCompare import cryptoCompare
from Connector import Connector
from BD_Prosphero import Prosphero
import getpass
import datetime
import os



#logging.basicConfig(filename='prosphero.log', level=logging.DEBUG)
#logging.debug('This message should go to the log file')
#logging.info('So should this')
#logging.warning('And this, too')

if __name__ == '__main__':

    import logging
    logging.basicConfig(filename='prosphero.log', level=logging.DEBUG)
    logging.info('Program started by ' + getpass.getuser() + ' at ' + str(datetime.datetime.utcnow()) + ' from directory ' + os.path.dirname(os.path.abspath(__file__)))

    conn = Connector() #set connection to database
    '''
    bd = Prosphero(conn)
    coin_list = bd.get_all_coins()
    cryptoCompare = cryptoCompare()

    #tsyms_all = ','.join([str(x[0]) for x in coin_list])

    j = 0
    tsyms_list = []

    while j + 10 <= len(coin_list):
        tsyms = ','.join([str(x[0]) for x in coin_list[j:j+10]])
        j += 10
        tsyms_list.append(tsyms)

    print(tsyms_list)


    price_dict = []
    for tsyms in tsyms_list:
        data = cryptoCompare.get_coin_pricemulti(from_currency='BTC,USD', to_currency=tsyms)
        price_dict.append(data)


    rows = ()

    for price in price_dict:
        for source_coin_cd, target_coin_dict in price.items():
            for target_coin_cd, price in target_coin_dict.items():
                row = (source_coin_cd, target_coin_cd, price)
                rows = rows + (row,)

    pprint.pprint(rows)
    bd.insert_price(rows)

    conn.close()


    #date = '01/06/2017'
    #print(int(datetime.strptime(date, '%d/%m/%Y').timestamp()))

    #pprint.pprint(cryptoCompare.get_price_historical('USD', 'BTC,ETH', '06/04/2017'))

    '''

    logging.info('Program ended execution at ' + str(datetime.datetime.utcnow()) )
