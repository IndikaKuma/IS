from flask_restful import Resource, reqparse
from flask import request

# dummy data
placeRecords = [
    {
        "name": "JADS",
        "rating": 4.5,
        "address": {
            "postcode": "5211 DA",
            "street": "Sint Janssingel",
            "houseNo": 92,
            "city": "Den Bosch"
        }
    }
]


# resource place record
class PlaceRecord(Resource):
    def get(self, name):
        for record in placeRecords:
            if name == record["name"]:
                return record, 200  # return 200 HTTP status code to indicate success
        return {"message": "Place record not found"}, 404  # return 404 HTTP status code to indicate resource not found


# resource collection place records
class PlaceRecords(Resource):
    def post(self):
        record_to_be_created = request.get_json(force=True)
        name = record_to_be_created['name']
        for record in placeRecords:
            if name == record["name"]:
                return {"message": "Record with name {} already exists".format(
                    name)}, 500  # 500 Internal Server Error HTTP status code

        placeRecords.append(record_to_be_created)
        return record_to_be_created, 201  # 201 Created HTTP status code
