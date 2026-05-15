export type ConsentCountdownFormatOptions = {
  allowSingularDay?: boolean;
};

export function formatConsentExpiryCountdown(
  value: number | string | null | undefined,
  options: ConsentCountdownFormatOptions = {}
) {
  if (value === null || value === undefined || value === "") return null;
  const timestamp =
    typeof value === "number" ? value : new Date(String(value)).getTime();

  if (!Number.isFinite(timestamp) || timestamp === 0) return null;

  const deltaMs = timestamp - Date.now();
  if (deltaMs <= 0) return "Expired";
  const totalMinutes = Math.ceil(deltaMs / (60 * 1000));
  if (totalMinutes < 60) return `${totalMinutes} min left`;
  const totalHours = Math.ceil(totalMinutes / 60);
  if (totalHours < 48) return `${totalHours} hr left`;
  const totalDays = Math.ceil(totalHours / 24);

  if (options.allowSingularDay) {
    return `${totalDays} day${totalDays === 1 ? "" : "s"} left`;
  }

  return `${totalDays} days left`;
}
