from flask import Flask, render_template, request, redirect, url_for, flash, session
import oracledb
from datetime import date

app = Flask(__name__)
app.secret_key = 'Atom_2021'  # Cambia esto por una clave más segura

# Datos de conexión
def get_db_connection():
    return oracledb.connect(
        user="system",
        password="Atom",
        dsn="localhost/xe"
    )

@app.route('/')
def index():
    return render_template('index.html') # Página de inicio

@app.route('/login', methods=['GET', 'POST']) # Ruta para iniciar sesión
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre']
        contrasena = request.form['contrasena']
        
        try:
            conexion = get_db_connection()
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT * FROM usuarios WHERE nombre = :nombre AND contrasella = :contrasena
            """, {
                'nombre': nombre_usuario,
                'contrasena': contrasena
            })
            usuario = cursor.fetchone()
            cursor.close()
            conexion.close()
            
            if usuario:
                session['usuario_id'] = usuario[0]
                session['usuario_nombre'] = usuario[1]
                session['usuario_apellido'] = usuario[2]
                flash(f'¡Bienvenido, {usuario[1]} {usuario[2]}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Nombre de usuario o contraseña incorrectos', 'error')
        except Exception as e:
            flash(f'Error de conexión: {str(e)}', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido_p = request.form['apellido_p']
        apellido_m = request.form['apellido_m']
        correo = request.form['correo']
        telefono = request.form['telefono']
        contrasella = request.form['contrasella']
        
        try:
            conexion = get_db_connection()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO usuarios (nombre, apellido_p, apellido_m, correo, telefono, contrasella)
                VALUES (:nombre, :apellido_p, :apellido_m, :correo, :telefono, :contrasella)
            """, {
                'nombre': nombre,
                'apellido_p': apellido_p,
                'apellido_m': apellido_m,
                'correo': correo,
                'telefono': telefono,
                'contrasella': contrasella
            })
            conexion.commit()
            cursor.close()
            conexion.close()
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error al registrar usuario: {str(e)}', 'error')
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    # Obtener perros del usuario
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT * FROM perros WHERE usuario_id = :usuario_id
        """, {'usuario_id': session['usuario_id']})
        perros = cursor.fetchall()
        cursor.close()
        conexion.close()
    except Exception as e:
        perros = []
        flash(f'Error al cargar perros: {str(e)}', 'error')
    
    return render_template('dashboard.html', perros=perros)

@app.route('/perfil')
def perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT * FROM usuarios WHERE id = :id
        """, {'id': session['usuario_id']})
        usuario = cursor.fetchone()
        cursor.close()
        conexion.close()
        return render_template('perfil.html', usuario=usuario)
    except Exception as e:
        flash(f'Error al cargar perfil: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/registrar_perro', methods=['GET', 'POST'])
def registrar_perro():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nombre_perro = request.form['nombre']
        raza_perro = request.form['raza']
        edad_perro = request.form['edad']
        peso_perro = request.form['peso']
        
        try:
            conexion = get_db_connection()
            cursor = conexion.cursor()
            cursor.execute("""
                INSERT INTO perros (nombre, raza, edad, peso, usuario_id)
                VALUES (:nombre, :raza, :edad, :peso, :usuario_id)
            """, {
                'nombre': nombre_perro,
                'raza': raza_perro,
                'edad': edad_perro,
                'peso': peso_perro,
                'usuario_id': session['usuario_id']
            })
            conexion.commit()
            cursor.close()
            conexion.close()
            flash(f'Perro {nombre_perro} registrado exitosamente', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Error al registrar perro: {str(e)}', 'error')
    
    return render_template('registrar_perro.html')

@app.route('/pasear_perro/<int:perro_id>')
def pasear_perro(perro_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT * FROM perros WHERE id = :id AND usuario_id = :usuario_id
        """, {
            'id': perro_id,
            'usuario_id': session['usuario_id']
        })
        perro = cursor.fetchone()
        cursor.close()
        conexion.close()
        
        if perro:
            return render_template('pasear_perro.html', perro=perro)
        else:
            flash('Perro no encontrado', 'error')
            return redirect(url_for('dashboard'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/procesar_pago', methods=['POST'])
def procesar_pago():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    tipo_paseo = request.form['tipo_paseo']
    perro_id = request.form['perro_id']
    
    # Determinar el monto según el tipo de paseo
    montos = {'1': 10, '2': 20, '3': 30}
    monto = montos.get(tipo_paseo, 0)
    
    tipos_paseo = {
        '1': 'Paseo corto (30 minutos)',
        '2': 'Paseo largo (1 hora)',
        '3': 'Paseo especial (2 horas)'
    }
    
    try:
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO pagos (usuario_id, fecha, monto)
            VALUES (:usuario_id, :fecha, :monto)
        """, {
            'usuario_id': session['usuario_id'],
            'fecha': date.today(),
            'monto': monto
        })
        conexion.commit()
        cursor.close()
        conexion.close()
        
        flash(f'¡Pago procesado! {tipos_paseo[tipo_paseo]} - ${monto}', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        flash(f'Error al procesar pago: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
