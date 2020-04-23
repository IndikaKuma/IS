import json
from threading import Thread
import pika
import requests


# see @ https://www.rabbitmq.com/tutorials/tutorial-one-python.html
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    payload = json.loads(body.decode('utf-8'))
    # This is the cleanest way to call the API methods locally.
    requests.post("http://localhost:5000/orders/", json=payload)


def pull_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters('35.226.146.183'))
    channel = connection.channel()
    channel.queue_declare(queue='order_reqd')
    # When  a  message is received, the callback  method is triggered
    channel.basic_consume(queue='order_reqd',
                          auto_ack=True,
                          on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


class MessagePuller(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            pull_message()
