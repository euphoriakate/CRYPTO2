from DPCryptoCompare import DPCryptoCompare
from Connector import Connector
from SHCryptoCompare import SHCryptoCompare
import getpass
import datetime
import os
import sys


if __name__ == '__main__':

    import logging

    logging.basicConfig(filename=os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__)) + '/prosphero.log',
                        level=logging.DEBUG,
                        format='%(message)s')
    logging.info('\n' + str(datetime.datetime.now()) + ' Program started by ' + getpass.getuser() +
                 ' from directory ' + os.path.dirname(os.path.abspath(__file__)))

    conn = Connector('prosphero')  # set connection to database

    CC_schema = SHCryptoCompare(conn, DPCryptoCompare())  # materialize schema CryptoCompare here
    CC_schema.insert_exchange()
    ''' insert actual exchange - trade pair info. This step is necessary before insert_exchange_x_coin step,
        because after we need to write explicity actual pair in api request'''

    CC_schema.insert_exchange_x_coin()

    conn.close()

    logging.info(str(datetime.datetime.now()) + ' Program ended an execution.')
