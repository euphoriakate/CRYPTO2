from Connector import Connector
import os
import getpass
import sys
from DPSemrushTA import DPSEMRushTA
import datetime
from SHSemrushTA import SHSemrushTA

if __name__ == '__main__':

    import logging
    logging.basicConfig(filename=os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__)) + '/prosphero.log',
                        level=logging.DEBUG,
                        format='%(message)s')
    logging.info('\n' + str(datetime.datetime.now()) + ' Program started by ' + getpass.getuser() +
                 ' from directory ' + os.path.dirname(os.path.abspath(__file__)))
    conn = Connector('prosphero')  # set connection to database

    SEMRushTA_dp = DPSEMRushTA()
    semrush_schema = SHSemrushTA(connection=conn, data_puller=SEMRushTA_dp)
    semrush_schema.insert_traffic_summary(api=False)
    # semrush_schema.insert_traffic_summary_history(api=False)

    conn.close()

    logging.info(str(datetime.datetime.now()) + ' Program ended an execution.')
