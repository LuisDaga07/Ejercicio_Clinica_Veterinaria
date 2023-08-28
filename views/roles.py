from db import mysql
from flask import Flask, Blueprint, flash, render_template, request, redirect, url_for, session
from flask_login import current_user, logout_user, login_required

import re


roles = Blueprint("roles_bp", __name__)


@roles.route('/inicio')
def inicio():
    
    if not 'loggedin' in session:
         return redirect(url_for('index'))
    
    return render_template('admin/admin.html')

@roles.route('/register', methods=['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'txtEmail' in request.form and 'txtPassword' in request.form and 'txtUsuario' in request.form:
        
        email = request.form['txtEmail']
        usuario = request.form['txtUsuario']
        password = request.form['txtPassword']
        conn= mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admin WHERE email = %s', (email))
        account = cursor.fetchone()
        if account:
           mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
           mesage = 'Invalid email address!'
        elif not email or not password or not usuario:
           mesage = 'Please fill out the form ! '
        else:
            sql = 'INSERT INTO admin (id, email, usuario, password) VALUES (NULL, %s, %s,%s)'         
            datos = (email, usuario, password)
            
            conn= mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql,datos)
            conn.commit()
            return redirect(url_for('roles_bp.login', mesage = 'you have successfully registered !'))
    elif request.method == 'POST':
        mesage = 'Please fill out the form'      
    return render_template('admin/register.html', mesage=mesage)
 
@roles.route('/login_', methods=['GET', 'POST'])
def login():
    
    mesage = ''
    if request.method == 'POST' and 'txtEmail' in request.form and 'txtPassword' in request.form:
        _password = request.form['txtPassword']
        _email = request.form['txtEmail']
        conn= mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM  admin WHERE email =%s AND password =%s ", (_email, _password,))
        user = cursor.fetchone() 
        if user:
            session['loggedin'] = True
            session[ 'id' ] = user[0]
            session[ 'email' ] = user[ 1 ]
            session[ 'password' ] = user[ 3 ]
            mesage = 'logged in successfully'
            return render_template('admin/admin.html', mesage=mesage)
        else:
            mesage = 'Please enter correct email address or password !'
    return render_template('admin/login.html', mesage=mesage)

@roles.route('/logout')
def logout():
    session.clear()
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return render_template('paginaWeb/index.html')  

@roles.route('/admin')
def admin():
    
    if not 'loggedin' in session:
       return redirect(url_for('index'))
   
    return render_template('admin/admin.html')   


