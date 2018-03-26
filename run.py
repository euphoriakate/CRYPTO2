import pprint
from cryptoCompare import cryptoCompare
import psycopg2
from config import config
from datetime import datetime
from Connector import Connector
from BD_Prosphero import Prosphero

'''
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        cur.execute('SELECT * from cryptocompare.coin order by id desc')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


#pprint.pprint(cryptoCompare_old.get_price(from_currency='ETH', to_currency='KICK'))

def insert_vendor(data):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO cryptocompare.coin(id, code, short_name, full_name, algorithm, proof_type, is_trading, premined_value, fully_premined, total_coin_supply, total_coins_free_float, sponsored, url)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"""
    conn = None
    vendor_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, data)
        # get the generated id back
        #vendor_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
'''

if __name__ == '__main__':


    conn = Connector()

    bd = Prosphero(conn)
    coin_list = bd.get_all_coins()
    cryptoCompare = cryptoCompare()

    tsyms = ','.join([str(x[0]) for x in coin_list])

    print(tsyms)
    print(len(tsyms))

    price = cryptoCompare.get_coin_pricemulti(from_currency='BTC,USD', to_currency=tsyms)
    #pprint.pprint(cryptoCompare.get_coin_pricemulti(from_currency='BTC,USD', to_currency=tsyms))
    pprint.pprint(price)

    #make data for insert

    for source_coin_cd, target_coin_dict in price.items():
        for target_coin_cd, price in target_coin_dict.items():
            row = (source_coin_cd, target_coin_cd, price)
            bd.insert_price(row)

    conn.close()


    #date = '01/06/2017'
    #print(int(datetime.strptime(date, '%d/%m/%Y').timestamp()))

    #pprint.pprint(cryptoCompare.get_price_historical('USD', 'BTC,ETH', '06/04/2017'))

    #insert_string = (data['Id'], key, data['CoinName'])
    #pprint.pprint(cryptoCompare.get_coin_info())
    #pprint.pprint(cryptoCompare.get_coin_price('BTC', 'USD', 'CoinBase'))
    #pprint.pprint(cryptoCompare.get_coin_pricemulti('BTC,USD', 'ETH,KICK'))
    #pprint.pprint(cryptoCompare.get_coin_pricemultifull())
    #pprint.pprint(cryptoCompare.get_avg('ETH', 'BTC', exchange='Kraken'))

    #host = "localhost", database = "suppliers", user = "postgres", password = "postgres"

    #pprint.pprint(conn)
    #connect()
    #insert_vendor()

    #print(datetime.today())




    '''
    cryptoCompare = cryptoCompare()
    coin_json = cryptoCompare.get_coin_info()
    for key, data in coin_json.items():
        data = (data['Id'], key, data['CoinName'], data['FullName'], data['Algorithm'], data['ProofType'], data['PreMinedValue'], data['FullyPremined'], data['TotalCoinSupply'], data['TotalCoinsFreeFloat'], data['Sponsored'], data['Url'])
        print(data)
        conn.insert(schema='cryptocompare',table='coin', data=data)
    '''

