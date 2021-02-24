# rpc client
import pika
import uuid
import json

class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('34.254.177.17',5672,'dar-tanks',pika.PlainCredentials('dar-tanks','5orPLExUYnyVYZg48caMpX')))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True, auto_delete=True)
        self.callback_queue = result.method.queue

        self.channel.queue_bind(exchange='X:routing.topic',
                                queue=self.callback_queue)
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=False)
# on_response callback checks if the correlation_id is the one we're looking for, if so it's saves the response and break loop
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, rk, request, corr_id):
        self.response = None
        self.corr_id = corr_id # we generate a unique correlation_id
        self.channel.basic_publish(
            exchange='X:routing.topic',
            routing_key=rk,
            properties=pika.BasicProperties(
                # we publish the request message, with two properties
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=request)
        while self.response is None:
            self.connection.process_data_events()
        return json.loads(self.response) # return the response back to the user.

fibonacci_rpc = FibonacciRpcClient()
corr_id = str(uuid.uuid4())
print(" [x] Requesting fib(30)")
room = json.dumps({"roomId":"room-2"})
response = fibonacci_rpc.call("tank.request.register", room, corr_id)
tankId = str(response["tankId"])
token = str(response["token"])
print(" [.] Got tankId - {}, token - {}".format(tankId, token))
condition = fibonacci_rpc.call("tank.request.healthcheck", "", corr_id)
print(condition)