#!/bin/bash

if [ $# == 2 ]; then
    if [ $1 = '-i' ]; then
	docker exec -u app -ti dot-server python manage.py $2
    fi
else    
    docker exec -u app dot-server python manage.py $1 --no-input
fi

