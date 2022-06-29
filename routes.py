from flask import render_template, request, redirect, url_for, flash, Response, session
from app import app, bcrypt
import binance_client as bc
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

            if 'role' in session and session['role'] == 'administrador':
                report_type_pdf = request.form["report_type_pdf"]
                if report_type_pdf == 'users':

                    return redirect(url_for('download_users'))

                return redirect(url_for('download_orders'))
            else:

                flash("Debe ser administrador para poder generar este reporte")

                return render_template('report.html')

        report_type = request.form["report_type"]
        symbol = request.form["symbol"]

        if 'id' in session:
            if report_type == 'Order':
                return redirect(url_for('report_order', symbol=symbol))

            return redirect(url_for('report_coin_info', symbol=symbol))
        else:
            flash('Debe iniciar sesión para poder generar reportes')
            return render_template('report.html')

    return render_template('report.html')


@app.route('/registro_usuario', methods=('GET', 'POST'))
def registro():
    if request.method == 'POST':
        nickname = str(request.form['nickname'])
        password = str(request.form['password1'])
        email = str(request.form['email'])
        api = str(request.form['api'])
        api_secret = str(request.form['api_secret'])
        role = "usuario"

        bandera = False

        hash = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT id FROM usuario WHERE nickname='{}'".format(nickname))

            exists = cur.fetchall()

            if not exists:
                cur.execute('INSERT INTO usuario (nickname, password1, email, role, api, api_secret)' 'VALUES (%s,%s,%s,%s,%s,%s)',
                            (nickname, hash, email, role, api, api_secret))

                bandera = True

        except (Exception, psycopg2.Error) as error:
            print("Error al guardar usuario en la base de datos", error)

        finally:
            conn.commit()
            cur.close()
            conn.close()

        if bandera:
            flash('Se ha registrado con exito')
            return redirect(url_for('iniciar_sesion'))
        else:
            flash('Nickname ingresado ya existe')
            return redirect(url_for('registro'))

    return render_template('registro_usuario.html')


@app.route('/inicio_sesion', methods=('GET', 'POST'))
def iniciar_sesion():

    if request.method == 'POST':
        nickname = request.form['nickname']
        password1 = request.form['password1']

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('''SELECT password1, id, role FROM usuario
                        WHERE nickname=%s''', (nickname,))

            usuario = cur.fetchall()

            if usuario:
                hash = bcrypt.check_password_hash(usuario[0][0], password1)

                if hash:
                    session['id'] = usuario[0][1]
                    session['role'] = usuario[0][2]

        except (Exception, psycopg2.Error) as error:
            print("Error al obtener datos de la base de datos", error)

        finally:
            cur.close()
            conn.close()

        if 'id' in session:
            flash("Ha iniciado sesión con exito")
            return redirect(url_for('index'))
        else:
            flash(
                "Ha ocurrido un error en el inicio de sesión, verifique nickname y contraseña")

    return render_template('inicio_sesion.html')


@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('id', None)
    session.pop('role', None)

    flash('Se ha cerrado sesión con exito')

    return redirect(url_for('index'))


@app.route('/editar_user', methods=('GET', 'POST'))
def editar():

    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password1']
        email = request.form['email']
        api = request.form['api']
        api_secret = request.form['api_secret']
        hash = bcrypt.generate_password_hash(password).decode('utf-8')
        bandera = True
        try:
                conn = get_db_connection()
                cur = conn.cursor()

                cur.execute('''
            UPDATE usuario
              SET nickname = %s,
                password1 = %s,
                email = %s,
                api = %s,
                api_secret = %s
             WHERE id = %s
            ''', (nickname, hash, email, api, api_secret, session['id']))

        except (Exception, psycopg2.Error) as error:
                bandera = False
                flash("Error al intentar editar")
                print("Error al obtener datos de la base de datos", error)
                return render_template('editar_usuario.html')
        finally:
                conn.commit()
                cur.close()
                conn.close()

        if bandera:
            flash('Se a editado de forma exitosa')
            return render_template('index.html')

        flash('Error en la toma de datos')
        return render_template('index.html')
        
    else:
        if 'id' in session:
            id = session['id']
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute('''SELECT * FROM usuario WHERE id = {}'''.format(id))

            usuario_edit = cur.fetchone()

            return render_template('editar_usuario.html', usuario_edit=usuario_edit)
        else:
            flash("Deberá iniciar sesión primero")
            return render_template('index.html')


