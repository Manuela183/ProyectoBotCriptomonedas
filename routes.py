from flask import render_template, request, redirect, url_for, flash, Response
from app import app, bcrypt
#import binance_client as bc
from gmail import *
from connection import get_db_connection
from fpdf import FPDF
import psycopg2.extras


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/report', methods=('GET', 'POST'))
def report():

    if request.method == 'POST':

        if 'generar' in request.form:
            return redirect(url_for('download_users'))

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
        password = request.form['password1']
        email = request.form['email']
        api = request.form['api']
        api_secret = request.form['api_secret']
        role = "usuario"

        hash = bcrypt.generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO usuario (nickname, password1, email, role, api, api_secret)' 'VALUES (%s,%s,%s,%s,%s,%s)',
                    (nickname, hash, email, role, api, api_secret))
        conn.commit()
        cur.close()
        conn.close()
        #return redirect(url_for('registro'))

    return render_template('registro_usuario.html')

@app.route('/editar_usuario')
def editar():
    pass

@app.route('/report/order/<symbol>')
def report_order(symbol):
    orders = bc.get_orders(symbol)

    for order in orders:
        order['side'] = 'Venta' if order['side'] == 'SELL' else 'Compra'

    return render_template('report_order.html', orders=orders)


@app.route('/report/order/download')
def download_users():
    try:
        conn = get_db_connection()
        print("1")
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM usuario")
        usuarios = cur.fetchall()

        pdf = FPDF()
        pdf.add_page()
        page_width = pdf.w - 2 * pdf.l_margin

        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(page_width, 0.0, 'Employee Data', align='C')
        pdf.ln(10)

        pdf.set_font('Courier', '', 12)
        col_width = page_width/4

        pdf.ln(1)
        th = pdf.font_size

        for usuario in usuarios:
            pdf.cell(col_width, th, str(usuario['id']), border=1)
            pdf.cell(col_width, th, str(usuario['nickname']), border=1)

        pdf.ln(10)

        pdf.set_font('Times', '', 10)
        pdf.cell(page_width, 0.0, '- end of report -', align='C')

        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=reporte_usuarios.pdf'})

    except Exception as e:
        print(e)

    finally:
        cur.close()
        conn.close()


@app.route('/report/coin_info/<symbol>')
def report_coin_info(symbol):
    coin_info = bc.get_symbol_info(symbol)

    return render_template('report_coin_info.html', coin_info=coin_info)


@app.route('/trade', methods=('GET', 'POST'))
def trade():

    if request.method == 'GET':
        print("dasdas")
        return render_template('trade.html')

    if request.method == 'POST':
        side = request.form['side']
        symbol = request.form['symbol']
        entry_price = request.form['entry_price']
        ammount = request.form['ammount']
        tp = int(request.form['tp']) / 100
        sl = int(request.form['sl']) / 100

        trade_successful = bc.make_trade(side, symbol, entry_price, tp, sl)

        if trade_successful:
            flash("La orden ha sido registrada con exito")
            type = 'Venta' if side == 'SELL' else 'Compra'
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO trades (tipo, moneda, precio_entrada, tomar_ganancias, detener_perdidas)' 'VALUES (%s,%s,%s,%s,%s)',
                        (type, symbol, entry_price, tp, sl))
            conn.commit()
            cur.close()
            conn.close()

        else:
            flash("Ha ocurrido un error en la orden")

        return render_template('trade.html')

    return render_template('trade.html')


@app.route('/tests')
def test():
    return render_template('tests.html', trades=bc.get_trades(), orders=bc.get_orders('BTCUSDT'), open_orders=bc.get_open_orders())
