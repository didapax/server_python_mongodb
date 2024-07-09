import json
import pymongo
from flask import Flask, request, jsonify, g
from bson.objectid import ObjectId
from bson import json_util

app = Flask(__name__)

#Help server:
#Nota: el nombre de la coleccion es opcional si va dirigida los datos a varias colecciones de documentos
#GET: pueden existir los valores ?accion= que pueden ser ['lista','buscar'] &coleccion=
#GEt: si la accion es buscar deben incluir los valores de &campo=&valor= que seran el query a buscar
#POST: debe existir contentivo en la data JSON enviada desde el fronted {'coleccion':'data','tipo':'insert','data':data}
#Tipo puede ser ['insert','update','delete','auth']
#

@app.before_request
def before_request():
    # Abre la conexión antes de cada solicitud
    g.mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
    g.db = g.mongo_client["adan"]
    g.collection = None  # Inicializamos la colección como None

@app.teardown_request
def teardown_request(exception=None):
    # Cierra la conexión después de cada solicitud
    if hasattr(g, 'mongo_client'):
        g.mongo_client.close()

@app.route('/', methods=['GET', 'POST'])
def handle_requests():
    try:
        if request.method == 'GET':
            coleccion = request.args.get('coleccion', '')  # Obtener el valor de "coleccion" desde los datos
            accion = request.args.get('accion', '')            

            if coleccion:
                g.collection = g.db[coleccion]

            if accion == "listaof":
                limit = request.args.get('limit', '')
                sort = request.args.get('sort', '')
                campo = request.args.get('campo', '')
                valor = request.args.get('valor', '')
                Q_filter = {campo:valor}            
                count = g.collection.count_documents(Q_filter)
                if count > 0:
                    resultados = g.collection.find(Q_filter)
                    if limit:
                        resultados = g.collection.find(Q_filter).limit(int(limit))
                        
                    if sort:
                        paran = sort.split(',')
                        if paran[1] == "asc":
                            resultados = g.collection.find(Q_filter).sort(paran[0], pymongo.ASCENDING)
                        if paran[1] == "desc":
                            resultados = g.collection.find(Q_filter).sort(paran[0], pymongo.DESCENDING)                        
                        
                    json_data = json_util.dumps(resultados)
                    parsed_data = json.loads(json_data)
                    return jsonify(parsed_data)
                else:
                    return jsonify({'message': 'No hay datos'})

            if accion == "lista":
                limit = request.args.get('limit', '')
                sort = request.args.get('sort', '')            
                count = g.collection.count_documents({})
                if count > 0:
                    resultados = g.collection.find()
                    if limit:
                        resultados = g.collection.find().limit(int(limit))
                        
                    if sort:
                        paran = sort.split(',')
                        if paran[1] == "asc":
                            resultados = g.collection.find().sort(paran[0], pymongo.ASCENDING)
                        if paran[1] == "desc":
                            resultados = g.collection.find().sort(paran[0], pymongo.DESCENDING)                                            
                    
                    json_data = json_util.dumps(resultados)
                    parsed_data = json.loads(json_data)
                    return jsonify(parsed_data)
                else:
                    return jsonify({'message': 'No hay datos'})

            elif accion == "buscar":
                # Implementa la lógica para buscar
                campo = request.args.get('campo', '')
                valor = request.args.get('valor', '')
                Q_filter = {campo:valor}
                count = g.collection.count_documents(Q_filter)
                if count > 0:
                    resultado = g.collection.find_one(Q_filter)
                    resultado['_id'] = str(resultado['_id'])
                    return jsonify(resultado)
                else:
                    return jsonify({'message': 'No hay datos'})

            else:
                return jsonify({'message': 'Bienvenido Server Mongo'}), 400

        elif request.method == 'POST':
            data = request.json
            coleccion = data.get('coleccion', '')
            tipo = data.get('tipo', '')

            if coleccion:
                g.collection = g.db[coleccion]

            if tipo == "insert":
                # Implementa la lógica para insertar un documento
                datos = data.pop("tipo", None)
                datos = data.pop("coleccion", None)
                result = g.collection.insert_one(data)
                if result.inserted_count > 0:
                    mensaje = "insert exitoso"
                else:
                    mensaje = "insert fail"
                    
            if tipo == "insert_many":
                # Implementa la lógica para insertar multipes documentos
                datos = data.pop("tipo", None)
                datos = data.pop("coleccion", None)
                result = g.collection.insert_many(data)
                if result.inserted_count > 0:
                    mensaje = "insert exitoso"
                else:
                    mensaje = "insert fail"                    

            elif tipo == "update":
                # Implementa la lógica para actualizar un documento
                datos = data.pop("tipo", None)
                datos = data.pop("coleccion", None)
                result = g.collection.update_one(data)
                if result.modified_count > 0:
                    mensaje = "update exitoso"
                else:
                    mensaje = "update fail"

            elif tipo == "delete":            
                # Implementa la lógica para eliminar un documento
                datos = data.pop("tipo", None)
                datos = data.pop("coleccion", None)
                result = g.collection.delete_one(data)
                if result.deleted_count > 0:
                    mensaje = "update exitoso"
                else:
                    mensaje = "update fail"

            elif tipo == "auth":
                # Implementa la lógica de autenticación
                datos = data.pop("tipo", None)
                datos = data.pop("coleccion", None)
                usuario = data.get('usuario', '')
                password = data.get('password', '')
                Q_filter=({'usuario': usuario, 'password':password})
                count = g.collection.count_documents(Q_filter)
                if count > 0:
                    resultados = g.collection.find_one(Q_filter)
                    return jsonify(list(resultados))
                else:
                    return jsonify({'message': 'Usuario o Contraseña Errada'})                

            else:
                return jsonify({'error': 'Tipo de operación no válida'}), 400

            response_data = {'message': f"{mensaje}"}
            # Devolver la respuesta como JSON
            return jsonify(response_data)

    except Exception as e:
        # Manejar cualquier excepción aquí
        error_message = f"Error: {str(e)}"
        return jsonify({'error': error_message}), 500  # Código de estado 500 para errores internos del servidor

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
    
    
