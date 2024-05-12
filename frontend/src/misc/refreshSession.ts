import { config } from "./config";

export function refreshSession(
  abortControllerSignal: AbortSignal,
  responseCallback: (success: boolean) => void,
  errorCallback?: (reason: Error) => void
) {
  fetch(config.BACKEND_API_URL + "/oauth/refresh", {
    method: "POST",
    credentials: "include",
    signal: abortControllerSignal,
  })
    .then(
      (response: Response) => {
        if (response.ok) {
          responseCallback(true);
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
