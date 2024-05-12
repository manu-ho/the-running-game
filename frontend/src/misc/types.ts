/**
 * This file is translated from JSON-Schema definition
 * (https://stravalib.readthedocs.io/en/latest/reference/model.html#stravalib.model.Activity) using https://app.quicktype.io/
 */

/**
 * Class representing a best effort on a particular segment.
 */
export type TSegmentEffort = {
  achievements?: TSegmentEffortAchievement[];
  activity?: TCoordinate;
  activity_id?: number;
  athlete?: TAthlete;
  average_cadence?: number;
  average_heartrate?: number;
  average_watts?: number;
  bound_client?: any;
  device_watts?: boolean;
  distance?: number;
  elapsed_time?: number;
  end_index?: number;
  hidden?: boolean;
  id?: number;
  is_kom?: boolean;
  kom_rank?: number;
  max_heartrate?: number;
  moving_time?: number;
  name?: string;
  pr_rank?: number;
  segment?: TSegment;
  start_date?: Date;
  start_date_local?: Date;
  start_index?: number;
  [property: string]: any;
};

/**
 * Class representing a best effort (e.g. best time for 5k)
 */
export type TBestEffort = {
  activity?: TCoordinate;
  activity_id?: number;
  athlete?: TAthlete;
  average_cadence?: number;
  average_heartrate?: number;
  average_watts?: number;
  bound_client?: any;
  device_watts?: boolean;
  distance?: number;
  elapsed_time?: number;
  end_index?: number;
  hidden?: boolean;
  id?: number;
  is_kom?: boolean;
  kom_rank?: number;
  max_heartrate?: number;
  moving_time?: number;
  name?: string;
  pr_rank?: number;
  segment?: TSegment;
  start_date?: Date;
  start_date_local?: Date;
  start_index?: number;
  [property: string]: any;
};

/**
 * Represents an activity (ride, run, etc.).
 */
export type TCoordinate = {
  achievement_count?: number;
  athlete?: TAthlete;
  athlete_count?: number;
  average_cadence?: number;
  average_heartrate?: number;
  average_speed?: number;
  average_temp?: number;
  average_watts?: number;
  best_efforts?: TBestEffort[];
  bound_client?: any;
  calories?: number;
  comment_count?: number;
  commute?: boolean;
  description?: string;
  device_name?: string;
  device_watts?: boolean;
  distance?: number;
  elapsed_time?: number;
  elev_high?: number;
  elev_low?: number;
  embed_token?: string;
  end_latlng?: number[];
  external_id?: string;
  flagged?: boolean;
  from_accepted_tag?: boolean;
  gear?: TGear;
  gear_id?: string;
  guid?: string;
  has_heartrate?: boolean;
  has_kudoed?: boolean;
  hide_from_home?: boolean;
  id?: number;
  instagram_primary_photo?: string;
  kilojoules?: number;
  kudos_count?: number;
  laps?: TLap[];
  location_city?: string;
  location_country?: string;
  location_state?: string;
  manual?: boolean;
  map?: TMap;
  max_heartrate?: number;
  max_speed?: number;
  max_watts?: number;
  moving_time?: number;
  name?: string;
  partner_brand_tag?: string;
  partner_logo_url?: string;
  perceived_exertion?: number;
  photo_count?: number;
  photos?: TActivityPhotoMeta;
  pr_count?: number;
  private?: boolean;
  segment_efforts?: TSegmentEffort[];
  segment_leaderboard_opt_out?: boolean;
  splits_metric?: TSplit[];
  splits_standard?: TSplit[];
  sport_type?: ERelaxedSportType;
  start_date?: Date;
  start_date_local?: Date;
  start_latitude?: number;
  start_latlng?: number[];
  start_longitude?: number;
  suffer_score?: number;
  timezone?: string;
  total_elevation_gain?: number;
  total_photo_count?: number;
  trainer?: boolean;
  type?: EActivityType;
  upload_id?: number;
  upload_id_str?: string;
  utc_offset?: number;
  weighted_average_watts?: number;
  workout_type?: number;
  [property: string]: any;
};

/**
 * An undocumented structure being returned for segment efforts.
 *
 * Notes
 * -----
 * Undocumented Strava elements can change at any time without notice.
 */
export type TSegmentEffortAchievement = {
  effort_count?: number;
  rank?: number;
  type?: string;
  type_id?: number;
  [property: string]: any;
};

