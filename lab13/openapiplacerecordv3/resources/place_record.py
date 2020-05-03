from flask import jsonify

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
class PlaceRecord:
    @staticmethod
    def get(name):
        for record in placeRecords:
            if name == record["name"]:
                return jsonify(record), 200
        return jsonify({"message": "Place record not found"}), 404

    @staticmethod
    def put(name, rating):
        for record in placeRecords:
            if name == record["name"]:
                record["rating"] = rating
                return jsonify(record), 200

        return jsonify({"message": "Place record not found"}), 404

    @staticmethod
    def delete(name):
        to_be_deleted = None
        for record in placeRecords:
            if name == record["name"]:
                to_be_deleted = record
                break

        if to_be_deleted:
            placeRecords.remove(to_be_deleted)
            return jsonify({"message": "{} is deleted.".format(name)}), 200
        return jsonify({"message": "Place record not found"}), 404


class PlaceRecords:
    @staticmethod
    def post(record_to_be_created):
        name = record_to_be_created['name']
        for record in placeRecords:
            if name == record["name"]:
                return jsonify({"message": "Record with name {} already exists".format(name)}), 500

        placeRecords.append(record_to_be_created)
        return jsonify(record_to_be_created), 201  # 201 Created HTTP status code
