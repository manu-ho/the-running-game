# The Running Game 🏃🕹️

_Invalidentreff ☕🍰_ presents **The Running Game** - an app to keep you motivated in running.

[Open the app](https://run.awesomestuff.me)

## Backend

```
docker compose -f docker-compose.yaml --env-file .env up -d --build
```

### Development

For development, a debug configuration is provided.
Start the backend service with a debugger in the container:

```
docker compose -f docker-compose.yaml -f docker-compose.debug.yaml --env-file .env up -d --build
```

Then attach to the container from local VSCode instance using the `Python: Remote Attach` launch configuration from `.vscode/launch.json`.
Set breakpoints as needed and trigger the respective endpoints manuelly using the SWAGGER docs provided at `localhost:${BACKEND_SERVICE_PORT}/docs`.

## Frontend

### Development

```shell
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm run dev
```
