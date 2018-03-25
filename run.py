import pprint
from cryptoCompare import cryptoCompare
import psycopg2
from config import config
from datetime import datetime

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


if __name__ == '__main__':
    #cryptoCompare = cryptoCompare()
    #pprint.pprint(cryptoCompare.get_coin_info())
    #pprint.pprint(cryptoCompare.get_coin_price('BTC', 'USD', 'CoinBase'))
    #pprint.pprint(cryptoCompare.get_coin_multiprice('BTC,ETH,LTC', 'USD,KICK'))
    #pprint.pprint(cryptoCompare.get_coin_pricemultifull())
    #pprint.pprint(cryptoCompare.get_avg('ETH', 'BTC', exchange='Kraken'))

    #host = "localhost", database = "suppliers", user = "postgres", password = "postgres"

    #pprint.pprint(conn)
    #connect()
    #insert_vendor()

    #print(datetime.today())
    data = (769483,'ILT', 'iOlite', 'iOlite (ILT)', 'Ethash', 'PoW',  None, None, None, 1000000000, None, 0, '/coins/ilt/overview')
#{"Id":"769483","Url":"/coins/ilt/overview","ImageUrl":"/media/27010772/iqt.png","Name":"ILT","Symbol":"ILT","CoinName":"iOlite","FullName":"iOlite (ILT)","Algorithm":"Ethash","ProofType":"PoW","FullyPremined":"0","TotalCoinSupply":"1000000000","PreMinedValue":"N/A","TotalCoinsFreeFloat":"N/A","SortOrder":"2288","Sponsored":false}}
    #insert_vendor(data)
    connect()