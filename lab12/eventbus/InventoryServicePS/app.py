from flask import Flask
from flask_restful import Api

from message_puller import MessagePuller
from resources.product import Product

app = Flask(__name__)
api = Api(app)

api.add_resource(Product, '/products/<string:pname>/quantity', methods=['GET','PUT'])
MessagePuller()
app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
# In the context of servers, 0.0.0.0 can mean "all IPv4 addresses on the local machine".
