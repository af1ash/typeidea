#!/bin/sh

cd /opt/apps/typeidea/src/

echo "migrate databse"
/opt/apps/typeidea/python/bin/python manage.py migrate

echo "create superuser"
/opt/apps/typeidea/python/bin/python manage.py createsuperuser --noinput

echo "collectstatic"
/opt/apps/typeidea/python/bin/python manage.py collectstatic

echo "server is running"
/opt/apps/typeidea/python/bin/gunicorn --worker-class gevent -w 1 typeidea.wsgi:application -c ../conf/gunicorn.conf.py --timeout 500 
