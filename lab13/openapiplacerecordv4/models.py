from flask_restful_swagger_3 import Schema


class AddressModel(Schema):
    type = 'object'
    properties = {
        'postcode': {
            'type': 'string'
        },
        'street': {
            'type': 'string'
        },
        'houseNo': {
            'type': 'integer',
            'format': 'int64',
        },
        'city': {
            'type': 'string'
        }
    }


class PlaceRecordModel(Schema):
    type = 'object'
    properties = {
        'name': {
            'type': 'string'
        },
        'rating': {
            'type': 'number',
            'format': 'double',
        },
        'address': AddressModel
    }
    required = ['name']


class ErrorModel(Schema):
    type = 'object'
    properties = {
        'message': {
            'type': 'string'
        },
        'code': {
            'type': 'integer',
            'format': 'int64',
        }
    }
    required = ['message', 'code']