/**
 * Represents high level athlete information including
 * their name, email, clubs they belong to, bikes, shoes, etc.
 *
 * Notes
 * ------
 * Also provides access to detailed athlete stats upon request.
 * Many attributes in this object are undocumented by Strava and could be
 * modified at any time.
 */
export type TAthlete = {
  admin?: boolean;
  agreed_to_terms?: string;
  approve_followers?: boolean;
  athlete_type?: EAthleteType;
  badge_type_id?: number;
  bikes?: TSummaryGear[];
  bound_client?: any;
  city?: string;
  clubs?: TSummaryClub[];
  country?: string;
  created_at?: Date;
  date_preference?: string;
  dateofbirth?: Date;
  description?: string;
  email?: string;
  email_facebook_twitter_friend_joins?: boolean;
  email_kom_lost?: boolean;
  email_language?: string;
  email_send_follower_notices?: boolean;
  facebook_sharing_enabled?: boolean;
  firstname?: string;
  follower?: string;
  follower_count?: number;
  follower_request_count?: number;
  friend?: string;
  friend_count?: number;
  ftp?: number;
  global_privacy?: boolean;
  id?: number;
  instagram_username?: string;
  is_authenticated?: boolean;
  lastname?: string;
  max_heartrate?: number;
  measurement_preference?: EMeasurementPreference;
  membership?: string;
  mutual_friend_count?: number;
  offer_in_app_payment?: boolean;
  owner?: boolean;
  plan?: string;
  premium?: boolean;
  premium_expiration_date?: number;
  profile?: string;
  profile_medium?: string;
  profile_original?: string;
  receive_comment_emails?: boolean;
  receive_follower_feed_emails?: boolean;
  receive_kudos_emails?: boolean;
  receive_newsletter?: boolean;
  resource_state?: number;
  sample_race_distance?: number;
  sample_race_time?: number;
  sex?: ESex;
  shoes?: TSummaryGear[];
  state?: string;
  subscription_permissions?: boolean[];
  summit?: boolean;
  super_user?: boolean;
  updated_at?: Date;
  username?: string;
  weight?: number;
  [property: string]: any;
};

export enum EAthleteType {
  Cyclist = "cyclist",
  Runner = "runner",
}

export type TSummaryGear = {
  distance?: number;
  id?: string;
  name?: string;
  primary?: boolean;
  resource_state?: number;
  [property: string]: any;
};

export type TSummaryClub = {
  activity_types?: EActivityType[];
  city?: string;
  country?: string;
  cover_photo?: string;
  cover_photo_small?: string;
  featured?: boolean;
  id?: number;
  member_count?: number;
  name?: string;
  private?: boolean;
  profile_medium?: string;
  resource_state?: number;
  sport_type?: ESportType;
  state?: string;
  url?: string;
  verified?: boolean;
  [property: string]: any;
};

export enum EActivityType {
  AlpineSki = "AlpineSki",
  BackcountrySki = "BackcountrySki",
  Canoeing = "Canoeing",
  Crossfit = "Crossfit",
  EBikeRide = "EBikeRide",
  Elliptical = "Elliptical",
  Golf = "Golf",
  Handcycle = "Handcycle",
  Hike = "Hike",
  IceSkate = "IceSkate",
  InlineSkate = "InlineSkate",
  Kayaking = "Kayaking",
  Kitesurf = "Kitesurf",
  NordicSki = "NordicSki",
  Ride = "Ride",
  RockClimbing = "RockClimbing",
  RollerSki = "RollerSki",
  Rowing = "Rowing",
  Run = "Run",
  Sail = "Sail",
  Skateboard = "Skateboard",
  Snowboard = "Snowboard",
  Snowshoe = "Snowshoe",
  Soccer = "Soccer",
  StairStepper = "StairStepper",
  StandUpPaddling = "StandUpPaddling",
  Surfing = "Surfing",
  Swim = "Swim",
  Velomobile = "Velomobile",
  VirtualRide = "VirtualRide",
  VirtualRun = "VirtualRun",
  Walk = "Walk",
  WeightTraining = "WeightTraining",
  Wheelchair = "Wheelchair",
  Windsurf = "Windsurf",
  Workout = "Workout",
  Yoga = "Yoga",
}

