from flask_restful import reqparse, Resource
from flask import request

# dummy data
from flask_restful_swagger import swagger

from models import PlaceRecordModel

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
    @swagger.operation(
        notes='Get a Place Record',
        responseClass=PlaceRecordModel,
        nickname='create',
        parameters=[
            {
                "name": "name",
                "description": "Place Record identifier",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "path"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Created. The URL of the created blueprint should " +
                           "be in the Location header"
            },
            {
                "code": 404,
                "message": "Place record not found"
            }
        ])
    def get(self, name):
        for record in placeRecords:
            if name == record["name"]:
                return record, 200  # return 200 HTTP status code to indicate success
        return {"message": "Place record not found"}, 404 # return 404 HTTP status code to indicate resource not found

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('rating', type=int, help='Rate to charge for this resource')
        args = parser.parse_args(strict=True)

        for record in placeRecords:
            if name == record["name"]:
                record["rating"] = args["rating"]
                return record, 200

        return {"message": "Place record not found"}, 404

    def delete(self, name):
        to_be_deleted = None
        for record in placeRecords:
            if name == record["name"]:
                to_be_deleted = record
                break

        if to_be_deleted:
            placeRecords.remove(to_be_deleted)
            return "{} is deleted.".format(name), 200
        return {"message": "Place record not found"}, 404


# resource collection place records
class PlaceRecords(Resource):
    def post(self):
        record_to_be_created = request.get_json(force=True)
        name = record_to_be_created['name']
        for record in placeRecords:
            if name == record["name"]:
                return {"message": "Record with name {} already exists".format(name)}, 500 # 500 Internal Server Error HTTP status code

        placeRecords.append(record_to_be_created)
        return record_to_be_created, 201  # 201 Created HTTP status code
