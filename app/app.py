import logging
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Configura el logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    app.logger.info(f"Obteniendo datos para el usuario: {user_id}")
    
    try:
        shard_id = int(user_id) % 3  # Ejemplo de cálculo de shard basado en el user_id
        shard_file = f'shard{shard_id}.json'
        app.logger.debug(f"Shard ID: {shard_id}")
        app.logger.debug(f"Nombre de archivo del shard: {shard_file}")

        if os.path.exists(shard_file):
            with open(shard_file, 'r') as file:
                data = json.load(file)
                app.logger.debug(f"Datos cargados del shard: {data}")
                user_data = data.get(str(user_id))  # Asegúrate de convertir a string si es necesario
                if user_data:
                    app.logger.info(f"Datos encontrados para el usuario {user_id}: {user_data}")
                    return jsonify(user_data), 200
                else:
                    app.logger.warning(f"No se encontraron datos para el usuario {user_id}")
        else:
            app.logger.error(f"Archivo no encontrado: {shard_file}")
        
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener datos del usuario {user_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

