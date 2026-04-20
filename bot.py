import alpaca_trade_api as tradeapi
import time
import os

API_KEY = os.environ.get('ALPACA_API_KEY')
API_SECRET = os.environ.get('ALPACA_SECRET_KEY')
BASE_URL = 'https://paper-api.alpaca.markets'

api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

def get_position(symbol):
    try:
        return api.get_position(symbol)
    except:
        return None

def run_bot():
    symbol = 'SPY'
    print(f"Bot started. Trading {symbol}")
    
    while True:
        try:
            clock = api.get_clock()
            if not clock.is_open:
                print("Market closed. Waiting...")
                time.sleep(60)
                continue

            bars = api.get_bars(symbol, '1Day', limit=50).df
            short_ma = bars['close'].tail(10).mean()
            long_ma = bars['close'].tail(30).mean()
            
            position = get_position(symbol)
            
            if short_ma > long_ma and not position:
                api.submit_order(symbol=symbol, qty=1, side='buy',
                    type='market', time_in_force='day')
                print(f"BUY {symbol}")
                
            elif short_ma < long_ma and position:
                api.submit_order(symbol=symbol, qty=1, side='sell',
                    type='market', time_in_force='day')
                print(f"SELL {symbol}")

            time.sleep(300)
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

run_bot()
