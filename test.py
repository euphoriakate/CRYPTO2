from DPCryptoCompare import DPCryptoCompare
from Connector import Connector
from SHCryptoCompare import SHCryptoCompare
import getpass
import datetime
import os
import sys
import pprint
from DataPuller import DataPuller

'''
cc = DPCryptoCompare()
data = cc.get_exchange_info()
#pprint.pprint(data)


for exchange in data:
    for source_coin in data[exchange]:
        for target_coin in data[exchange][source_coin]:
            print(exchange, source_coin, target_coin)
'''

conn = Connector('prosphero')  # set connection to database

CC_schema = SHCryptoCompare(conn, DPCryptoCompare())  # materialize schema CryptoCompare here
#CC_schema.insert_exchange()

url = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms=AID&tsyms=BTC,USD,ETH&e=Bitfinex'
dp = DataPuller()
val = dp.json_data_obtain(url)['RAW']
#d = CC_schema.get_all_exchange_x_coin()
#pprint.pprint(d)
d = CC_schema.insert_exchange_x_coin()
pprint.pprint(d)
#print(d['Tidex'])
# pprint.pprint(val)


conn.close()
