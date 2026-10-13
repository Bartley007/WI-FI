export function Notice({ kind = 'info', children }) {
  return <div className={`notice ${kind}`}>{children}</div>
}

export const DISCLAIMER =
  'Research prototype for single-person indoor monitoring. Not a medical device. Each module replays its own samples, so the combined view shows the expected effect, not joint ground truth.'
