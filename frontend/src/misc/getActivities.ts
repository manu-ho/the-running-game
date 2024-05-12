import { config } from "./config";
import { TActivity } from "./types";

export function getActivities(
  abortControllerSignal: AbortSignal,
  responseCallback: (activities: TActivity[]) => void,
  errorCallback?: (reason: Error) => void
) {
  fetch(config.BACKEND_API_URL + "/activities", {
    method: "GET",
    credentials: "include",
    signal: abortControllerSignal,
  })
    .then(
      (response: Response) => {
        if (response.ok) {
          response.json().then((activities) => {
            responseCallback(activities);
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
