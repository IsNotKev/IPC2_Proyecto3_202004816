from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json 
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def rutaInicial():
    return ('Kevin Steve Martinez Lemus - 202004816')

if __name__ == "__main__":
    app.run(debug=True)