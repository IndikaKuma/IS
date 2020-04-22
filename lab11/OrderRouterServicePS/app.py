from flask import Flask
from flask_restful import Api

from resources.order import Orders

app = Flask(__name__)
api = Api(app)

api.add_resource(Orders, '/orders/', methods=['POST'])

app.run(host='0.0.0.0', port=5001, debug=True)
