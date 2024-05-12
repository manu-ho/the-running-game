import { ReactNode } from "react";
import { TActivity } from "../misc/types";
import { formatDistance, formatDuration } from "../misc/formatNumber";

type TActivityProps = { data: TActivity };

export function Activity({ data }: TActivityProps): ReactNode {
  return (
    <>
      <h5>{data.name}</h5>
      <div className="d-flex justify-content-between">
        <div>{data.distance && formatDistance(data.distance)}</div>
        <div>{data.moving_time && formatDuration(data.moving_time)}</div>
      </div>
      <p>{data.description || "..."}</p>
    </>
  );
}
