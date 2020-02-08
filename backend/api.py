from flask import Flask, request
from flask_cors import CORS
import json
import text_similarity.py as sim

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True

@app.route('/api/xml', methods=['GET'])
def get_xml():
    url = request.args.get('url')

    return {"success": False}

app.run(host='0.0.0.0')
