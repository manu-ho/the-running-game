import { config } from "./config";
import { TAthlete } from "./types";

export function getAthlete(
  abortControllerSignal: AbortSignal,
  responseCallback: (athlete: TAthlete[]) => void,
  errorCallback?: (reason: Error) => void
) {
  fetch(config.BACKEND_API_URL + "/athlete", {
    method: "GET",
    credentials: "include",
    signal: abortControllerSignal,
  })
    .then(
      (response: Response) => {
        if (response.ok) {
          response.json().then((athlete) => {
            responseCallback(athlete);
          });
        } else {
          errorCallback?.({
            name: response.status.toString(),
            message: response.statusText,
          });
        }
      },
      (reason: Error) => {
        errorCallback?.(reason);
      }
    )
    .catch((reason: Error) => {
      errorCallback?.(reason);
    });
}
