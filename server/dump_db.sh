#!/bin/bash

if [[ $1 = 'prod' ]]; then
    set -e
    set -o allexport
    source .env.prod
    set +o allexport	
    docker exec -u app dot-server /usr/bin/pg_dump -c -h db > pg.production.sql
else
    set -e
    set -o allexport    
    export PGPASSWORD="postgres"
    set +o allexport    
    docker exec -u app -ti dot-server /usr/bin/pg_dump -c -d postgres -U postgres -h db > pg.develop.sql
fi
