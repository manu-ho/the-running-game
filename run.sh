#!/bin/bash

docker compose -f docker-compose.yaml --env-file .env.prod up -d --build
