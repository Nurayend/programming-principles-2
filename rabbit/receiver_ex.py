import pika
import time

def callback(ch, method, properties, body):
    print("Received: {}".format(body))
    time.sleep(body.count(b'.')) #message.... 4 sec
    print("Done")
    ch.basic_ack(delivery_tag = metod.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue='example1')

channel.basic_consume(queue='example1', auto_ack=True, on_message_callback=callback)

channel.start_consuming()