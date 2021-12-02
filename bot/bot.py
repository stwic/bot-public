import ccxt
import config
import schedule
import pandas as pd
pd.set_option('display.max_rows', None)

import warnings
warnings.filterwarnings('ignore')

from datetime import datetime
import time

from buySignal import check_buy_sell_signals
from mongodb import cryptos
from supertrend import supertrend

exchange = ccxt.bitpanda({
    'apiKey': config.API_KEY
})

def run_bot(index):
    market = cryptos.find()[index]['key']
    print(f"Fetching new bars for {datetime.now().isoformat()}", market)
    bars = exchange.fetch_ohlcv(str(market) + '/EUR', timeframe='15m')
    df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    supertrend_data = supertrend(df)
    
    check_buy_sell_signals(supertrend_data, exchange, index, True)


for index in range(cryptos.count()):
    schedule.every(15).seconds.do(run_bot, index)

while True:
    schedule.run_pending()
    time.sleep(1)