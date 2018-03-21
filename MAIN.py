import requests
import pprint
from collections import OrderedDict

response = requests.get('https://min-api.cryptocompare.com/data/all/coinlist').json()
#pairs = list(response.keys())
#pprint.pprint(pairs)
pprint.pprint(response['Data'].keys())
pprint.pprint(response['Data']['KICK'])
#data_ordered_dict = OrderedDict(sorted(response['Data'], key = lambda x:sorted(x.keys())))


#https://www.cryptocompare.com/api/data/coinlist/RRR
pprint.pprint(type(response['Data']))


import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
json_key = json.load(open('ekaterina@prosphere.io#projectX'))
pprint.pprint(json_key['client_email'])
scope = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('ekaterina@prosphere.io#projectX',scope)
pprint.pprint(credentials)
gss_client = gspread.authorize(credentials)
doc = gss_client.open('dict_coin')
#sheet.update_cell(2,3,'Blue')
#print(sheet.range('A1:A5'))
#pprint.pprint(sheet.get_all_records())
#pprint.pprint(sheet.get_all_values())
#sheet.append_row(['KEY', 'VALUE', 'WHATEVER'])
#sheet.append_row([])




#gss_client.open('dict_coin').batch_update(spreadsheetId = 'Sheet1', body = body)
#Id	Name	CoinName	FullName	Symbol	Algorithm	ProofType	IsTrading	PreMinedValue	FullyPremined	Sponsored	TotalCoinSupply	TotalCoinsFreeFloat	Url	ImageUrl	SortOrder
i = 0
#gss_client.open('dict_coin').values_append(range = 'A15:C30', body=body)
#sorted(response['Data'].items(), key=lambda x: x['Id'])
data_for_insert = []
for key,data in response['Data'].items():
    i = i + 1
    data_for_insert.append([data['Id'], data['Name'], data['CoinName'], data['FullName'], data['Symbol'], data['Algorithm'], data['ProofType'], data['IsTrading'], data['PreMinedValue'], data['FullyPremined'], data['Sponsored'], data['TotalCoinSupply'], data['TotalCoinsFreeFloat'], data['Url'], data['SortOrder']])

    #sheet.append_row([i, '1900-01-01 00:00:00', '9999-12-31 00:00:00', data['Name'], data['FullName'], data['Algorithm'], data['ProofType'], data['TotalCoinSupply'] ])
    #sheet.append_row([data['Id'], data['Name'], data['CoinName'], data['FullName'], data['Symbol'], data['Algorithm'], data['ProofType'], data['IsTrading'], data['PreMinedValue'], data['FullyPremined'], data['Sponsored'], data['TotalCoinSupply'], data['TotalCoinsFreeFloat'], data['Url'], data['ImageUrl'], data['SortOrder']])
    #if i == 5:
    #    break

values = data_for_insert
range = 'A2:P2'
body = {
    'values': data_for_insert
}
param = { 'valueInputOption': 'RAW'}
doc.values_append(range = range, body=body, params=param)