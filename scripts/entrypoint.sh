#!/bin/sh

cd /opt/apps/pipeline_model/main/

echo "migrate databse"
/opt/apps/pipeline_model/python/bin/python manage.py migrate

echo "create superuser"
/opt/apps/pipeline_model/python/bin/python manage.py createsuperuser --noinput

echo "collectstatic"
/opt/apps/pipeline_model/python/bin/python manage.py collectstatic

echo "server is running"
/opt/apps/pipeline_model/python/bin/gunicorn --worker-class gevent -w 1 main.wsgi:application -c ../conf/gunicorn.conf.py --timeout 500 
