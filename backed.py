import json
from flask import Flask, request, jsonify
from bson.objectid import ObjectId
from bson import json_util
app = Flask(__name__)

headers = {"Content-Type": "application/json"}

@app.before_request
def before_request():
    # Abre la conexión antes de cada solicitud

@app.teardown_request
def teardown_request(exception=None):
    # Cierra la conexión después de cada solicitud


@app.route('/', methods=['GET', 'POST'])
def handle_requests():
    try:
        if request.method == 'GET':
            accion = request.args.get('accion', '')            
                
            if accion == "listaof":
                #aqui va la logica para esta accion GET
            elif accion == "lista":
                #otra
            else:
                return jsonify({'message': 'No hay datos'})                

        elif request.method == 'POST':
            data = request.json
            accion = data.get('accion','')
            if accion == "insert":
                #aqio va la logica para el POSt inser
            elif accion == "update":
                #otra
            else:
                return jsonify({'error': 'Tipo de operación no válida'}), 400
        else
            return jsonify({'error': 'No encuentra la página o recurso solicitado'}), 404                
    except Exception as e:
        # Manejar cualquier excepción aquí
        error_message = f"Error: {str(e)}"
        return jsonify({'error': error_message}), 500  # Código de estado 500 para errores internos del servidor

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
