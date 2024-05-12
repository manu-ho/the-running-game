import { config } from "./config";

export function userLogin() {
  fetch(config.BACKEND_API_URL + "/login", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(
      (response: Response) => {
        if (response.ok) {
          response.json().then((authorizationInfo) => {
            console.debug(authorizationInfo);
            if (!authorizationInfo.authorization_url) {
              console.error(
                "Missing `authorization_url` in server response! Got:" +
                  JSON.stringify(authorizationInfo)
              );
              return;
            }
            window.open(
              authorizationInfo.authorization_url,
              "_blank",
              "noreferrer"
            );
          });
        } else {
          console.error({
            name: response.status.toString(),
            message: response.statusText,
          });
        }
      },
      (reason: Error) => {
        console.error(reason);
      }
    )
    .catch((reason: Error) => {
      console.error(reason);
    });
}
