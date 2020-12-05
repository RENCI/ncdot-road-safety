#!/bin/bash

if [ $1 == '-i' ]; then
	docker exec -u app -ti dot-server python manage.py $2
else    
        docker exec -u app dot-server python manage.py $* 
fi
