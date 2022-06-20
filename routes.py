from flask import render_template, request, redirect, url_for, flash
from app import app
import binance_client as bc
from gmail import *
from connection import get_db_connection


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/report', methods=('GET', 'POST'))
def report():

    if request.method == 'POST':
        report_type = request.form["report_type"]
        symbol = request.form["symbol"]
       
        if report_type == 'Order':
            return redirect(url_for('report_order', symbol=symbol))

        return redirect(url_for('report_coin_info', symbol=symbol))

    return render_template('report.html')


@app.route('/registro_usuario', methods=('GET', 'POST'))
def registro():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password1 = request.form['password1']
        email = request.form['email']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO usuario (nickname, password1, email)' 'VALUES (%s,%s,%s)',
                    (nickname, password1, email))
        conn.commit()
        cur.close()
        conn.close()
        #return redirect(url_for('registro'))

    return render_template('registro_usuario.html')


@app.route('/report/order/<symbol>')
def report_order(symbol):
    orders = bc.get_orders(symbol)

    for order in orders:
        if order['side'] == 'SELL':
            order['side'] = 'Venta'
        else:
            order['side'] = 'Compra'

    return render_template('report_order.html', orders=orders)


@app.route('/report/coin_info/<symbol>')
def report_coin_info(symbol):
    coin_info = bc.get_symbol_info(symbol)

    return render_template('report_coin_info.html', coin_info=coin_info)


@app.route('/trade', methods=('GET', 'POST'))
def trade():

    if request.method == 'POST':
        side = request.form['side']
        symbol = request.form['symbol']
        entry_price = request.form['entry_price']
        ammount = request.form['ammount']
        tp = int(request.form['tp']) / 100
        sl = int(request.form['sl']) / 100

        print(tp, sl)

        trade_successful = bc.make_trade(side, symbol, entry_price, tp, sl)

        if trade_successful:
            flash("La orden ha sido registrada con exito")
        else:
            flash("Ha ocurrido un error en la orden")

        return render_template('trade.html')

    return render_template('trade.html')


@app.route('/tests')
def test():
    return render_template('tests.html', trades=bc.get_trades(), orders=bc.get_orders('BTCUSDT'), open_orders=bc.get_open_orders())
