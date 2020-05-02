from flask_restful import fields
from flask_restful_swagger import swagger

@swagger.model
class AddressModel:
    resource_fields = {
        'postcode': fields.String,
        'street': fields.String,
        'houseNo': fields.Integer,
        'city': fields.String
    }


@swagger.model
class PlaceRecordModel:
    resource_fields = {
        'name': fields.String,
        'rating': fields.Float,
        'address': fields.Nested(AddressModel.resource_fields)
    }

    # Specify which of the resource fields are required
    required = ['name']