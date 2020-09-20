#!/bin/bash
set -e

set -o allexport
source .env.dev
set +o allexport

docker-compose down -v 
