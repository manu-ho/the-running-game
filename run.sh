#!/bin/bash

local_flag=""
if [[ "$1" == "--local" ]]; then
    local_flag="-f docker-compose.local.yaml"
fi

debug_flag=""
if [[ "$1" == "--debug" ]]; then
    debug_flag="-f docker-compose.debug.yaml"
fi

docker network inspect service-routing >/dev/null 2>&1 || \
    docker network create service-routing

docker compose -f docker-compose.yaml $local_flag $debug_flag --env-file .env.prod up -d --build
