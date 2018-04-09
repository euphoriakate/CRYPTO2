from DPSEMrush import DPSEMRush
from Connector import Connector
import pprint

if __name__ == '__main__':
    SEMRush_dp = DPSEMRush()
    data = SEMRush_dp.get_url_attendance().text
    rows_count = data.count('\n')

    rows = ()
    for i in range(1, rows_count):
        row = tuple((data.split('\n')[i].strip().split(';')))
        rows = rows + (row,)

    pprint.pprint(rows)
    conn = Connector('prosphero')  # set connection to database
    col = ('report_date', 'country' 'rank', 'organic_traffic', 'adwords_traffic')
    conn.insert('cryptocompare', 'exchange_attendance', col, rows)
    conn.close()