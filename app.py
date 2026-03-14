from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

tareas = [] #BD

#Leer
@app.rouyte('/tareas',methods =['GET'])
def obtener_tarea():
    return jsonify(tareas)

#Registrar
@app.route('/tareas',methods = ['POST'])
def agregar_tarea():
    nuevo = request.json
    tareas.append(nuevo)
    return jsonify({"mensaje":"Tarea Agregada"})

#Actualizar
@app.route('/tareas/<int:id>',methods = ['PUT'])
def actualizar_tarea(id):
    tareas[id] = request.json
    return jsonify ({"mensaje":"Tarea eliminada"})

#Eliminar
@app.route('/tareas/<int:id>',methods = ['DELETE'])
def eliminar_tarea(id):
    tareas.pop[id]
    return jsonify ({"mensaje":"Tarea eliminada"})

if __name__ == '__main__':
    app.run(debug=True)
#Prueba de API