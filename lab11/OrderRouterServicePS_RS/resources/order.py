import json
import uuid

import pika
import requests
from flask import request
from flask_restful import Resource


class Orders(Resource):

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def post(self):
        self.response = None
        record_to_be_created = request.get_json(force=True)
        # Make a GET request to the Inventory Service. URI is dynamically created based on the data in the received
        # message
        r = requests.get('http://127.0.0.1:5000/products/' + record_to_be_created['product type'] + '/quantity')
        ava_quantity = r.json()['quantity']

        # If quantify available > quantity requested
        if ava_quantity > record_to_be_created['quantity']:
            # to establish a connection with RabbitMQ server
            connection = pika.BlockingConnection(pika.ConnectionParameters('104.198.35.199'))
            channel = connection.channel()
            # Create an exchange of typo topic
            channel.exchange_declare(exchange='order', exchange_type='topic')
            channel.queue_declare(queue='order_reply_queue')
            self.corr_id = str(uuid.uuid4())

            # Messages sent to a topic exchange can't have an arbitrary routing_key - it must be a list of words,
            # delimited by dots.  A message sent with a particular routing key will be delivered to all the queues
            # that are bound with a matching binding key.
            channel.basic_publish(exchange='order',
                                  routing_key='order.create.inventory.update',
                                  properties=pika.BasicProperties(
                                      reply_to='order_reply_queue',
                                      correlation_id=self.corr_id,
                                  ),
                                  body=json.dumps(record_to_be_created))

            print("[x] Sent 'order_reqd!'")

            channel.basic_consume(
                queue='order_reply_queue',
                on_message_callback=self.on_response,
                auto_ack=True)

            while self.response is None:
                connection.process_data_events()
            return json.loads(self.response.decode('utf-8')), 200

        else:
            return {"message": "Order cannot be accepted at the moment :  out-of-stock"}, 200
