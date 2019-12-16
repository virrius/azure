#!/usr/bin/env python
# coding=utf-8
import pika
import json
import time
from workersManager import WorkersManager
import sys


out=["0s start",
    "5s omm... \n", 
"10s ooommm.....\n" , 
"15s im focused\n", 
"20s im the universe\n"
"25s meditation cleanses the brain and strengthens the body\n",
"30s i feel power",
"35s more power",
"40s SO MUCH POWER",
"45s TOO MUCH POWEEEER",
"50s AAAGHGGh",
"55s ...",
"60s ......",
]

parameters = pika.URLParameters(
            'amqp://hkdomwxh:HOFklVVJFhu5qjmPgpRWlfYYDC1Z6lpQ@prawn.rmq.cloudamqp.com/hkdomwxh')
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
queue = channel.queue_declare(queue='tasks', exclusive=False)
print("here")
if queue.method.message_count>0:  
    print("in consume")    
    method_frame, properties, body = channel.basic_get('tasks')
    channel.basic_ack(method_frame.delivery_tag)
    print("after consume "+ str(body) + "    "+ str(method_frame.delivery_tag))    
    json_res = json.loads(body)
    
    time_to_wait = int(json_res["data"])
    time.sleep(time_to_wait)
    print(time_to_wait%61)
    print(time_to_wait%61//5)
    json_res["data"] = out[time_to_wait%61//5]

    channel.queue_declare(queue="results")
    channel.basic_publish(
        exchange='', routing_key="results", body=json.dumps(json_res))
channel.close()
manager = WorkersManager()
time.sleep(100)
manager.delete_container_group(sys.argv[1])