@echo off

set "local_flag="
if "%~1"=="--local" (
    set "local_flag=-f docker-compose.local.yaml"
)

set "debug_flag="
if "%~1"=="--debug" (
    set "debug_flag=-f docker-compose.debug.yaml"
)

docker network inspect service-routing >nul 2>&1
if errorlevel 1 (
    docker network create service-routing
)

docker-compose -f docker-compose.yaml %local_flag%  %debug_flag% --env-file .env.prod up -d --build
