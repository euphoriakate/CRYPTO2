from DPCryptoCompare import DPCryptoCompare
from Connector import Connector
from SHCryptoCompare import SHCryptoCompare
import getpass
import datetime
import os
import sys
import pprint

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
CC_schema.insert_exchange()

conn.close()
