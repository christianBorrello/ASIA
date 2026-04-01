import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ASIA - Veterinary Oncology Assistant",
  description:
    "AI-powered Scientific Information Assistant for veterinary oncology",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
