from flask import Flask, jsonify
from flask_cors import CORS

from datetime import datetime

from settings import MY_ENV_VAR

app = Flask(__name__)
CORS(app)


@app.route('/hello', methods=['GET'])
def hello():
    results = {'date': datetime.now().strftime("%b %d %Y %H:%M:%S"), 'env_variable': MY_ENV_VAR}
    return jsonify(results)
