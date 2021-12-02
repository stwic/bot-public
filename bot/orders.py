from slackbot.slackbot import trigger_slack_bot
import ccxt

def create_sell_order(exchange, market):
    amount = get_sell_amount(exchange, market)
    try:
        return exchange.create_market_sell_order(str(market) + '/EUR', amount)
    except ccxt.NetworkError as e:
        message = ' creating sell order failed due to a network error: '
        print(exchange.id, message, str(e))
        trigger_slack_bot(str(message + str(e) + str(market)))
        return False
        # retry or whatever
        # ...
    except ccxt.ExchangeError as e:
        message = ' creating sell order failed due to exchange error: '
        print(exchange.id, message, str(e))
        trigger_slack_bot(str(message + str(e) + str(market) + str(amount)))
        return False
        # retry or whatever
        # ...
    except Exception as e:
        message = ' creating sell order failed with exception error: '
        print(exchange.id, message, str(e))
        trigger_slack_bot(str(message + str(e) + str(market)))
        return False
        # retry or whatever
        # ...

def create_buy_order(exchange, market):
    amount = get_buy_amount(exchange, market)
    try:
        return exchange.create_market_buy_order(str(market) + '/EUR', amount)
    except ccxt.NetworkError as e:
        message = ' creating buy order failed due to a network error: '
        print(exchange.id, message, str(e))
        trigger_slack_bot(str(message + str(e) + str(market)))
        return False
        # retry or whatever
        # ...
    except ccxt.ExchangeError as e:
        message = ' creating buy order failed due to exchange error: '
        print(exchange.id, message, str(e))
        trigger_slack_bot(str(message + str(e) + str(market) + str(amount)))
        return False
        # retry or whatever
        # ...
    except Exception as e:
        message = ' creating buy order failed with exception error: '
        print(exchange.id, message, str(e))
        trigger_slack_bot(str(message + str(e) + str(market)))
        return False
        # retry or whatever
        # ...


def get_buy_amount(exchange, market):
    balance = exchange.fetch_balance()
    ticker = exchange.fetch_ticker(str(market) + '/EUR')
    fee = (balance['EUR']['free'] * 0.1500 / 100)
    return (balance['EUR']['free'] - fee) / ticker['last']

def get_sell_amount(exchange, market):
    balance = exchange.fetch_balance()
    return balance[str(market)]['free']
