#!/bin/sh
python /ysnp/ysnp/manage.py collectstatic --noinput
/usr/local/bin/gunicorn ysnp.wsgi -w 4 -b 0.0.0.0:5000 --chdir=/ysnp/ysnp
