import requests
import pprint
from collections import OrderedDict

response = requests.get('https://min-api.cryptocompare.com/data/all/coinlist').json()

i=0
data_for_insert = []
for key,data in response['Data'].items():
    i = i + 1
    data_for_insert.append([key, data['Id'], data['Name'], data['CoinName'], data['FullName'], data['Symbol'], data['Algorithm'], data['ProofType'], data['IsTrading'], data['PreMinedValue'], data['FullyPremined'], data['Sponsored'], data['TotalCoinSupply'], data['TotalCoinsFreeFloat'], data['Url'], data['SortOrder']])
    if i ==5:
        break


pprint.pprint(data_for_insert)