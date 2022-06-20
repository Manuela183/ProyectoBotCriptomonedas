from binance.client import Client
import config

client = Client(config.API_KEY, config.SECRET_API_KEY)


def get_orders(symbol):
    orders = client.get_all_orders(symbol=symbol)
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


def get_symbol_info(symbol):
    info = client.get_symbol_info(symbol)
    return info


def get_account_info():
    account_info = client.get_account()
    return account_info


def get_futures_info():
    return client.futures_account()

def get_open_orders():
    return client.futures_get_open_orders(symbol='BTCUSDT')


def make_trade(symbol, entry_price, tp, sl):
    client.futures_change_leverage(symbol='BTCUSDT', leverage=config.LEVERAGE)

    client.futures_create_order(
        symbol=symbol,
        type='LIMIT',
        timeInForce='GTC',
        price=entry_price,
        side='BUY',
        quantity=0.001
    )

    client.futures_create_order(
        symbol=symbol,
        type='STOP_MARKET',
        side='SELL',
        stopPrice= float(entry_price) * 0.98,
        quantity=0.001
    )

    client.futures_create_order(
        symbol='BTCUSDT',
        type='TAKE_PROFIT_MARKET',
        side='SELL',
        stopPrice=float(entry_price) * 1.02,
        quantity=0.001
    )
