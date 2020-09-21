#!/bin/bash
set -e

set -o allexport
source .env.prod
set +o allexport

docker-compose -f docker-compose-prod.yml up -d --build -V
