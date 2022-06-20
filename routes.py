from flask import render_template, request, redirect, url_for
from app import app
import binance_client as bc
from gmail import *

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/registroUsuario')
def registro():
    return render_template('registroUsuario.html')

@app.route('/report', methods=('GET', 'POST'))
def report():

    if request.method == 'POST':
        report_type = request.form["report_type"]
        symbol = request.form["symbol"]

        if report_type == 'Order':
            return redirect(url_for('report_order', symbol=symbol))
        
        return redirect(url_for('report_coin_info', symbol=symbol))

    return render_template('report.html')


@app.route('/report/order/<symbol>')
def report_order(symbol):
    orders = bc.get_orders(symbol)

    return render_template('report_order.html', orders=orders)

@app.route('/report/coin_info/<symbol>')
def report_coin_info(symbol):
    coin_info = bc.get_symbol_info(symbol)

    return render_template('report_coin_info.html', coin_info=coin_info)

@app.route('/trade_long', methods=('GET', 'POST'))
def trade_long():

    if request.method == 'POST':
        symbol = request.form['symbol']
        entry_price = request.form['entry_price']
        ammount = request.form['ammount']
        tp = request.form['tp']
        sl = request.form['sl']

        bc.make_trade(symbol, entry_price, tp, sl)

        return render_template('trade_long.html')

    return render_template('trade_long.html')

@app.route('/tests')
def test():
    return render_template('tests.html', trades=bc.get_trades(), orders=bc.get_orders('BTCUSDT'), open_orders=bc.get_open_orders())