from DPSemrush import DPSEMRush
from DPCryptoCompare import DPCryptoCompare
from SHCryptoCompare import SHCryptoCompare
from Connector import Connector
import os
import getpass
import sys
from SHSemrush import SHSemrush
import datetime
import pprint


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
    CC_schema.insert_social_stats(social=['CodeRepository'])
    conn.close()

    logging.info(str(datetime.datetime.now()) + ' Program ended an execution.')

'''
('5301', 'undefined', 'undefined', None, None, None, 0, 0, 'undefined', 'undefined', 'undefined', 0, -1, '', '', -1, '', '')
coin_id,url,language,created_dt,last_push_dt,last_update_dt,subscribers,stars,size,open_issues,open_pull_issues,open_total_issues,closed_issues,closed_pull_issues,closed_total_issues,fork,forks,parent_internal_id,parent_internal_name,parent_internal_url,source_internal_id,source_internal_name,source_internal_url
%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
'''