import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# La URL del servicio Flask;
FLASK_SERVICE_URL = "http://flask_service:5000"

@app.route('/user/<user_id>', methods=['GET'])
def proxy_request(user_id):
    response = requests.get(f"{FLASK_SERVICE_URL}/user/{user_id}")
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
