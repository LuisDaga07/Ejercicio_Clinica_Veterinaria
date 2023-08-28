
from flask import Flask, render_template, url_for,redirect, request, session
from flask_login import login_required

from db import mysql

from views.roles import roles

app = Flask(__name__)
app.secret_key="ejjd%&$76G$Eg"

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema_veterinario'
mysql.init_app(app)


app.register_blueprint(roles, url_prefix="/inicio")


@app.route('/', methods=['GET', 'POST'])  
def index():
      
    mesage = ''
    if request.method == 'POST' and 'txtMascota' in request.form and 'txtEdad' in request.form and 'txtRaza' in request.form and 'txtFecha' in request.form and 'txtHora' in request.form and 'txtAmo' in request.form:  
        _mascota = request.form['txtMascota']
        _edad = request.form['txtEdad']
        _raza = request.form['txtRaza']
        _fecha = request.form['txtFecha']
        _hora = request.form['txtHora']
        _amo = request.form['txtAmo']
        
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE fecha=%s AND hora=%s", (_fecha,_hora))
        cita = cursor.fetchone()
        if cita:
           mesage = 'Horario no Disponible, Por Favor Agende un Horario Disponible!'
        elif not _mascota or not _edad or not _raza or not _fecha or not _hora or not _amo:
           mesage = 'Todos los Campos son Requeridos !'
        else: 
           sql = 'INSERT INTO usuarios (id, mascota, edad, raza, fecha, hora, amo) VALUES (NULL, %s, %s, %s,%s,%s,%s)'
           datos = (_mascota, _edad, _raza, _fecha, _hora, _amo)
           
           conn= mysql.connect()
           cursor = conn.cursor()
           cursor.execute(sql,datos)
           conn.commit()    
           mesage = 'Su Cita ha Sido Agendada Satisfactoriamente !'          
    elif request.method == 'POST':
          mesage = 'Por Favor Llene Todos los Campos !'           
    return render_template('paginaWeb/index.html', mesage=mesage)

@app.route('/service')
def servicios():
    return render_template('paginaWeb/servicios.html')



@app.route('/lista_usuario')
def lista_u():
    
    if not 'loggedin' in session:
       return redirect(url_for('index'))
     
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM usuarios ")
    usuarios=cursor.fetchall()
    conn.commit()
    return render_template('admin/lista_user.html', usuarios=usuarios)

@app.route('/edit/<int:id>')
def edit(id):
    
    if not 'loggedin' in session:
        return redirect(url_for('index'))
    
    conn= mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id=%s", (id))
    usuarios = cursor.fetchall()
    conn.commit()
    
    return render_template('admin/editar.html', usuarios=usuarios)

@app.route('/update', methods=['POST'])
def update():
    
    _mascota = request.form['txtMascota']
    _edad = request.form['txtEdad']
    _raza = request.form['txtRaza']
    _fecha = request.form['txtFecha']
    _hora = request.form['txtHora']
    _amo = request.form['txtAmo']
    _id = request.form['txtID']
   
    sql ="UPDATE usuarios SET mascota=%s, edad=%s, raza=%s, fecha=%s, hora=%s, amo=%s WHERE id=%s ;"
   
    datos = (_mascota,_edad,_raza,_fecha,_hora,_amo,_id)
   
    conn= mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
   
    conn.commit()
    
    return redirect(url_for('lista_u'))  

@app.route("/destroy/<int:id>")
def destroy(id):
  conn= mysql.connect()
  cursor = conn.cursor()
  
  cursor.execute("DELETE FROM usuarios WHERE id=%s", (id))
  conn.commit()
  
  return redirect(url_for('lista_u')) 


if __name__ == '__main__':
    app.run(debug=True, port=3000)