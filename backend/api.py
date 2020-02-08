from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True

@app.route('/api/xml', methods=['GET'])
def get_xml():

    return {"success": False}

app.run(host='0.0.0.0')


#database of news websites (perhaps if they are trusted?)
#   related to a database for each site, containing article entries of:
    #   article identifier
    #   article embedding
    #   article publish timestamp
    #   logical clock of last access / timestamp of some kind (to keep track of eviction
            # do NoSQL databases do this without explicit entries?)

#will need to do
