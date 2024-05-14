# The Running Game 🏃🕹️

_Invalidentreff ☕🍰_ presents **The Running Game** - an app to keep you motivated in running.

[Open the app](https://run.awesomestuff.me)

## Run the app locally

The frontend and backend is dockerized <img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/js-packages/%40fortawesome/fontawesome-free/svgs/brands/docker.svg" width="30" height="30" > and a docker-compose file is provided for orchestration.

Setup local environment variables:
- Create a STRAVA app for development [documentation](https://developers.strava.com/docs/getting-started/)
- Copy the `.env.example` file to `.env.prod` file in project root directory
- Fill the missing variables
  - You can find the STRAVA Client ID and Client Secret [in the settings](https://www.strava.com/settings/api)

Run the app
- Linux
```shell
./run.sh --local
```
- Windows
```batch
.\run.bat --local
```

Access the local [frontend](http://localhost:8080) and the [backend api docs](http://localhost:8081/docs) in your browser.


## Development

### Backend

For development, a debug configuration is provided.
Start the backend service with a debugger in the container:

```shell
./run.sh --local --debug
```

Then attach to the container from local VSCode instance using the `Python: Remote Attach` launch configuration from `.vscode/launch.json`.

### Frontend

Start the frontend in development mode with hot-reloading of the source code

```shell
npm run dev
```
