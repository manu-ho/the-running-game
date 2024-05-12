// Demonstrate selected international locales
// const locales = [
//   undefined, // Your own browser
//   "en-US", // United States
//   "de-DE", // Germany
//   "ru-RU", // Russia
//   "hi-IN", // India
//   "de-CH", // Switzerland
// ];

export function formatDistance(value: number): string {
  return (
    (value / 1000).toLocaleString("en-US", { maximumFractionDigits: 2 }) + " km"
  );
}

export function formatDuration(value: number): string {
  return new Date(value * 1000).toISOString().slice(11, 19);
}
