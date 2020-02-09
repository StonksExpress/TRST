from flask import Flask, request
from flask_cors import CORS
import json
import random
# import text_similarity as sim

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True

@app.route('/api/testSite', methods=['GET'])
def get():
    site = request.args.get("site")
    return {"trust": round(random.random(), 2), "reasons": ["site1", "site2", "site3"], "site": site}


app.run(host='0.0.0.0', port=80)
