from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)
inventories = [
    {
        "name": "Laptop",
        "quantity": 1000
    },
    {
        "name": "Phone",
        "quantity": 5000
    }
]


class Product(Resource):
    def get(self, pname):
        for record in inventories:
            if pname == record["name"]:
                return record, 200
        return {"message": "No product for " + pname}, 404

    def put(self, pname):
        parser = reqparse.RequestParser()
        parser.add_argument('value', type=int, help='Quantity to be issued')
        args = parser.parse_args(strict=True)

        for record in inventories:
            if pname == record["name"]:
                record["quantity"] = record["quantity"] - args["value"]
                return record, 200
        return {"message": "No product for " + pname}, 404