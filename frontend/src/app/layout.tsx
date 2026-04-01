import type { Metadata } from "next";
import "./globals.css";
import Navigation from "@/components/shared/Navigation";
import Disclaimer from "@/components/shared/Disclaimer";

export const metadata: Metadata = {
  title: "ASIA \u2014 Aggregated Scientific Intelligence for Animals",
  description: "Supporto alla decisione clinica per l\u2019oncologia veterinaria canina, basato sulla letteratura scientifica.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="it">
      <body className="noise-bg min-h-screen flex flex-col">
        <Navigation />
        <main className="flex-1">{children}</main>
        <Disclaimer />
      </body>
    </html>
  );
}
