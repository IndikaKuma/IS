import json

import requests
from flask import request
from flask_restful import Resource
import pika


class Orders(Resource):

    def post(self):
        record_to_be_created = request.get_json(force=True)
        # Make a GET request to the Inventory Service. URI is dynamically created based on the data in the received
        # message
        r = requests.get('http://172.17.0.3:5000/products/' + record_to_be_created['product type'] + '/quantity')
        ava_quantity = r.json()['quantity']

        # If quantify available > quantity requested
        if ava_quantity > record_to_be_created['quantity']:
            # to establish a connection with RabbitMQ server
            connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.0.5'))
            channel = connection.channel()
            # Create a queue for the event order_reqd
            channel.queue_declare(queue='order_reqd')
            # With the default exchange (empty string), we can say to which queue the message should go by using the
            # queue name as routing_key
            channel.basic_publish(exchange='',
                                  routing_key='order_reqd',
                                  body=json.dumps(record_to_be_created))
            print("[x] Sent 'order_reqd!'")
            connection.close()
            return {"message": "[x] Sent 'order_reqd!'"}, 200

        else:
            return {"message": "Order cannot be accepted at the moment :  out-of-stock"}, 200
