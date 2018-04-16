import logging
from collections import defaultdict
import datetime
import pprint
import inspect

logging.getLogger(__name__)


class SHCryptoCompare:

    def __init__(self, conn, data_puller=None):
        self.conn = conn
        self.schema = 'cryptocompare'
        self.schema_last_value = 'public'
        self.coin_table = 'coin'
        self.price_table = 'price'
        self.exchange_table = 'exchange'
        self.exchange_x_coin_table = 'exchange_x_coin'
        self.stats_twitter_table = 'coin_x_twitter'
        self.data_puller = data_puller
        self.max_tsyms_elem = 10
        self.social = ['CryptoCompare', 'Twitter', 'Reddit', 'Facebook', 'CodeRepository']
        self.coin_ident_type = ['id', 'code']

    def get_all_coins(self, type):
        if type in self.coin_ident_type:
            return self.conn.select(self.schema, self.coin_table, type)
        else:
            logging.error('Please call function ' + str(inspect.stack()[0][3]) + ' with proper value in type param ' + str(self.coin_ident_type))

    def insert_price(self, rows):
        columns = ('source_coin', 'target_coin', 'price')
        return self.conn.insert(self.schema, self.price_table, columns, rows)

    def insert_current_price(self, target_coin='BTC,USD'):

        coin_list = self.get_all_coins(type='code')  # load all coins codes from table with coins within this schema
        logging.info([coin[0] for coin in coin_list])
        j = 0
        tsyms_list = []  # dictionary with short coin list elements for insert to API url
        # filling dictionary tsyms_list
        while j < len(coin_list):
            last_cycle_elem = min(j + self.max_tsyms_elem, len(coin_list))
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

        tuple_list = []

        rows = ()
        for exchange in exchange_json:
            for source_coin in exchange_json[exchange]:
                for target_coin in exchange_json[exchange][source_coin]:
                    tuple_list.append((source_coin, target_coin))
                    row = (exchange, source_coin, target_coin)
                    rows = rows + (row,)

        """
        need to manually add all possible pairs source coin, target coin with CCCAGG
        for easy load aggregate full information in insert_exchange_x_coin function
        """

        tuple_set = set(tuple_list)
        manual_rows = [('CCCAGG',) + element for element in tuple_set]
        rows_all = rows + tuple(manual_rows)

        self.conn.insert(self.schema, self.exchange_table, columns, rows_all)

    def get_all_exchange_x_coin(self, exchange_list=None):
        columns = ['exchange_name', 'source_coin', 'target_coin']
        where = ''
        if exchange_list is not None:
            where = 'where exchange_name = \'' + exchange_list + '\''
        return self.conn.select(self.schema_last_value, self.exchange_table, columns, where)

    def insert_exchange_x_coin(self, exchange_list=None):
        exchange_x_coin = self.get_all_exchange_x_coin(exchange_list)  # return list of tuples
        pprint.pprint(exchange_x_coin)

        exchange_x_coin_json = defaultdict(dict)

        for row in exchange_x_coin:
            if row[2] in exchange_x_coin_json[row[0]].keys():
                exchange_x_coin_json[row[0]][row[2]].append(row[1])
            else:
                exchange_x_coin_json[row[0]][row[2]] = [row[1]]

        columns = (
            'exchange_name',
            'source_coin',
            'target_coin',
            'change24hour',
            'change_day',
            'change_pct24hour',
            'change_pct_day',
            'flags',
            'high24hour',
            'last_trade_id',
            'last_update',
            'last_volume',
            'last_volume_to',
            'low24hour',
            'market_cap',
            'open24hour',
            'price',
            'supply',
            'total_volume24h',
            'total_volume_24h_to',
            'type',
            'volume_24_hour',
            'volume_24_hour_to'
        )

        for exchange_name, coins in exchange_x_coin_json.items():
            fsyms_list = []
            for source_coin, target_coin_list in coins.items():
                j = 0
                while j < len(target_coin_list):
                    last_cycle_elem = min(j + self.max_tsyms_elem, len(target_coin_list))
                    fsyms = ','.join([x for x in target_coin_list[j:last_cycle_elem]])
                    j += self.max_tsyms_elem
                    fsyms_list.append(fsyms)

                    dat = self.data_puller.get_coin_pricemultifull(from_currency=fsyms, to_currency=source_coin,
                                                                   exchange=exchange_name)

                    rows = ()

                    for s_coin, t_coin_dict in dat.items():
                        for t_coin, attribute_dict in t_coin_dict.items():
                            row = (
                                attribute_dict['MARKET'],
                                attribute_dict['FROMSYMBOL'],
                                attribute_dict['TOSYMBOL'],
                                attribute_dict['CHANGE24HOUR'],
                                attribute_dict['CHANGEDAY'],
                                attribute_dict['CHANGEPCT24HOUR'],
                                attribute_dict['CHANGEPCTDAY'],
                                attribute_dict['FLAGS'],
                                attribute_dict['HIGH24HOUR'],
                                attribute_dict['LASTTRADEID'],
                                datetime.datetime.utcfromtimestamp(attribute_dict['LASTUPDATE']).strftime(
                                    '%Y-%m-%dT%H:%M:%S'),
                                attribute_dict['LASTVOLUME'],
                                attribute_dict['LASTVOLUMETO'],
                                attribute_dict['LOW24HOUR'],
                                attribute_dict['MKTCAP'],
                                attribute_dict['OPEN24HOUR'],
                                attribute_dict['PRICE'],
                                attribute_dict['SUPPLY'],
                                attribute_dict['TOTALVOLUME24H'],
                                attribute_dict['TOTALVOLUME24HTO'],
                                attribute_dict['TYPE'],
                                attribute_dict['VOLUME24HOUR'],
                                attribute_dict['VOLUME24HOURTO']
                            )
                            rows = rows + (row,)
                            print(row)


                    self.conn.insert(schema='cryptocompare', table='exchange_x_coin',
                                     columns=columns, data=rows)

    def insert_social_stats(self, social=None):

        if social == None:
            social = self.social
        elif isinstance(social,str):
            social = [social]

        coin_list_tuple = self.get_all_coins('id')
        coin_id_list = [str(x[0]) for x in coin_list_tuple]

        social_dict = {}
        new_dict = {}

        for coin_id in coin_id_list:
            data = self.data_puller.get_social_stats(coin_id)
            social_dict[coin_id] = data

            for scl in social:
                if scl not in new_dict.keys():
                    new_dict[scl] = {coin_id: data[scl]}
                else:
                    new_dict[scl][coin_id] = data[scl]

        pprint.pprint(new_dict)

        for scl in social:
            if scl == 'Twitter':
                self.insert_coin_x_twitter(new_dict[scl])
            if scl == 'Reddit':
                #self.insert_coin_x_reddit(new_dict[scl])
                pass

    def insert_coin_x_twitter(self, data):

        pprint.pprint('Twitter')
        columns = ('coin_id',
                   'followers',
                   'following',
                   'favourites',
                   'statuses',
                   'points',
                   'lists',
                   'account_create_dt',
                   'account_url')

        rows = ()

        for coin_id, value in data.items():
            row = (coin_id,
                   value['followers'],
                   value['following'],
                   value['favourites'],
                   value['statuses'],
                   value['Points'],
                   value['lists'],
                   datetime.datetime.utcfromtimestamp(int(value['account_creation'])).strftime(
                       '%Y-%m-%dT%H:%M:%S'),
                   value['link'])
            rows = rows + (row,)

        return self.conn.insert(schema=self.schema, table=self.stats_twitter_table, columns=columns, data=rows)

    def insert_coin_x_reddit(self, data):
        pprint.pprint('Reddit')
        pprint.pprint(data)




