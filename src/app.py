from __future__ import annotations
import os
from datetime import date
from decimal import Decimal
import psycopg
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from psycopg.rows import dict_row

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'development-only-change-me')

def connect_db():
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        return psycopg.connect(database_url, row_factory=dict_row)
    return psycopg.connect(host=os.getenv('PGHOST','localhost'), port=os.getenv('PGPORT','5432'), dbname=os.getenv('PGDATABASE','hotel_db'), user=os.getenv('PGUSER','postgres'), password=os.getenv('PGPASSWORD','postgres'), row_factory=dict_row)

@app.get('/')
def index():
    with connect_db() as conn:
        reservas = conn.execute('SELECT * FROM vw_resumo_reservas ORDER BY data_checkin,id_reserva').fetchall()
        hospedes = conn.execute('SELECT id_hospede,nome,email,telefone FROM hospedes ORDER BY nome').fetchall()
    return render_template('index.html',reservas=reservas,hospedes=hospedes)

@app.post('/hospedes')
def cadastrar_hospede():
    nome=request.form.get('nome','').strip(); email=request.form.get('email','').strip(); telefone=request.form.get('telefone','').strip() or None
    if not nome or not email:
        flash('Nome e e-mail são obrigatórios.','erro'); return redirect(url_for('index'))
    try:
        with connect_db() as conn: conn.execute('INSERT INTO hospedes(nome,email,telefone) VALUES(%s,%s,%s)',(nome,email,telefone))
        flash('Hóspede cadastrado.','sucesso')
    except psycopg.Error as exc:
        flash('Não foi possível cadastrar: '+str(exc.diag.message_primary or exc),'erro')
    return redirect(url_for('index'))

@app.post('/reservas/valor')
def calcular_valor():
    try:
        checkin=date.fromisoformat(request.form['checkin']); checkout=date.fromisoformat(request.form['checkout']); diaria=Decimal(request.form['valor_diaria'])
        with connect_db() as conn: total=conn.execute('SELECT fn_calcular_valor_reserva(%s,%s,%s) AS total',(checkin,checkout,diaria)).fetchone()['total']
        flash(f'Prévia calculada pela Function: R$ {total:.2f}','sucesso')
    except (KeyError,ValueError,ArithmeticError,psycopg.Error) as exc:
        diag=getattr(exc,'diag',None); flash('Não foi possível calcular: '+str(getattr(diag,'message_primary',None) or exc),'erro')
    return redirect(url_for('index'))

@app.post('/reservas')
def criar_reserva():
    try:
        hospede_id=int(request.form['id_hospede']); checkin=date.fromisoformat(request.form['checkin']); checkout=date.fromisoformat(request.form['checkout']); diaria=Decimal(request.form['valor_diaria'])
        with connect_db() as conn: conn.execute('CALL sp_criar_reserva(%s,%s,%s,%s)',(hospede_id,checkin,checkout,diaria))
        flash('Reserva criada pela Procedure sp_criar_reserva.','sucesso')
    except (KeyError,ValueError,ArithmeticError,psycopg.Error) as exc:
        diag=getattr(exc,'diag',None); flash('Não foi possível criar a reserva: '+str(getattr(diag,'message_primary',None) or exc),'erro')
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(host='127.0.0.1',port=int(os.getenv('PORT','5000')),debug=False)
