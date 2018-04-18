from DPSemrush import DPSEMRush
from Connector import Connector
import os
import getpass
import sys
from SHSemrush import SHSemrush
import datetime


if __name__ == '__main__':

    import logging
    logging.basicConfig(filename=os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__)) + '/prosphero.log',
                        level=logging.DEBUG,
                        format='%(message)s')
    logging.info('\n' + str(datetime.datetime.now()) + ' Program started by ' + getpass.getuser() +
                 ' from directory ' + os.path.dirname(os.path.abspath(__file__)))
    conn = Connector('prosphero')  # set connection to database

    SEMRush_dp = DPSEMRush()
    semrush_schema = SHSemrush(connection=conn, data_puller=SEMRush_dp)
    semrush_schema.insert_keyword_search_volume()
    semrush_schema.insert_url_attendace()

    conn.close()

    logging.info(str(datetime.datetime.now()) + ' Program ended an execution.')
