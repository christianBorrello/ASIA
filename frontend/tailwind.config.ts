import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#1e3a5f",
          light: "#2d5a8e",
          dark: "#0f1f33",
        },
        accent: {
          DEFAULT: "#c4a35a",
          light: "#e8d5a0",
        },
        surface: {
          DEFAULT: "#f8f7f4",
          elevated: "#ffffff",
        },
        alto: "#059669",
        moderato: "#d97706",
        basso: "#dc2626",
      },
      fontFamily: {
        serif: ["Source Serif 4", "Georgia", "serif"],
        sans: ["DM Sans", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      borderColor: {
        DEFAULT: "#e5e2db",
      },
    },
  },
  plugins: [],
};

export default config;
