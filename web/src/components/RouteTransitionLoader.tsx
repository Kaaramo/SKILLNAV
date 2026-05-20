"use client";

import { usePathname } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { PageSkeleton } from "./PageSkeleton";

const DURATION_MS = 750;

export function RouteTransitionLoader({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const prevPath = useRef(pathname);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (pathname === prevPath.current) return;
    prevPath.current = pathname;
    setLoading(true);
    const t = window.setTimeout(() => setLoading(false), DURATION_MS);
    return () => window.clearTimeout(t);
  }, [pathname]);

  return loading ? <PageSkeleton /> : <>{children}</>;
}
