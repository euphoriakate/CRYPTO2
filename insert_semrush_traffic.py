from DPSemrushTA import DPSEMRushTA
from Connector import Connector
import os
import getpass
import sys
from SHSemrushTA import SHSemrushTA
import datetime


if __name__ == '__main__':

    import logging
    logging.basicConfig(filename=os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__)) + '/prosphero.log',
                        level=logging.DEBUG,
                        format='%(message)s')
    logging.info('\n' + str(datetime.datetime.now()) + ' Program started by ' + getpass.getuser() +
                 ' from directory ' + os.path.dirname(os.path.abspath(__file__)))
    conn = Connector('prosphero')  # set connection to database

    SEMRushTA_dp = DPSEMRushTA()
    semrush_ta_schema = SHSemrushTA(connection=conn, data_puller=SEMRushTA_dp)
    semrush_ta_schema.insert_traffic_summary()

    conn.close()

    logging.info(str(datetime.datetime.now()) + ' Program ended an execution.')
