# Ruta para registrar un nuevo usuario
@app.route('/usuarios', methods=['POST'])
def add_usuario():
    data = request.get_json()
    nombre_usuario = data['nombre_usuario']
    nombre = data['nombre']
    email = data['email']
    contraseña = data['contraseña']
    telefono = data['telefono']
    edad = data['edad']
    ciudad = data['ciudad']

    connection = create_connection()
    cursor = connection.cursor()
    query = "INSERT INTO usuarios (nombre_usuario, nombre, email, contraseña, telefono, edad, ciudad) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (nombre_usuario, nombre, email, contraseña, telefono, edad, ciudad)

    try:
        cursor.execute(query, values)
        connection.commit()
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    except Error as e:
        print(f"Error: '{e}'")
        return jsonify({'message': 'Error al registrar el usuario'}), 500
    finally:
        cursor.close()
        connection.close()

# Ruta para obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM usuarios"

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return jsonify(result), 200
    except Error as e:
        print(f"Error: '{e}'")
        return jsonify({'message': 'Error al obtener los usuarios'}), 500
    finally:
        cursor.close()
        connection.close()

# Ruta para obtener un usuario por ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE id = %s"

    try:
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        if result:
            return jsonify(result), 200
        else:
            return jsonify({'message': 'Usuario no encontrado'}), 404
    except Error as e:
        print(f"Error: '{e}'")
        return jsonify({'message': 'Error al obtener el usuario'}), 500
    finally:
        cursor.close()
        connection.close()

# Ruta para actualizar un usuario por ID
@app.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    data = request.get_json()
    nombre_usuario = data['nombre_usuario']
    nombre = data['nombre']
    email = data['email']
    contraseña = data['contraseña']
    telefono = data['telefono']
    edad = data['edad']
    ciudad = data['ciudad']

    connection = create_connection()
    cursor = connection.cursor()
    query = """
        UPDATE usuarios
        SET nombre_usuario = %s, nombre = %s, email = %s, contraseña = %s, telefono = %s, edad = %s, ciudad = %s
        WHERE id = %s
    """
    values = (nombre_usuario, nombre, email, contraseña, telefono, edad, ciudad, id)

    try:
        cursor.execute(query, values)
        connection.commit()
        return jsonify({'message': 'Usuario actualizado exitosamente'}), 200
    except Error as e:
        print(f"Error: '{e}'")
        return jsonify({'message': 'Error al actualizar el usuario'}), 500
    finally:
        cursor.close()
        connection.close()

# Ruta para eliminar un usuario por ID
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    connection = create_connection()
    cursor = connection.cursor()
    query = "DELETE FROM usuarios WHERE id = %s"

    try:
        cursor.execute(query, (id,))
        connection.commit()
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
    except Error as e:
        print(f"Error: '{e}'")
        return jsonify({'message': 'Error al eliminar el usuario'}), 500
    finally:
        cursor.close()
        connection.close()