export enum ESportType {
  Cycling = "cycling",
  Other = "other",
  Running = "running",
  Triathlon = "triathlon",
}

export enum EMeasurementPreference {
  Feet = "feet",
  Meters = "meters",
}

export enum ESex {
  F = "F",
  M = "M",
}

/**
 * Represents a single Strava segment.
 */
export type TSegment = {
  activity_type?: EActivityType;
  athlete_count?: number;
  athlete_pr_effort?: TAthletePREffort;
  athlete_segment_stats?: TAthleteSegmentStats;
  average_grade?: number;
  bound_client?: any;
  city?: string;
  climb_category?: number;
  country?: string;
  created_at?: Date;
  distance?: number;
  effort_count?: number;
  elevation_high?: number;
  elevation_low?: number;
  elevation_profile?: string;
  end_latitude?: number;
  end_latlng?: number[];
  end_longitude?: number;
  hazardous?: boolean;
  id?: number;
  map?: TMap;
  maximum_grade?: number;
  name?: string;
  pr_time?: number;
  private?: boolean;
  star_count?: number;
  starred?: boolean;
  starred_date?: Date;
  start_latitude?: number;
  start_latlng?: number[];
  start_longitude?: number;
  state?: string;
  total_elevation_gain?: number;
  updated_at?: Date;
  [property: string]: any;
};

/**
 * Mixin that intercepts attribute lookup and raises warnings or modifies
 * return values based on what is defined in the following class attributes:
 *
 * * _field_conversions
 *
 * Notes
 * ------
 * The class attributes below are not yet implemented:
 * * _deprecated_fields (TODO)
 * * _unsupported_fields (TODO)
 */
export type TAthletePREffort = {
  distance?: number;
  effort_count?: number;
  is_kom?: boolean;
  pr_activity_id?: number;
  pr_date?: Date;
  pr_elapsed_time?: number;
  start_date?: Date;
  start_date_local?: Date;
  [property: string]: any;
};

/**
 * A structure being returned for segment stats for current athlete.
 */
export type TAthleteSegmentStats = {
  activity_id?: number;
  distance?: number;
  effort_count?: number;
  elapsed_time?: number;
  id?: number;
  is_kom?: boolean;
  pr_date?: Date;
  pr_elapsed_time?: number;
  start_date?: Date;
  start_date_local?: Date;
  [property: string]: any;
};

/**
 * Pass through object. Inherits from PolyLineMap
 */
export type TMap = {
  id?: string;
  polyline?: string;
  summary_polyline?: string;
  [property: string]: any;
};

/**
 * Represents a piece of gear (equipment) used in physical activities.
 */
export type TGear = {
  brand_name?: string;
  description?: string;
  distance?: number;
  frame_type?: number;
  id?: string;
  model_name?: string;
  name?: string;
  primary?: boolean;
  resource_state?: number;
  [property: string]: any;
};

export type TLap = {
  activity?: TMetaActivity;
  athlete?: TMetaAthlete;
  average_cadence?: number;
  average_speed?: number;
  distance?: number;
  elapsed_time?: number;
  end_index?: number;
  id?: number;
  lap_index?: number;
  max_speed?: number;
  moving_time?: number;
  name?: string;
  pace_zone?: number;
  split?: number;
  start_date?: Date;
  start_date_local?: Date;
  start_index?: number;
  total_elevation_gain?: number;
  [property: string]: any;
};

export type TMetaActivity = {
  id?: number;
  [property: string]: any;
};

export type TMetaAthlete = {
  id?: number;
  [property: string]: any;
};

/**
 * Represents the metadata of photos returned with the activity.
 *
 * Not to be confused with the fully loaded photos for an activity.
 *
 * Attributes
 * ----------
 * primary : ActivityPhotoPrimary, optional
 * The primary photo for the activity.
 * use_primary_photo : bool, optional
 * Indicates whether the primary photo is used. Not currently documented
 * by Strava.
 *
 * Notes
 * -----
 * Undocumented attributes could be changed by Strava at any time.
 */
export type TActivityPhotoMeta = {
  count?: number;
  primary?: TActivityPhotoPrimary;
  use_primary_photo?: boolean;
  [property: string]: any;
};

/**
 * Represents the primary photo for an activity.
 *
 * Attributes
 * ----------
 * use_primary_photo : bool, optional
 * Indicates whether the photo is used as the primary photo.
 *
 * Notes
 * -----
 * Attributes for activity photos are currently undocumented.
 */
