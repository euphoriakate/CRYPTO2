class Prosphero:

    def __init__(self, conn):
        self.conn = conn
        self.schema = 'cryptocompare'
        self.coin_table = 'coin'
        self.price_table = 'price'

    def get_all_coins(self):
        columns = ['code']
        return self.conn.select(self.schema, self.coin_table, columns)

    def insert_price(self, rows):
        columns = ('source_coin', 'target_coin', 'price')
        return self.conn.insert(self.schema, self.price_table, columns, rows)