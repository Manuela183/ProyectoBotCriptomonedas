from binance.client import Client
import config

client = Client(config.API_KEY, config.SECRET_API_KEY)


def get_orders():
    orders = client.get_all_orders(symbol='BTCUSDT')
    return orders

def get_balance():
    balance = client.get_asset_balance(asset='BTC')
    return balance

def get_trades():
    trades = client.get_my_trades(symbol='BTCUSDT')
    return trades

def get_deposity_history():
    deposits = client.get_deposit_history()
    return deposits

def get_symbol_info():
    info = client.get_symbol_info('BTCUSDT')
    return info

def get_account_info():
    account_info = client.get_account()
    return account_info

def get_futures_info():
    return client.futures_account()

# def make_trade():
#     client.futures_change_leverage(symbol='BTCUSDT', leverage=config.LEVERAGE)

#     client.futures_create_order(
#         symbol='BTCUSDT',
#         type='MARKET',
#         side='BUY',
#         quantity=0.001
#     )
