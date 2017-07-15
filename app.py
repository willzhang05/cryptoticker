#!./env/bin/python3
import logging

import requests
from flask import Flask
from flask_ask import Ask, statement, question


ENDPOINT = 'https://api.coinmarketcap.com/v1/ticker/'

app = Flask(__name__)
ask = Ask(app, '/')
logger = logging.getLogger()


@ask.launch
def launch():
    speech = 'Please state coin type'
    logger.info('speech = {}'.format(speech))
    return statement(speech)


@ask.session_ended
def end():
    speech = 'Goodbye!'
    logger.info('speech = {}'.format(speech))
    return statement(speech)


@ask.intent('AMAZON.CancelIntent')(end)
@ask.intent('AMAZON.StopIntent')(end)
@ask.intent('AMAZON.HelpIntent')
def help():
    help_message = 'You can say tell me the price of a cryptocurrency, for example, bitcoin or ethereum. You can also say exit... What can I help you with?'
    help_reprompt = 'Sorry, I didn\'t get that. What coin are you interested in?'
    logger.info('question = {}, {}'.format(help_message, help_reprompt))
    return question(help_message).reprompt(help_reprompt)


@ask.intent('GetPriceIntent')
def get_price(coin):
    r = requests.get(ENDPOINT + coin)
    if r.status_code == 200:
        out = r.json()[0]
        speech = 'The market price of {} is currently {} US Dollars'.format(coin, out[
                                                                            'price_usd'])
    else:
        speech = 'Sorry, I don\'t know that coin'
    logger.info('speech = {}'.format(speech))
    return statement(speech)
