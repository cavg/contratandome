#!/bin/bash
gunicorn_django --bind=127.0.0.1:8000 --backlog 2048 -w 2 --worker-connections 1000 --log-level=debug -p "/var/tmp/ivanhoe/gunircorn.pid"  --log-file=/var/tmp/ivanhoe/gunicorn.log &
