from flask import request
from flask_restful import reqparse
# dummy data
from flask_restful_swagger_3 import swagger, Resource

from models import PlaceRecordModel, ErrorModel, DeleteMsgModel

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
    @swagger.doc({
        'tags': ['place record'],
        'description': 'Get a Place Record',
        'parameters': [
            {
                'name': 'name',
                'description': 'Place Record identifier',
                'in': 'path',
                'schema': {
                    'type': 'string'
                }
            }
        ],
        'responses': {
            '200': {
                'description': 'Place Record',
                'content': {
                    'application/json': {
                        'schema': PlaceRecordModel
                    }
                }
            },
            '404': {
                'description': 'Place record not found',
                'content': {
                    'application/json': {
                        'schema': ErrorModel
                    }
                }
            }
        }
    })
    def get(self, name):
        for record in placeRecords:
            if name == record["name"]:
                return record, 200  # return 200 HTTP status code to indicate success
        return {"message": "Place record not found"}, 404  # return 404 HTTP status code to indicate resource not found

    @swagger.doc({
        'tags': ['place record'],
        'description': 'Updated Place Record',
        'parameters': [
            {
                'name': 'name',
                'description': 'Place Record identifier',
                'in': 'path',
                'schema': {
                    'type': 'string'
                }
            },
            {
                'name': 'rating',
                'description': 'Place rating',
                'in': 'query',
                'schema': {
                    'type': 'number',
                    'format': 'double'
                }
            }
        ],
        'responses': {
            '200': {
                'description': 'Updated Place Record',
                'content': {
                    'application/json': {
                        'schema': PlaceRecordModel
                    }
                }
            },
            '404': {
                'description': 'Place record not found',
                'content': {
                    'application/json': {
                        'schema': ErrorModel
                    }
                }
            }
        }
    })
    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('rating', type=int, help='Rate to charge for this resource')
        args = parser.parse_args(strict=True)

        for record in placeRecords:
            if name == record["name"]:
                record["rating"] = args["rating"]
                return record, 200

        return {"message": "Place record not found"}, 404

    @swagger.doc({
        'tags': ['place record'],
        'description': 'Delete a Place Record',
        'parameters': [
            {
                'name': 'name',
                'description': 'Place Record identifier',
                'in': 'path',
                'schema': {
                    'type': 'string'
                }
            }
        ],
        'responses': {
            '200': {
                'description': 'Record was deleted',
                'content': {
                    'application/json': {
                        'schema': DeleteMsgModel
                    }
                }
            },
            '404': {
                'description': 'Place record not found',
                'content': {
                    'application/json': {
                        'schema': ErrorModel
                    }
                }
            }
        }
    })
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
    @swagger.doc({
        'tags': ['place record'],
        'description': 'Create a New Place Record',
        'requestBody':
            {
                'description': 'Place Information',
                'content': {
                    'application/json': {
                        'schema': PlaceRecordModel
                    }
                }
            }
        ,
        'responses': {
            '200': {
                'description': 'Created Place Record',
                'content': {
                    'application/json': {
                        'schema': PlaceRecordModel
                    }
                }
            },
            '500': {
                'description': 'Record with the same name already exists',
                'content': {
                    'application/json': {
                        'schema': ErrorModel
                    }
                }
            }
        }
    })
    def post(self):
        record_to_be_created = request.get_json(force=True)
        name = record_to_be_created['name']
        for record in placeRecords:
            if name == record["name"]:
                return {"message": "Record with name {} already exists".format(
                    name)}, 500  # 500 Internal Server Error HTTP status code

        placeRecords.append(record_to_be_created)
        return record_to_be_created, 201  # 201 Created HTTP status code
