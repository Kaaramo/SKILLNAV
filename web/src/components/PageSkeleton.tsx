"use client";

export function PageSkeleton() {
  return (
    <div className="sk-page" aria-busy="true" aria-live="polite">
      {/* KPI strip */}
      <div className="sk-grid sk-grid-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="sk-card sk-kpi">
            <div className="sk-line sk-w-30" />
            <div className="sk-line sk-h-28 sk-w-60" />
            <div className="sk-line sk-w-80" />
          </div>
        ))}
      </div>

      {/* Section header */}
      <div className="sk-section-head">
        <div className="sk-line sk-w-20" />
        <div className="sk-line sk-h-22 sk-w-50" />
      </div>

      {/* Two large cards */}
      <div className="sk-grid sk-grid-2">
        <div className="sk-card sk-tall">
          <div className="sk-line sk-w-40" />
          <div className="sk-bars">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="sk-bar-row">
                <div className="sk-line sk-w-30" />
                <div className="sk-bar" style={{ width: `${85 - i * 10}%` }} />
              </div>
            ))}
          </div>
        </div>
        <div className="sk-card sk-tall">
          <div className="sk-line sk-w-40" />
          <div className="sk-bars">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="sk-bar-row">
                <div className="sk-line sk-w-30" />
                <div className="sk-bar" style={{ width: `${78 - i * 9}%` }} />
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Section header */}
      <div className="sk-section-head">
        <div className="sk-line sk-w-20" />
        <div className="sk-line sk-h-22 sk-w-50" />
      </div>

      {/* Wide card */}
      <div className="sk-card sk-wide">
        <div className="sk-line sk-w-30" />
        <div className="sk-chart" />
      </div>
    </div>
  );
}
