#!./env/bin/python3
import logging

import requests
from flask import Flask
from flask_ask import Ask, request, statement, question


ENDPOINT = 'https://api.coinmarketcap.com/v1/ticker/'

app = Flask(__name__)
ask = Ask(app, '/')
logger = logging.getLogger()


@ask.session_ended
def end():
    speech = 'Goodbye!'
    logger.info('speech = {}'.format(speech))
    return statement(speech)


ask.intent('AMAZON.CancelIntent')(end)
ask.intent('AMAZON.StopIntent')(end)


@ask.intent('AMAZON.HelpIntent')
def help():
    help_message = 'You can say tell me the price of a cryptocurrency, for example, bitcoin or ethereum. You can also say exit... What can I help you with?'
    help_reprompt = 'Sorry, I didn\'t get that. What would you like me to do?'
    logger.info('question = {}, {}'.format(help_message, help_reprompt))
    return question(help_message).reprompt(help_reprompt)

ask.launch(help)


@ask.intent('GetPriceIntent', default={'coin': 'NULL'})
def get_price(coin):
    print(request)
    if coin == 'NULL':
        error_message = 'Please specify a cryptocurrency... What can I help you with?'
        error_reprompt = 'What would you like me to do?'
        logger.info('question = {}, {}'.format(error_message, error_reprompt))
        return question(error_message).reprompt(error_reprompt)

    r = requests.get(ENDPOINT + coin)
    if r.status_code == 200:
        out = r.json()[0]
        speech = 'The market price of {} is currently {} US Dollars'.format(coin, out[
                                                                            'price_usd'])
        logger.info('speech = {}'.format(speech))
        return statement(speech).simple_card(
            title='Price of ' + coin,
            content='$' + out['price_usd'] + ' USD')
    else:
        error_message = 'Sorry, I don\'t know that coin. You can try a different coin or you can also say exit... What can I help you with?'
        error_reprompt = 'What would you like me to do?'
        logger.info('question = {}, {}'.format(error_message, error_reprompt))

        return question(error_message).reprompt(error_reprompt)
