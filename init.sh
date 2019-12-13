#!/bin/bash
set -e

echo "Starting SSH ..."
service ssh start


service rabbitmq-server start
rabbitmq-plugins enable rabbitmq_management
service rabbitmq-server restart
rabbitmqctl add_user vir QWErty123
rabbitmqctl clear_permissions -p / vir
rabbitmqctl set_permissions -p / vir ".*" ".*" ".*"

# rabbitmqctl set_permissions -p "/" vir “.*” “.*” “.*” # set config/write/read permissions 
rabbitmqctl set_user_tags vir administrator

python /code/server/manage.py runserver 0.0.0.0:8000
