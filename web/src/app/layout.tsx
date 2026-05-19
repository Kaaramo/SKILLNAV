import type { Metadata, Viewport } from "next";
import "./globals.css";
import { ThemeProvider } from "@/components/ThemeProvider";
import { AppShell } from "@/components/AppShell";
import { SplashScreen } from "@/components/SplashScreen";

export const metadata: Metadata = {
  title: "SKILLNAV — Dashboard",
  description:
    "Observatoire des compétences IA & Data Science par Web Mining. M242 ENSA-Tétouan, Sylla & Konaté.",
};

export const viewport: Viewport = {
  width: 1440,
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr" data-theme="light">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300..900&family=Inter:wght@300..900&family=JetBrains+Mono:wght@400..700&display=swap"
        />
      </head>
      <body>
        <ThemeProvider>
          <SplashScreen>
            <AppShell>{children}</AppShell>
          </SplashScreen>
        </ThemeProvider>
      </body>
    </html>
  );
}
