# rpc client
import pika
import uuid
import json
from threading import Thread 
class FibonacciRpcClient(Thread):

    def run(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('34.254.177.17',5672,'dar-tanks',pika.PlainCredentials('dar-tanks','5orPLExUYnyVYZg48caMpX')))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True, auto_delete=True)
        self.callback_queue = result.method.queue

        self.channel.queue_bind(exchange='X:routing.topic',
                                queue=self.callback_queue,
                                routing_key="event.state.room-2"
                                )

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.channel.start_consuming()
# on_response callback checks if the correlation_id is the one we're looking for, if so it's saves the response and break loop
    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)
        print(self.response)
fibonacci_rpc = FibonacciRpcClient()
fibonacci_rpc.start()
