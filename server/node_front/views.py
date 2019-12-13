from django.shortcuts import render
from  .forms import Wait_task_form
from django.conf import settings
import pika

# Create your views here.
def mainView(request):
    if request.method == 'POST':
        form = Wait_task_form(request.POST)
        
        if form.is_valid():
            print("yep, you created a task")
            task_id = request.POST["name"]
            task_data = request.POST["time_to_wait"]
            #user = settings.BROKER_USER
            broker_host = settings.BROKER_HOST
            #password = settings.BROKER_PASSWORD
            parameters = pika.ConnectionParameters(host=broker_host)
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare( queue = "tasks")
            channel.basic_publish(exchange='', routing_key="tasks", body="{}:{}".format(task_id, task_data))
            connection.close()
            task = form.save()
            task.save()
        
    if request.method == 'GET':
        form = Wait_task_form()
    return render(request, 'node_front/main.html', {'task_form': form})
