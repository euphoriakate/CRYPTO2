import requests
import pprint
from collections import OrderedDict

#response = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC&tsyms=USD,EUR').json()
#pprint.pprint(response['RAW'])

i = 0
data_for_insert = []

all_coins = requests.get('https://min-api.cryptocompare.com/data/all/coinlist').json()
header = []

for key,data in all_coins['Data'].items():
    i = i + 1
    string = []



    coin_info = requests.get('https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id=' + data['Id']).json()
    #pprint.pprint(coin_info['Data']['General'].keys())
    #pprint.pprint(coin_info['Data']['General'])
    #pprint.pprint(all_coins['Data'][key])

    for k in coin_info['Data']['General'].keys():
        all_coins['Data'][key][k] = coin_info['Data']['General'][k]

    del (all_coins['Data'][key]['Sponsor'])
    if len(header) == 0:
        header = list(all_coins['Data'][key].keys())
        data_for_insert.append(header)

    #pprint.pprint(all_coins['Data'][key])

    for k in all_coins['Data'][key].keys():
        string.append(all_coins['Data'][key][k])


    data_for_insert.append(string)

    #pprint.pprint(all_coins['Data'][key])

    #print(data_for_insert)
    if i == 3:
        break

pprint.pprint(data_for_insert)

import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
json_key = json.load(open('ekaterina@prosphere.io#projectX'))
#pprint.pprint(json_key['client_email'])
scope = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('ekaterina@prosphere.io#projectX',scope)
#pprint.pprint(credentials)
gss_client = gspread.authorize(credentials)
doc = gss_client.open('dict_coin')

values = data_for_insert
range = 'A1:P2'
body = {
    'values': data_for_insert
}
param = { 'valueInputOption': 'RAW'}
doc.values_append(range = range, body=body, params=param)