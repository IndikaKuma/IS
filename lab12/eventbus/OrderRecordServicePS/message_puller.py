import json
import logging
import time
from threading import Thread
import pika
import requests


def callback(ch, method, properties, body):
    logging.info(" [x] Received %r" % body)
    payload = json.loads(body.decode('utf-8'))
    msg = requests.post("http://127.0.0.1:5000/orders/", json=payload)
    logging.info(msg.content)


def pull_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq_ct'))
    channel = connection.channel()

    channel.exchange_declare(exchange='order', exchange_type='topic')

    # the empty string - create a random queue name by the broker
    # The exclusive flag - when the consumer connection is closed, the queue is deleted.
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    # * (star) can substitute for exactly one word.
    # # (hash) can substitute for zero or more words.
    channel.queue_bind(exchange='order', queue=queue_name, routing_key="order.create.*.*")

    logging.info(' [*] Waiting for messages. To exit press CTRL+C ' + queue_name)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


class MessagePuller(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            try:
                pull_message()
            except Exception as ex:
                logging.info(ex)
                time.sleep(30)
