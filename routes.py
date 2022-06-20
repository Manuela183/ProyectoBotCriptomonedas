from flask import Flask, render_template, request, redirect, url_for
from app import app
#import binance_client as bc
import os, psycopg2
from gmail import *
from connection import get_db_connection

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/history')
def binance_history():
    orders = bc.get_orders()
    balance = bc.get_balance()
    trades = bc.get_trades()
    deposits = bc.get_deposity_history()
    info = bc.get_symbol_info()
    account_info = bc.get_account_info()
    futures = bc.get_futures_info()
    # bc.make_trade()

    gmail_order = get_tradingview_label_content()

    return render_template('binance_history.html', orders=orders, balance=balance, trades=trades, deposits=deposits, info=info, account_info=account_info, futures=futures, gmail_order=gmail_order)



@app.route('/registro_usuario', methods=('GET', 'POST'))
def registro():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password1 = request.form['password1']
        email = request.form['email']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO usuario (nickname, password1, email)' 'VALUES (%s,%s,%s)', (nickname, password1, email))
        conn.commit()
        cur.close()
        conn.close()
        #return redirect(url_for('registro'))   

    return render_template('registro_usuario.html')


