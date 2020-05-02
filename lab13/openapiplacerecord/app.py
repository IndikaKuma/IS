from flask import Flask
from flask_restful import Api
from flask_restful_swagger import swagger

from resources.place_record import PlaceRecord, PlaceRecords

app = Flask(__name__)

# Wrap the Api with swagger.docs. It is a thin wrapper around the Api class that adds some swagger smarts
api = swagger.docs(Api(app), apiVersion='0.1', description='API docs of Place Record Service')

api.add_resource(PlaceRecords, '/placerecords/', methods=['POST'])
api.add_resource(PlaceRecord, '/placerecords/<string:name>', methods=['GET', 'PUT', 'DELETE'])

app.run(host='0.0.0.0', port=5000, debug=True)
# In the context of servers, 0.0.0.0 can mean "all IPv4 addresses on the local machine".
