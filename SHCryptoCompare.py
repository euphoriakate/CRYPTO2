import logging

logging.getLogger(__name__)


class SHCryptoCompare:

    def __init__(self, conn, data_puller=None):
        self.conn = conn
        self.schema = 'cryptocompare'
        self.coin_table = 'coin'
        self.price_table = 'price'
        self.exchange_table = 'exchange'
        self.data_puller = data_puller
        self.max_tsyms_elem = 10

    def get_all_coins(self):
        columns = ['code']
        return self.conn.select(self.schema, self.coin_table, columns)

    def insert_price(self, rows):
        columns = ('source_coin', 'target_coin', 'price')
        return self.conn.insert(self.schema, self.price_table, columns, rows)

    def insert_current_price(self, target_coin='BTC,USD'):

        coin_list = self.get_all_coins()  # load all coins codes from table with coins within this schema
        logging.info([coin[0] for coin in coin_list])
        j = 0
        tsyms_list = []  # dictionary with short coin list elements for insert to API url
        # filling dictionary tsyms_list
        while j <= len(coin_list):

            last_cycle_elem = min(j+self.max_tsyms_elem, len(coin_list))
            tsyms = ','.join([str(x[0]) for x in coin_list[j:last_cycle_elem]])
            j += self.max_tsyms_elem
            tsyms_list.append(tsyms)

        price_dict = []  # dictionary source_coin, target coin, price
        # filling dictionary price_dict
        for tsyms in tsyms_list:
            data = self.data_puller.get_coin_pricemulti(from_currency=tsyms, to_currency=target_coin)
            price_dict.append(data)

        rows = ()

        for price_row in price_dict:
            for source_coin_cd, target_coin_dict in price_row.items():
                for target_coin_cd, price in target_coin_dict.items():
                    row = (source_coin_cd, target_coin_cd, price)
                    rows = rows + (row,)
        self.insert_price(rows)

    def insert_exchange(self):
        columns = ('exchange_name', 'source_coin', 'target_coin')

        exchange_json = self.data_puller.get_exchange_info()

        rows = ()
        for exchange in exchange_json:
            for source_coin in exchange_json[exchange]:
                for target_coin in exchange_json[exchange][source_coin]:
                    row = (exchange, source_coin, target_coin)
                    if len(source_coin) >= 64 or len(target_coin) >= 64:
                        print(row)
                    rows = rows + (row,)
        #print(rows)
        self.conn.insert(self.schema, self.exchange_table, columns, rows)
