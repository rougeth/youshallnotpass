#!/bin/bash

set -e
cmd="$@"

export RABBITMQ_URL=amqp://rabbitmq:5672
export CELERY_BROKER_URL=$RABBITMQ_URL

exec $cmd
