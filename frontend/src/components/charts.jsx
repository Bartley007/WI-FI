// Small dependency-free chart pieces. Feel free to add recharts / d3 in your own page.

export function ProbBars({ probs, highlight }) {
  return (
    <div className="probs">
      {Object.entries(probs).map(([k, v]) => (
        <div className="prob-row" key={k}>
          <span className="prob-name">{k}</span>
          <div className="bar"><i style={{ width: `${Math.round(v * 100)}%`, background: k === highlight ? 'var(--accent)' : 'var(--bar-muted)' }} /></div>
          <span className="prob-val">{Math.round(v * 100)}%</span>
        </div>
      ))}
    </div>
  )
}

export function LineChart({ points, upTo = Infinity, threshold, height = 120, yLabel }) {
  const w = 320
  const pad = 14
  const ts = points.map((p) => p.x)
  const xmin = Math.min(...ts)
  const xmax = Math.max(...ts) || 1
  const sx = (x) => pad + ((x - xmin) / (xmax - xmin || 1)) * (w - 2 * pad)
  const sy = (y) => height - pad - y * (height - 2 * pad)
  const shown = points.filter((p) => p.x <= upTo)
  return (
    <svg viewBox={`0 0 ${w} ${height}`} width="100%" style={{ maxHeight: 190 }} role="img" aria-label={yLabel || 'line chart'}>
      <line x1={pad} x2={w - pad} y1={sy(0)} y2={sy(0)} stroke="var(--border-strong)" />
      {threshold != null && (
        <line x1={pad} x2={w - pad} y1={sy(threshold)} y2={sy(threshold)} stroke="var(--danger)" strokeDasharray="3 3" />
      )}
      <polyline fill="none" stroke="var(--accent)" strokeWidth="2" points={shown.map((p) => `${sx(p.x)},${sy(p.y)}`).join(' ')} />
      {shown.map((p, i) => <circle key={i} cx={sx(p.x)} cy={sy(p.y)} r="3" fill="var(--accent)" />)}
    </svg>
  )
}

export function ConfusionMatrix({ labels, matrix }) {
  const rowMax = matrix.map((r) => r.reduce((a, b) => a + b, 0) || 1)
  return (
    <table className="cm">
      <thead>
        <tr><th>true \ pred</th>{labels.map((l) => <th key={l}>{l}</th>)}</tr>
      </thead>
      <tbody>
        {matrix.map((row, i) => (
          <tr key={labels[i]}>
            <th>{labels[i]}</th>
            {row.map((v, j) => (
              <td key={j} style={{ background: `rgba(34,228,255,${(0.08 + 0.7 * v / rowMax[i]).toFixed(2)})`, color: v / rowMax[i] > 0.5 ? "#04101C" : "inherit" }}>{v}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  )
}

export function MetricTable({ rows }) {
  return (
    <table className="mt">
      <thead><tr>{Object.keys(rows[0] || {}).map((k) => <th key={k}>{k}</th>)}</tr></thead>
      <tbody>
        {rows.map((r, i) => <tr key={i}>{Object.values(r).map((v, j) => <td key={j}>{v}</td>)}</tr>)}
      </tbody>
    </table>
  )
}