@app.route('/report/order/<symbol>')
def report_order(symbol):

    try:
        bandera = True
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''SELECT api, api_secret FROM usuario
                    WHERE id=%s''', (session['id'],))

        data = cur.fetchall()
        api = (data[0][0], data[0][1])

        client = bc.init_client(api[0], api[1])

        orders = bc.get_orders(symbol, client)

        for order in orders:
            order['side'] = 'Venta' if order['side'] == 'SELL' else 'Compra'

    except:
        flash("Error en credenciales de la api")
        bandera = False

    finally:
        cur.close()
        conn.close()

    if bandera:
        return render_template('report_order.html', orders=orders)

    return render_template('report.html')


@app.route('/report/users/download')
def download_users():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM usuario")
        usuarios = cur.fetchall()

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)

        pdf.multi_cell(w= 0, h= 7, txt='REPORTE DE USUARIOS', border=1, align='C', fill=0)
        pdf.ln(0.25)
        pdf.cell(w= 20, h= 8, txt='ID', border=1, align='C', fill=0)

        pdf.cell(w= 50, h= 8, txt='Nombre', border=1, align='C', fill=0)

        pdf.multi_cell(w= 0, h= 8, txt='Correo', border=1, align='C', fill=0)

        for usuario in usuarios:
            pdf.cell(20, 8, str(usuario['id']), border=1)
            pdf.cell(50, 8, str(usuario['nickname']), border=1)
            pdf.multi_cell(0, 8, str(usuario['email']), border=1)

        pdf.ln(10)

        pdf.set_font('Times', '', 10)

        pdf.cell(0, 0.0, '- end of report -', align='C')

        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=reporte_usuarios.pdf'})

    except Exception as e:
        print("Error en la creacion del pdf", e)

    finally:
        cur.close()
        conn.close()


@app.route('/report/order/download')
def download_orders():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM trades")
        ordenes = cur.fetchall()

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)

        pdf.multi_cell(w= 0, h= 7, txt='REPORTE DE ORDENES', border=1, align='C', fill=0)
        pdf.ln(0.25)
        pdf.cell(w= 12, h= 8, txt='ID', border=1, align='C', fill=0)

        pdf.cell(w= 50, h= 8, txt='Preciodeentrada', border=1, align='C', fill=0)
        pdf.cell(w= 33, h= 8, txt='Moneda', border=1, align='C', fill=0)
        pdf.cell(w= 57, h= 8, txt='Detener las perdidas', border=1, align='C', fill=0)

        pdf.multi_cell(w= 0, h= 8, txt='Tipo', border=1, align='C', fill=0)

        for ordenes in ordenes:
            pdf.cell(12, 8, str(ordenes['id']), border=1)
            pdf.cell(50, 8, str(ordenes['precio_entrada']), border=1)
            pdf.cell(33, 8, str(ordenes['moneda']), border=1)
            pdf.cell(57, 8, str(ordenes['detener_perdidas']), border=1)
            pdf.multi_cell(0, 8, str(ordenes['tipo']), border=1)

        pdf.ln(10)

        pdf.set_font('Times', '', 10)

        pdf.cell(0, 0.0, '- end of report -', align='C')

        return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition': 'attachment;filename=reporte_ordenes.pdf'})

    except Exception as e:
        print("Error en la creacion del pdf", e)

    finally:
        cur.close()
        conn.close()


@app.route('/report/coin_info/<symbol>')
def report_coin_info(symbol):
    try:
        bandera = True
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''SELECT api, api_secret FROM usuario
                    WHERE id=%s''', (session['id'],))

        data = cur.fetchall()
        api = (data[0][0], data[0][1])

        client = bc.init_client(api[0], api[1])

        coin_info = bc.get_symbol_info(symbol, client)

    except:
        flash("Error en credenciales de la api")
        bandera = False

    finally:
        cur.close()
        conn.close()

    if bandera:
        return render_template('report_coin_info.html', coin_info=coin_info)

    return render_template('report.html')


@app.route('/trade', methods=('GET', 'POST'))
def trade():

    if request.method == 'POST':

        if 'id' in session:

            side = request.form['side']
            symbol = request.form['symbol']
            entry_price = request.form['entry_price']
            ammount = request.form['ammount']
            tp = int(request.form['tp']) / 100
            sl = int(request.form['sl']) / 100

            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute('''SELECT api, api_secret FROM usuario
                            WHERE id=%s''', (session['id'],))

                data = cur.fetchall()
                api = (data[0][0], data[0][1])

                client = bc.init_client(api[0], api[1])
                trade_successful = bc.make_trade(side, symbol, entry_price, tp, sl, client)

                if trade_successful:
                    flash("La orden ha sido registrada con exito")

                    type = 'Venta' if side == 'SELL' else 'Compra'
                    cur.execute('INSERT INTO trades (tipo, moneda, precio_entrada, tomar_ganancias, detener_perdidas)' 'VALUES (%s,%s,%s,%s,%s)',
                                (type, symbol, entry_price, tp, sl))

                    conn.commit()

                else:
                    flash("Ha ocurrido un error en la orden")

            except:
                flash("Error en credenciales de la api")

            finally:
                cur.close()
                conn.close()

        else:
            flash('Debe iniciar sesión para poder crear ordenes')

        return render_template('trade.html')

    return render_template('trade.html')

@app.route('/cancelar_ordenes', methods=('GET', 'POST'))
def cancelar_ordenes():

    if request.method == 'POST':

        if 'id' in session:
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute('''SELECT api, api_secret FROM usuario
                            WHERE id=%s''', (session['id'],))

                data = cur.fetchall()
                api = (data[0][0], data[0][1])
                client = bc.init_client(api[0], api[1])
                open_orders = bc.get_open_orders(client)
                print(len(open_orders))
                
                for order in open_orders:
                    print(order['orderId'])
                    print(bc.cancel_orders(client, order['orderId']))

            except:
                pass

        

    return render_template('trade.html')

