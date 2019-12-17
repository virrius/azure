from django.shortcuts import render
from .forms import Wait_task_form, Result_form
from django.conf import settings
from .workersManager import workersManager
import pika
from .models import Result
import json
import uuid


# Create your views here.


def mainView(request):
    if request.method == 'POST':
        form = Wait_task_form(request.POST)

        if form.is_valid():
            print("yep, you created a task")
            message = {}
            uid = str(uuid.uuid4())
            message["name"] = str(request.POST["name"])
            message["data"] = str(request.POST["time_to_wait"])
            message["uid"] = uid
            print(json.dumps(message))
            parameters = pika.URLParameters(
                'amqp://hkdomwxh:HOFklVVJFhu5qjmPgpRWlfYYDC1Z6lpQ@prawn.rmq.cloudamqp.com/hkdomwxh')
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue="tasks")
            channel.basic_publish(
                exchange='', routing_key="tasks", body=json.dumps(message))
            connection.close()
            manager = workersManager()
            manager.run_task_based_container(manager.aciclient,
                                             manager.resource_group, 
                                             str(uid),
                                             manager.container_image_name)
            task = form.save()
            task.save()
            return render(request, 'node_front/main.html', {'task_form': form, 'output': "uid of this task: {}".format(uid)})

    if request.method == 'GET':
        form = Wait_task_form()
        return render(request, 'node_front/main.html', {'task_form': form})


def statusView(request):
    if request.method == 'POST':
        result_form = Result_form(request.POST)
        parameters = pika.URLParameters(
            'amqp://hkdomwxh:HOFklVVJFhu5qjmPgpRWlfYYDC1Z6lpQ@prawn.rmq.cloudamqp.com/hkdomwxh')
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        queue = channel.queue_declare(queue='results', exclusive=False)
        last = queue.method.message_count
        if last > 0:
            for method_frame, properties, body in channel.consume('results'):
                print("im in consuming!")
                print(body)
                json_res = json.loads(body)
                res = Result.objects.create(
                    uid=json_res["uid"], name=json_res["name"], body="task ends with result: {}".format(json_res["data"]))
                print(res)
                res.save()
                channel.basic_ack(method_frame.delivery_tag)
                if method_frame.delivery_tag == last:
                    break
        channel.cancel()
        channel.close()
        connection.close()
        return render(request, 'node_front/status.html', {'result_form': result_form, "output": Result.objects.filter(uid=request.POST["uid"])})

    if request.method == 'GET':
        result_form = Result_form()
        return render(request, 'node_front/status.html', {'result_form': result_form})
