#!/bin/bash
set -e

set -o allexport
source .env.prod
export INITBUILD=True
set +o allexport

docker-compose -f docker-compose-prod.yml up -d --build -V
