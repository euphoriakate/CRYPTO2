from DPSEMrush import DPSEMRush
from Connector import Connector
import pprint

from datetime import datetime

exchange_list = [
'https://www.binance.com/',
'https://upbit.com/',
'https://www.huobi.pro',
'https://bittrex.com',
'https://www.bithumb.com/',
'https://www.okex.com',
'https://bitsblockchain.com/',
'https://www.bitfinex.com',
'https://www.bit-z.com',
'https://www.gdax.com/',
'https://wex.nz/',
'https://www.kraken.com',
'https://poloniex.com',
'https://hitbtc.com',
'https://www.kucoin.com',
'https://www.bitstamp.net',
'https://bitflyer.jp/',
'https://exchange.btcc.com/',
'https://gemini.com/',
'https://www.itbit.com',
'https://www.bitmex.com/',
'https://coinone.co.kr/',
'https://exmo.com/'
]

if __name__ == '__main__':

    SEMRush_dp = DPSEMRush()

    for exc in exchange_list:
        data = SEMRush_dp.get_url_attendance(exc).text
        rows_count = data.count('\n')

        rows = ()
        for i in range(1, rows_count):
            list = data.split('\n')[i].strip().split(';')
            list[0] = str(datetime.strptime(list[0], '%Y%m%d'))
            row = tuple(list)
            rows = rows + (row,)

        pprint.pprint(rows)
        conn = Connector('prosphero')  # set connection to database
        col = ('report_date', 'country','domain', 'rank', 'organic_traffic', 'adwords_traffic')
        conn.insert('cryptocompare', 'exchange_attendance', col, rows)
        conn.close()

