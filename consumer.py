# coding=utf-8
#!/usr/bin/env python
import pika

RABBIT_HOST = '0.0.0.0'
RABBIT_PORT = '5672'
RABBIT_USER = 'vir'
RABBIT_PASSWORD = 'QWErty123'

cred = pika.credentials.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST, RABBIT_PORT, credentials=cred))
channel = connection.channel()
channel.queue_declare(queue='tasks')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)



channel.basic_consume(queue='tasks',  on_message_callback=callback,  auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()