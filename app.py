from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app) #Permite que el Fronted (Interfaz) se conecte sin bloqueos de seguridad

tareas = [] #BD

#Bienvenida
@app.route('/', methods = ['GET'])
def bienvenida():
    return jsonify("Bienvenido a la API")

#Leer todas las tareas
@app.route('/tareas',methods =['GET'])
def obtener_tarea():
    return jsonify({"tareas": tareas, "total": len(tareas)})

#Registrar
@app.route('/tareas',methods = ['POST'])
def agregar_tarea():
    nuevo = request.json
    tareas.append(nuevo)
    return jsonify({"mensaje":"Tarea Agregada"})

# Actualizar
@app.route('/tareas/<int:id>', methods=['PUT'])
def actualizar_tarea(id):
    datos_nuevos = request.json
    
    for tarea in tareas:
        # Verificamos que sea un diccionario y que el ID coincida
        if isinstance(tarea, dict) and tarea.get('id') == id:
            tarea['titulo'] = datos_nuevos.get('titulo', tarea.get('titulo', 'Sin título'))
            tarea['descripcion'] = datos_nuevos.get('descripcion', tarea.get('descripcion', ''))
            tarea['completada'] = datos_nuevos.get('completada', tarea.get('completada', False))
            return jsonify({"mensaje": "Tarea actualizada", "tarea": tarea})
            
    return jsonify({"error": "No se encontro la tarea"}), 404


#Eliminar
@app.route('/tareas/<int:id>',methods = ['DELETE'])
def eliminar_tarea(id):
    global tareas #Modificar la lista GLOBAL
    
    #Existe la tarea
    tarea_existe = any(isinstance(t, dict) and t.get('id') == id for t in tareas)
    
    if tarea_existe:
        #Filtrar la lista menos la que tenga el ID buscado
        tareas = [t for t in tareas if isinstance (t, dict) and t.get('id') != id]
        return jsonify({"mensaje": f"Tarea {id} eliminada correctamente"})
    
    return jsonify ({"mensaje":"Tarea no encontrada"})

if __name__ == '__main__':
    app.run(debug=True)
#Prueba de API