from threading import Thread
import pika
import uuid
import pygame
import json


token = ''
tank = ''


class RpcConsumer(Thread):
    def __init__(self, binding_key):
        Thread.__init__(self)
        self.binding_key = binding_key
        self.cb = None
        self.corr_id = None
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('34.254.177.17', 5672, 'dar-tanks',
                                      pika.PlainCredentials('dar-tanks', '5orPLExUYnyVYZg48caMpX')))
        self.channel = self.connection.channel()
        self.channel.queue_declare(self.binding_key, exclusive=True)
        self.channel.queue_bind(exchange='X:routing.topic',
                                queue=self.binding_key,
                                routing_key=self.binding_key)

    def run(self):
        def callback(ch, method, props, body):
            if self.corr_id == props.correlation_id:
                self.response = body
                decoded = body.decode('utf-8')
                if self.cb is not None:
                    self.cb(decoded)
            else:
                print("Unexpected response {}".format(body))

        self.channel.basic_consume(queue=self.binding_key, on_message_callback=callback, auto_ack=True)
        print("Starting RPC client...")
        self.connection.process_data_events()
        self.channel.start_consuming()

    def set_callback(self, corr_id, cb):
        self.corr_id = corr_id
        self.cb = cb


class RpcClient(Thread):
    def __init__(self, queue_name, rpc_consumer):
        Thread.__init__(self)
        self.rpc_consumer = rpc_consumer
        self.queue_name = queue_name
        self.exchange = 'X:routing.topic'
        self.corr_id = None
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('34.254.177.17', 5672, 'dar-tanks',
                                      pika.PlainCredentials('dar-tanks', '5orPLExUYnyVYZg48caMpX')))
        self.channel = self.connection.channel()

    def run(self) -> None:
        pass

    def call(self, request, rk, cb):
        self.corr_id = str(uuid.uuid4())
        self.rpc_consumer.set_callback(self.corr_id, cb)

        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=rk,
            properties=pika.BasicProperties(
                reply_to=self.queue_name,
                correlation_id=self.corr_id
            ),
            body=str(request)
        )
        print(str(request))


def handle_regular_response(obj):
    print(str(obj))


def handle_register_response(obj):
    state = json.loads(obj)
    print(str(obj))
    global token
    token = state["token"]
    global tank
    tank = state["tankId"]


class GameStateConsumer(Thread):
    def __init__(self, room):
        Thread.__init__(self)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('34.254.177.17', 5672, 'dar-tanks',
                                      pika.PlainCredentials('dar-tanks', '5orPLExUYnyVYZg48caMpX')))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='X:routing.topic', exchange_type='topic', durable=True)
        self.result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = self.result.method.queue
        self.channel.queue_bind(
            exchange='X:routing.topic', queue=self.queue_name, routing_key="event.state.{}".format(room))

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1000, 800))

        def callback(ch, method, properties, body):
            state = json.loads(body)
            print(state)
            screen.fill((0, 0, 0))
            pygame.event.get()
            for t in state["gameField"]["tanks"]:
                c = int(t["x"]), int(t["y"])
                col = (125, 108, 130)
                if t["id"] == tank:
                    col = (255, 234, 99)
                pygame.draw.circle(screen, col, (c[0] + 20, c[1] + 20), 20)
                pygame.draw.rect(screen, col, (c[0], c[1], 40, 40), 2)
            pygame.display.flip()

        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()


queue_name = "{}.response".format(uuid.uuid4())
rpc_consumer = RpcConsumer(queue_name)
rpc_consumer.daemon = True
rpc_consumer.start()

rpc_client = RpcClient(queue_name, rpc_consumer)
rpc_client.daemon = True
rpc_client.start()

while True:
    message = input()
    params = message.split()
    if params[0] == 'healthcheck':
        rpc_client.call(None, 'tank.request.healthcheck', handle_regular_response)
    elif params[0] == 'register':
        rpc_client.call('{"roomId":"room-6"}', 'tank.request.register', handle_register_response)
        state_consumer = GameStateConsumer('room-6')
        state_consumer.daemon = True
        state_consumer.start()
    elif params[0] == "l":
        req = '{"token":"' + token + '", "direction":"LEFT"}'
        rpc_client.call(req, 'tank.request.turn', handle_regular_response)
    elif params[0] == "r":
        req = '{"token":"' + token + '", "direction":"RIGHT"}'
        rpc_client.call(req, 'tank.request.turn', handle_regular_response)
    elif params[0] == "u":
        req = '{"token":"' + token + '", "direction":"UP"}'
        rpc_client.call(req, 'tank.request.turn', handle_regular_response)
    elif params[0] == "d":
        req = '{"token":"' + token + '", "direction":"DOWN"}'
        rpc_client.call(req, 'tank.request.turn', handle_regular_response)