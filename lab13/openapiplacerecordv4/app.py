from flask import Flask
from flask_cors import CORS
from flask_restful_swagger_3 import Api

from resources.place_record import PlaceRecord, PlaceRecords

app = Flask(__name__)
CORS(app)
# Use the swagger Api class as you would use the flask restful class.
# It supports several (optional) parameters, these are the defaults:
api = Api(app, version='0.0', api_spec_url='/api/spec')

api.add_resource(PlaceRecords, '/placerecords/', methods=['POST'])
api.add_resource(PlaceRecord, '/placerecords/<string:name>', methods=['GET', 'PUT', 'DELETE'])

app.run(host='0.0.0.0', port=5000, debug=True)
# In the context of servers, 0.0.0.0 can mean "all IPv4 addresses on the local machine".
