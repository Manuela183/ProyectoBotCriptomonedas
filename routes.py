from flask import render_template
from app import app
import binance_client as bc
from gmail import *

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/history')
def binance_history():
    orders = bc.get_orders()
    # balance = bc.get_balance()
    # trades = bc.get_trades()
    # deposits = bc.get_deposity_history()
    # info = bc.get_symbol_info()
    # account_info = bc.get_account_info()
    # futures = bc.get_futures_info()
    # # bc.make_trade()

    # gmail_order = get_tradingview_label_content()

    return render_template('binance_history.html', orders=orders)
    # , balance=balance, trades=trades, deposits=deposits, info=info, account_info=account_info, futures=futures, gmail_order=gmail_order