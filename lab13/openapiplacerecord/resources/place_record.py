from flask import request
from flask_restful import reqparse, Resource
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
        responseClass=PlaceRecordModel.__name__,
        nickname='getRecord',
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
                "message": "Place Record"
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
        return {"message": "Place record not found"}, 404  # return 404 HTTP status code to indicate resource not found

    @swagger.operation(
        notes='Update a Place Record',
        nickname='updateRecord',
        responseClass=PlaceRecordModel.__name__,
        parameters=[
            {
                "name": "name",
                "description": "Place Record identifier",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "path"
            },
            {
                "name": "rating",
                "description": "Place rating",
                "required": True,
                "allowMultiple": False,
                "dataType": 'integer',
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Place Record was updated"
            },
            {
                "code": 404,
                "message": "Place record not found"
            }
        ])
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('rating', type=int, help='Rate to charge for this resource')
        args = parser.parse_args(strict=True)

        for record in placeRecords:
            if name == record["name"]:
                record["rating"] = args["rating"]
                return record, 200

        return {"message": "Place record not found"}, 404

    @swagger.operation(
        notes='Delete a Place Record',
        nickname='deleteRecord',
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
                "message": "Place Record was deleted"
            },
            {
                "code": 404,
                "message": "Place record not found"
            }
        ])
    def delete(self, name):
        to_be_deleted = None
        for record in placeRecords:
            if name == record["name"]:
                to_be_deleted = record
                break

        if to_be_deleted:
            placeRecords.remove(to_be_deleted)
            return "{} was deleted.".format(name), 200
        return {"message": "Place record not found"}, 404


# resource collection place records
class PlaceRecords(Resource):
    @swagger.operation(
        notes='Create a Place Record',
        responseClass=PlaceRecordModel,
        nickname='createRecord',
        parameters=[
            {
                "name": "body",
                "description": "Place Record identifier",
                "required": True,
                "allowMultiple": False,
                "dataType": PlaceRecordModel.__name__,
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "Created Place Record"
            },
            {
                "code": 500,
                "message": "Record with the given name already exists"
            }
        ])
    def post(self):
        record_to_be_created = request.get_json(force=True)
        name = record_to_be_created['name']
        for record in placeRecords:
            if name == record["name"]:
                return {"message": "Record with name {} already exists".format(
                    name)}, 500  # 500 Internal Server Error HTTP status code

        placeRecords.append(record_to_be_created)
        return record_to_be_created, 201  # 201 Created HTTP status code
