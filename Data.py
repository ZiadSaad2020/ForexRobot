import requests
from time import sleep
import pandas as pd
import json
from pandas.io.json import json_normalize
import Config

headers = {'Authorization' : 'Bearer ' + Config.api_token}
instruments = 'USD_CAD'
url_prices = 'https://api-fxpractice.oanda.com/v3/accounts/101-002-14506410-001/pricing?instruments='+instruments
historical_data = {}
iteration = 0
requesting = True
last_buy_price = 0
last_sell_price = 0

response = requests.get(url_prices,headers=headers).content
data = json.loads(response)
price_time = data['prices'][0]['time']
sell_price = data['prices'][0]['closeoutBid']
buy_price = data['prices'][0]['closeoutAsk']
currency_pair = data['prices'][0]['instrument']

historical_data['iteration'+str(iteration)]={
                'currencyPair':currency_pair,
                'buy':buy_price,
                'sell':sell_price,
                'time':price_time,
            }
with open('historicalData.txt','a') as txt_file:
    txt_file.write(
    '{0},{1},{2},{3},{4}\n'.format(iteration,currency_pair,price_time,sell_price,buy_price)
    )

data_df = pd.read_csv(Config.csv_file,names=['index','currency pair','time','sell','buy'],usecols=[1,2,3,4])

while requesting:
    try:
        iteration+=1
        response = requests.get(url_prices,headers=headers).content
        data = json.loads(response)
        price_time = data['prices'][0]['time']
        sell_price = data['prices'][0]['closeoutBid']
        buy_price = data['prices'][0]['closeoutAsk']
        currency_pair = data['prices'][0]['instrument']
        
        data_df = pd.read_csv(Config.csv_file,names=['index','currency pair','time','sell','buy'],usecols=[1,2,3,4])
        
        last_buy_price = data_df.buy.iat[-1]
        last_sell_price = data_df.sell.iat[-1]
        
        if data_df.empty:
            
            historical_data['iteration'+str(iteration)]={
                'currencyPair':currency_pair,
                'buy':buy_price,
                'sell':sell_price,
                'time':price_time,
            }
            with open('historicalData.txt','a') as txt_file:
                txt_file.write(
                '{0},{1},{2},{3},{4}\n'.format(iteration,currency_pair,price_time,sell_price,buy_price)
                )
            print('Iteration {0}: the last captured data has been saved'.format(iteration))
            
        elif buy_price != last_buy_price and sell_price != last_sell_price:
            historical_data['iteration'+str(iteration)]={
                'currencyPair':currency_pair,
                'buy':buy_price,
                'sell':sell_price,
                'time':price_time,
            }
            with open('historicalData.txt','a') as txt_file:
                txt_file.write(
                '{0},{1},{2},{3},{4}\n'.format(iteration,currency_pair,price_time,sell_price,buy_price)
                )
            print('Iteration {0}: Currency Pair: {1} Buy: {2} Sell: {3}'.format(iteration,currency_pair,buy_price,sell_price))

        else:
            print('Iteration {0}: No new changes since last captured price.'.format(iteration))
        
        print('\nRetrying in 30 seconds...')
             
        sleep(30)
        
    except Exception as e:
        print("Error: "+ str(e))
        
        


class getData():
    def __init__(self):
        pass
    
    