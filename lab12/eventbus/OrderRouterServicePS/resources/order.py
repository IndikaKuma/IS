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
        r = requests.get('http://inventory_service_ps_ct:5000/products/' + record_to_be_created['product type'] + '/quantity')
        ava_quantity = r.json()['quantity']

        # If quantify available > quantity requested
        if ava_quantity > record_to_be_created['quantity']:
            # to establish a connection with RabbitMQ server
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq_ct'))
            channel = connection.channel()
            # Create an exchange of type topic
            channel.exchange_declare(exchange='order', exchange_type='topic')
            # Messages sent to a topic exchange can't have an arbitrary routing_key - it must be a list of words,
            # delimited by dots.  A message sent with a particular routing key will be delivered to all the queues
            # that are bound with a matching binding key.
            channel.basic_publish(exchange='order',
                                  routing_key='order.create.inventory.update',
                                  body=json.dumps(record_to_be_created))
            print("[x] Sent 'order_reqd!'")
            connection.close()
            return {"message": "[x] Sent 'order_reqd!'"}, 200

        else:
            return {"message": "Order cannot be accepted at the moment :  out-of-stock"}, 200
