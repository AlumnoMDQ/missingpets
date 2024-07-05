from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Recuerda usar una clave secreta fuerte en producción

# Configuración de la base de datos
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='missingpets'
        )
    except Error as e:
        print(f"Error: '{e}'")
    return connection

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        nombre = request.form['nombre']
        email = request.form['email']
        contraseña = generate_password_hash(request.form['contraseña'])  # Encriptar la contraseña
        telefono = request.form['telefono']
        edad = request.form['edad']
        ciudad = request.form['ciudad']
        is_admin = request.form.get('is_admin', False)  # Obtiene el valor del checkbox (True o False)
        is_active = request.form.get('is_active', True)  # Obtiene el valor del checkbox (True o False)

        connection = create_connection()
        
        if connection is None:
            flash('Error de conexión a la base de datos')
            return redirect(url_for('registro'))

        cursor = connection.cursor()

        try:
            query = "INSERT INTO usuarios (nombre_usuario, nombre, email, contraseña, telefono, edad, ciudad, is_admin, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (nombre_usuario, nombre, email, contraseña, telefono, edad, ciudad, is_admin, is_active)
            cursor.execute(query, values)
            connection.commit()
            flash('Usuario registrado exitosamente')
            return redirect(url_for('home'))
        except Error as e:
            print(f"Error al ejecutar la consulta SQL: {e}")
            flash(f"Error al registrar el usuario: {e}")
            connection.rollback()  # Revertir cualquier cambio en caso de error
            return redirect(url_for('registro'))
        finally:
            cursor.close()
            connection.close()

    return render_template('registro.html')

# Ruta para la página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contraseña = request.form['contraseña']

        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM usuarios WHERE nombre_usuario = %s"
        values = (nombre_usuario,)

        cursor.execute(query, values)
        usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario['contraseña'], contraseña):
            session['nombre_usuario'] = usuario['nombre_usuario']
            session['usuario_id'] = usuario['id']
            session['logged_in'] = True
            return redirect(url_for('mostrar_formulario_crearmascota'))
        else:
            return jsonify({'message': 'Nombre de usuario o contraseña incorrectos'}), 401

    return render_template('login.html')


        

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Ruta para la página de crear mascotas
@app.route('/crearmascotas')
def crearmascotas():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))  # Redirige a login si no está logeado
    return render_template('crearmascotas.html')

# Función para añadir una nueva mascota
@app.route('/mascotas', methods=['POST'])
def add_mascota():
    data = request.get_json()
    nombre = data['nombre']
    tipo = data['tipo']
    raza = data['raza']
    color = data['color']
    edad = data['edad']
    descripcion = data['descripcion']
    estado = data['estado']
    usuario_id = data['usuario_id']

    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO mascotas (nombre, tipo, raza, color, edad, descripcion, estado, usuario_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (nombre, tipo, raza, color, edad, descripcion, estado, usuario_id)

    try:
        cursor.execute(query, values)
        connection.commit()
        return jsonify({'message': 'Mascota registrada exitosamente'}), 201
    except Error as e:
        print(f"Error: '{e}'")
        return jsonify({'message': 'Error al registrar la mascota'}), 500
    finally:
        cursor.close()
        connection.close()

# Ruta para obtener todas las mascotas
@app.route('/mascotas', methods=['GET'])
def get_mascotas():
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM mascotas"

    try:
        cursor.execute(query)
        mascotas = cursor.fetchall()
        return jsonify(mascotas), 200
    except Error as e:
        print(f"Error: '{e}'")
        return jsonify({'message': 'Error al obtener las mascotas'}), 500
    finally:
        cursor.close()
        connection.close()

# Ruta para actualizar una mascota por su ID
@app.route('/mascotas/<int:id>', methods=['PUT'])
def update_mascota(id):
    data = request.get_json()
    nombre = data['nombre']
    tipo = data['tipo']
    raza = data['raza']
    color = data['color']
    edad = data['edad']
    descripcion = data['descripcion']
    estado = data['estado']
    usuario_id = data['usuario_id']

    connection = create_connection()
    cursor = connection.cursor()
    query = "UPDATE mascotas SET nombre=%s, tipo=%s, raza=%s, color=%s, edad=%s, descripcion=%s, estado=%s, usuario_id=%s WHERE id=%s"
    values = (nombre, tipo, raza, color, edad, descripcion, estado, usuario_id, id)

    try:
        cursor.execute(query, values)
        connection.commit()
        return jsonify({'message': 'Mascota actualizada exitosamente'}), 200
    except Error as e:
        print(f"Error: '{e}'")
        return jsonify({'message': 'Error al actualizar la mascota'}), 500
    finally:
        cursor.close()
        connection.close()

# Ruta para eliminar una mascota por su ID
@app.route('/mascotas/<int:id>', methods=['DELETE'])
def delete_mascota(id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "DELETE FROM mascotas WHERE id=%s"
    
    try:
        cursor.execute(query, (id,))
        connection.commit()
        return jsonify({'message': 'Mascota eliminada exitosamente'}), 200
    except Error as e:
        print(f"Error: '{e}'")
        return jsonify({'message': 'Error al eliminar la mascota'}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
