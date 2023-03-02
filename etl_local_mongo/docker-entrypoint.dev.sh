#!/bin/bash

if [ "$MONGO" = "true" ]
then
    echo "Waiting for mongo..."

    while ! nc -z $MONGO_HOST_DOCKER $MONGO_PORT; do
      sleep 1
    done

    echo "Mongo started"
fi
python3 main.py