import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handle_requests():
    try:
        if request.method == 'GET':
            valor = request.args.get('saludar', '')
            valor = f"Hola Mundo Get {valor}"
                
            # Crear un diccionario con la respuesta JSON
            response_data = {'mensaje': f"Respuesta para GET con datos: {valor}"}

            # Devolver la respuesta como JSON
            return jsonify(response_data)
        elif request.method == 'POST':
            data = request.form.get('campo')

            # Crear un diccionario con la respuesta JSON
            response_data = {'mensaje': f"Respuesta para POST con datos: {data}"}

            # Devolver la respuesta como JSON
            return jsonify(response_data)
    except Exception as e:
        # Manejar cualquier excepción aquí
        error_message = f"Error: {str(e)}"
        return jsonify({'error': error_message}), 500  # Código de estado 500 para errores internos del servidor

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)