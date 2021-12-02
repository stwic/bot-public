from config import sell_percent
from slackbot.slackbot import trigger_slack_bot
from mongodb import cryptos

from orders import create_sell_order, create_buy_order

def check_buy_sell_signals(df, exchange, index, triSupertrend):
    crypto = cryptos.find()[index]
    market = crypto['key']
    highestPrice = 0
    
    
    ticker = exchange.fetch_ticker(str(market) + '/EUR')
    high = ticker['high']
    last = ticker['last']
    
    if high >= highestPrice:
        highestPrice = high
    
    last_row_index = len(df.index) - 1
    previous_row_index = last_row_index - 1
    
    uptrend = not df['in_uptrend'][previous_row_index] and df['in_uptrend'][last_row_index]
    downtrend = last < highestPrice and (highestPrice - last) / highestPrice * 100 > sell_percent
    print((highestPrice - last) / highestPrice * 100)
    
    if uptrend:
        if not check_any_in_position():
            order = create_buy_order(exchange, market)
            if order:
                trigger_slack_bot('created buy order at: ' +  str(df['open'][last_row_index]) + str(order))
                cryptos.update_one({'_id': crypto['_id']}, {'$set': {'in_position': True}})
    
    else:
        if downtrend and crypto['in_position']:
            order = create_sell_order(exchange, market)
            if order:
                trigger_slack_bot('created sell order at: ' +  str(df['open'][last_row_index]) + str(order))
                cryptos.update_one({'_id': crypto['_id']}, {'$set': {'in_position': False}})

def check_any_in_position():
    return any(x['in_position'] == True for x in cryptos.find())