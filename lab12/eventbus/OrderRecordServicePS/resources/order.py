from flask import request
from flask_restful import Resource, reqparse
import random

orderRecords = [
    {
        "id": "id1",
        "product type": "Laptop",
        "quantity": 4000,
        "unit price": 444.50
    }
]


class Order(Resource):
    def get(self, id):
        for record in orderRecords:
            if id == record["id"]:
                return record, 200
        return {"message": "Order record not found"}, 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('rating', type=int, help='Rate to charge for this resource')
        args = parser.parse_args(strict=True)

        for record in orderRecords:
            if id == record["id"]:
                record["rating"] = args["rating"]
                return record, 200
        return {"message": "Order record not found"}, 404

    def delete(self, id):
        to_be_deleted = None
        for record in orderRecords:
            if id == record["id"]:
                to_be_deleted = record
                break
        if to_be_deleted:
            orderRecords.remove(to_be_deleted)
            return {"message": "{} is deleted.".format(id)}, 200
        return {"message": "Order record not found"}, 404


class Orders(Resource):
    def post(self):
        record_to_be_created = request.get_json(force=True)
        id1 = "id" + str(random.randint(1, 100001))
        record_to_be_created["id"] = id1
        for record in orderRecords:
            if id1 == record["id"]:
                return {"message": "Order with id {} already exists".format(id)}, 400
        orderRecords.append(record_to_be_created)
        return record_to_be_created, 201

    def put(self):
        record_to_be_created = request.get_json(force=True)
        id = record_to_be_created['id']
        to_be_deleted = None
        for record in orderRecords:
            if id == record["id"]:
                to_be_deleted = record
                break
        if to_be_deleted:
            orderRecords.remove(to_be_deleted)
        orderRecords.append(record_to_be_created)
        return record_to_be_created, 201

    def get(self):
        results = []
        for record in orderRecords:
            results.append(record["id"])
        return results, 200
