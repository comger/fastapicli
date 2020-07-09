#! /usr/bin/env bash

# Exit in case of error
set -e

docker-compose -f docker-compose-sb2.yml build
docker-compose -f docker-compose-sb2.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -f docker-compose-sb2.yml up -d
docker-compose -f docker-compose-sb2.yml exec -T api ./tests-start.sh
docker-compose -f docker-compose-sb2.yml down -v --remove-orphans
