from flask import Flask
from flask_restful import Api

from resources.place_record import PlaceRecord, PlaceRecords

app = Flask(__name__)
api = Api(app)

api.add_resource(PlaceRecords, '/placerecords/', methods=['POST'])
api.add_resource(PlaceRecord, '/placerecords/<string:name>', methods=['GET', 'PUT', 'DELETE'])

app.run(host='0.0.0.0', port=5000, debug=True)
