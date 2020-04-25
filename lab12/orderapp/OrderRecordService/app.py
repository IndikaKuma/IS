from flask import Flask
from flask_restful import Api

from resources.order import Order, Orders

app = Flask(__name__)
api = Api(app)

api.add_resource(Orders, '/orders/', methods=['POST','GET','PUT'])
api.add_resource(Order, '/orders/<string:id>', methods=['GET', 'PUT', 'DELETE'])

app.run(host='0.0.0.0', port=5000, debug=True)
# In the context of servers, 0.0.0.0 can mean "all IPv4 addresses on the local machine".
