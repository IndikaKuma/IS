from flask import Flask, request

from resources.place_record import PlaceRecords, PlaceRecord

app = Flask(__name__)

placeRecords = PlaceRecords()
placeRecord = PlaceRecord()


@app.route('/placerecords/<string:name>', methods=['GET'])
def get_place_record(name):
    return placeRecord.get(name)


@app.route('/placerecords/<string:name>', methods=['PUT'])
def update_place_record(name):
    return placeRecord.put(name, int(request.args.get('rating')))


@app.route('/placerecords/<string:name>', methods=['DELETE'])
def delete_place_record(name):
    return placeRecord.delete(name)


@app.route('/placerecords/', methods=['POST'])
def create_place_record():
    return placeRecords.post(request)


app.run(host='0.0.0.0', port=5000, debug=True)
