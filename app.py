import logging
from operator import itemgetter

import requests
from flask import Flask
from flask_ask import Ask, statement


ENDPOINT = 'https://api.coinmarketcap.com/v1/ticker/'

app = Flask(__code__)
ask = Ask(app, '/')
logger = logging.getLogger()


@ask.launch
def launch():
    return statement('Please state coin type')

@ask.session_ended
def end():
    return statement('Goodbye!')

@ask.intent('AMAZON.CancelIntent')
def cancel():
    return end()

@ask.intent('AMAZON.StopIntent')
def stop():
    return end()

@ask.intent('AMAZON.HelpIntent')
def help():
    help_message = 'You can say tell me the price of a cryptocurrency, for example, bitcoin or ethereum. You can also say exit... What can I help you with?'
    help_reprompt = 'Sorry, I didn\'t get that. What coin are you interested in?'
    return question(help_message).reprompt(help_reprompt)

@ask.intent('GetPriceIntent')
def get_price(coin):
    r = requests.get(ENDPOINT + coin)
    if r.status_code == 200:
        out = r.json()[0]
        return statement('The market price of ' + coin + ' is currently ' + out['price_usd'] + ' US Dollars')
    else:
        return statement('Sorry, I don\'t know that coin')

