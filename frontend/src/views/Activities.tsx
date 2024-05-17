import { ReactNode, useEffect, useState } from "react";
import { CardList } from "../components/CardList";
import { getActivities } from "../misc/getActivities";
import ErrorToast from "../components/ErrorToast";
import { TActivity } from "../misc/types";
import { Activity } from "../components/Activity";
import { CardListPlaceholder } from "../components/CardListPlaceholder";

type TActivitiesProps = {
  isSignedIn: boolean;
};

export function Activities({ isSignedIn }: TActivitiesProps): ReactNode {
  const [activities, setActivities] = useState<TActivity[]>();

  const [isLoading, setIsLoading] = useState(false);

  const [showErrorToast, setShowErrorToast] = useState(false);
  const [errorToastReason, setErrorToastReason] = useState<Error>({
    name: "-",
    message: "-",
  });

  const loadActivities = () => {
    if (!isSignedIn || isLoading) return;
    const controller = new AbortController();
    setIsLoading(true);
    getActivities(
      controller.signal,
      (acts) => {
        setIsLoading(false);
        setActivities(acts);
      },
      (reason: Error) => {
        setIsLoading(false);
        setErrorToastReason(reason);
        setShowErrorToast(true);
      }
    );
  };

  useEffect(() => {
    if (isSignedIn) {
      loadActivities();
    }
  }, [isSignedIn]);

  return (
    <>
      <ErrorToast
        show={showErrorToast}
        setShow={setShowErrorToast}
        reason={errorToastReason}
      />
      {activities ? (
        <CardList
          title="Activities"
          isLoadingContent={isLoading}
          refreshHandler={loadActivities}
        >
          {activities?.map((activity, index) => (
            <Activity data={activity} key={index} />
          ))}
        </CardList>
      ) : (
        <CardListPlaceholder title="Activities" />
      )}
    </>
  );
}
