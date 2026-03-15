import sqlite3
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app) #Permite que el Fronted (Interfaz) se conecte sin bloqueos de seguridad

DATABASE = "tareas.db" #BD

def conectar_bd():
    conexion  = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row #Accede a los datos por nombre de columna
    return conexion

#Crea una tabla
def crear_tabla():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            completada BOOLEAN DEFAULT 0
        )
    ''')
    conexion.commit()
    conexion.close()
    
crear_tabla() #Ejecutamos la creacion al encender el servidor

#Bienvenida
@app.route('/', methods = ['GET'])
def bienvenida():
    return jsonify("Bienvenido a la API")

#Leer todas las tareas
@app.route('/tareas',methods =['GET'])
def obtener_tareas():
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM tareas")
    
    #Convertir las filas de la BD en una lista de diccionarios
    filas = cursor.fetchall()
    lista_tareas = [dict(fila) for fila in filas]
    conexion.close
    return jsonify({"tareas": lista_tareas, "total": len(lista_tareas)})

#Registrar
@app.route('/tareas',methods = ['POST'])
def agregar_tarea():
    nuevo = request.json
    titulo = nuevo.get('titulo')
    descripcion = nuevo.get('descripcion')
    completada = nuevo.get('completada', False)
    
    #Validar que almenos este el titulo
    if not titulo:
        return jsonify({"Error": "El titulo es obligatorio"}), 400
    
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        #Insertamos los datos.El ID se genera en automatico
        cursor.execute('''
            INSERT INTO tareas (titulo, descripcion, completada) 
            VALUES (?, ?, ?)
        ''', (titulo, descripcion, completada))
        
        conexion.commit()
        nuevo_id = cursor.lastrowid #Id generado por la BD
        conexion.close
        
        return jsonify({
            "mensaje": "Tarea agregada",
            "id_asignado": nuevo_id
        }),  201
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

# Actualizar
@app.route('/tareas/<int:id>', methods=['PUT'])
def actualizar_tarea(id):
    datos_nuevos = request.json
    
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        #Verificamos que la tarea exista
        cursor.execute("SELECT * FROM tareas WHERE id= ?", (id,))
        tarea = cursor.fetchone()
        
        if tarea is None:
            conexion.close()
            return jsonify({"error": "No se encontro la tarea con ese ID"}), 404
            
        #Extraemos datos nuevos
        nuevo_titulo = datos_nuevos.get('titulo', tarea ['titulo'])
        nueva_descripcion = datos_nuevos.get('descripcion', tarea ['descripcion'])
        nueva_comp = datos_nuevos.get('completada', tarea ['completada'])
        
        #Ejecutamos la acutalizacion de datos
        cursor.execute('''
                UPDATE tareas
                SET titulo = ?, descripcion = ?, completada = ?
                WHERE id= ?''',(nuevo_titulo, nueva_descripcion, nueva_comp, id))
        
        conexion.commit()
        conexion.close()
        
        return jsonify({"mensaje": "Tarea actualizada existosamente,", "id": id})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#Eliminar
@app.route('/tareas/<int:id>',methods = ['DELETE'])
def eliminar_tarea(id):
    
    try:
        conexion = conectar_bd()
        cursor = conexion.cursor()
        
        cursor.execute("DELETE FROM tareas WHERE id = ?", (id,))
        
        #cursor.rowcount me dice cuantas filas se borraron
        
        if cursor.rowcount == 0:
            conexion.close()
            return jsonify({"error": "No se encontro la tarea a eliminar"}), 404
        conexion.commit()
        conexion.close()
        
        return jsonify({"mensaje": f"Tarea {id} eliminada correctamente"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
#Prueba de API