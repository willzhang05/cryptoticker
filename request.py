#!./env/bin/python3
import requests
import json

ENDPOINT = 'https://api.coinmarketcap.com/v1/ticker/'

coin = "bitcoin"
r = requests.get(ENDPOINT + coin)
if r.status_code == 200:
    out = r.json()[0]
    print('The market price of ' + coin + ' is currently ' + out['price_usd'] + ' US Dollars')
else:
    print('Sorry, I don\'t know that coin')

