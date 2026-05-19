"use client";

import { useEffect, useState } from "react";

const DURATION_MS = 4500;
const FADE_MS = 500;

export function SplashScreen({ children }: { children: React.ReactNode }) {
  const [phase, setPhase] = useState<"loading" | "fading" | "done">("loading");
  const [pct, setPct] = useState(0);

  useEffect(() => {
    const start = performance.now();
    let raf = 0;
    const tick = (now: number) => {
      const elapsed = now - start;
      const ratio = Math.min(1, elapsed / DURATION_MS);
      setPct(Math.round(ratio * 100));
      if (ratio < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);

    const fadeT = window.setTimeout(() => setPhase("fading"), DURATION_MS);
    const doneT = window.setTimeout(() => setPhase("done"), DURATION_MS + FADE_MS);
    return () => {
      cancelAnimationFrame(raf);
      window.clearTimeout(fadeT);
      window.clearTimeout(doneT);
    };
  }, []);

  return (
    <>
      {children}
      {phase !== "done" ? (
        <div
          className="splash-root"
          data-state={phase}
          aria-hidden={phase === "fading"}
          role="status"
        >
          <div className="splash-eyebrow">
            <span className="splash-dot" />
            OBSERVATOIRE DE COMPÉTENCES DATA SCIENCE &amp; INTELLIGENCE ARTIFICIELLE
          </div>

          <h1 className="splash-mark" aria-label="SKILLNAV">
            <span>S</span>
            <span>K</span>
            <span>I</span>
            <span>L</span>
            <span>L</span>
            <span>N</span>
            <span>A</span>
            <span>V</span>
          </h1>

          <div className="splash-bottom">
            <div className="splash-bar" aria-hidden="true">
              <div className="splash-bar-fill" style={{ width: `${pct}%` }} />
            </div>
            <div className="splash-status">
              <span className="splash-status-label">chargement</span>
              <span className="splash-status-pct">
                {String(pct).padStart(3, "0")}%
              </span>
            </div>
            <div className="splash-footer">
              Réalisé par SYLLA KARAMO &amp; KONATÉ BACHIROU
            </div>
          </div>
        </div>
      ) : null}
    </>
  );
}
