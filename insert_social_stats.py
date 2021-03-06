from DPCryptoCompare import DPCryptoCompare
from SHCryptoCompare import SHCryptoCompare
from Connector import Connector
import os
import getpass
import sys
import datetime


if __name__ == '__main__':

    import logging
    logging.basicConfig(filename=os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__)) + '/prosphero.log',
                        level=logging.DEBUG,
                        format='%(message)s')
    logging.info('\n' + str(datetime.datetime.now()) + ' Program started by ' + getpass.getuser() +
                 ' from directory ' + os.path.dirname(os.path.abspath(__file__)))
    conn = Connector('prosphero')  # set connection to database

    dp = DPCryptoCompare()

    CC_schema = SHCryptoCompare(conn, DPCryptoCompare())  # materialize schema CryptoCompare here
    CC_schema.insert_social_stats(social=['Twitter', 'Reddit', 'Facebook', 'CodeRepository'])
    conn.close()

    logging.info(str(datetime.datetime.now()) + ' Program ended an execution.')
