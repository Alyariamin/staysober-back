#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
# if [ -z "$DISABLE_COLLESTATIC" ]; then
#   python manage.py collectstatic --noinput
# fi  
# python manage.py collectstatic --noinput

python manage.py migrate