export type TActivityPhotoPrimary = {
  id?: number;
  source?: number;
  unique_id?: string;
  urls?: { [key: string]: string };
  use_primary_photo?: boolean;
  [property: string]: any;
};

/**
 * A split -- may be metric or standard units (which has no bearing
 * on the units used in this object, just the binning of values).
 */
export type TSplit = {
  average_grade_adjusted_speed?: number;
  average_heartrate?: number;
  average_speed?: number;
  distance?: number;
  elapsed_time?: number;
  elevation_difference?: number;
  moving_time?: number;
  pace_zone?: number;
  split?: number;
  [property: string]: any;
};

export enum ERelaxedSportType {
  AlpineSki = "AlpineSki",
  BackcountrySki = "BackcountrySki",
  Badminton = "Badminton",
  Canoeing = "Canoeing",
  Crossfit = "Crossfit",
  EBikeRide = "EBikeRide",
  EMountainBikeRide = "EMountainBikeRide",
  Elliptical = "Elliptical",
  Golf = "Golf",
  GravelRide = "GravelRide",
  Handcycle = "Handcycle",
  HighIntensityIntervalTraining = "HighIntensityIntervalTraining",
  Hike = "Hike",
  IceSkate = "IceSkate",
  InlineSkate = "InlineSkate",
  Kayaking = "Kayaking",
  Kitesurf = "Kitesurf",
  MountainBikeRide = "MountainBikeRide",
  NordicSki = "NordicSki",
  Pickleball = "Pickleball",
  Pilates = "Pilates",
  Racquetball = "Racquetball",
  Ride = "Ride",
  RockClimbing = "RockClimbing",
  RollerSki = "RollerSki",
  Rowing = "Rowing",
  Run = "Run",
  Sail = "Sail",
  Skateboard = "Skateboard",
  Snowboard = "Snowboard",
  Snowshoe = "Snowshoe",
  Soccer = "Soccer",
  Squash = "Squash",
  StairStepper = "StairStepper",
  StandUpPaddling = "StandUpPaddling",
  Surfing = "Surfing",
  Swim = "Swim",
  TableTennis = "TableTennis",
  Tennis = "Tennis",
  TrailRun = "TrailRun",
  Velomobile = "Velomobile",
  VirtualRide = "VirtualRide",
  VirtualRow = "VirtualRow",
  VirtualRun = "VirtualRun",
  Walk = "Walk",
  WeightTraining = "WeightTraining",
  Wheelchair = "Wheelchair",
  Windsurf = "Windsurf",
  Workout = "Workout",
  Yoga = "Yoga",
}

export type TActivity = {
  bound_client?: any;
  id?: number;
  achievement_count?: number;
  athlete?: TAthlete;
  athlete_count?: number;
  average_speed?: number;
  average_watts?: number;
  comment_count?: number;
  commute?: boolean;
  device_watts?: boolean;

  distance?: number;

  elapsed_time?: number;

  elev_high?: number;
  elev_low?: number;
  end_latlng?: any;
  external_id?: string;
  flagged?: boolean;
  gear_id?: string;
  has_kudoed?: boolean;
  hide_from_home?: boolean;
  kilojoules?: number;
  kudos_count?: number;
  manual?: boolean;
  map?: TMap;
  max_speed?: number;
  max_watts?: number;

  moving_time?: number;

  name?: string;

  photo_count?: number;
  private?: boolean;
  sport_type?: ERelaxedSportType;
  start_date?: string;
  start_date_local?: string;
  start_latlng?: any;
  timezone?: string;

  total_elevation_gain?: number;

  total_photo_count?: number;
  trainer?: boolean;

  type?: any;

  upload_id?: number;
  upload_id_str?: string;
  weighted_average_watts?: number;

  workout_type?: number;

  best_efforts?: TBestEffort[];

  calories?: number;
  description?: string;

  laps?: TLap[];
  photos?: TActivityPhotoMeta;
  splits_metric?: TSplit[];
  splits_standard?: TSplit[];

  pr_count?: number;
  suffer_score?: number;
  has_heartrate?: boolean;
  average_heartrate?: number;
  max_heartrate?: number;
  average_cadence?: number;
  average_temp?: number;
  perceived_exertion?: number;
};
