"use client";

import { useState, type FormEvent } from "react";

interface SearchBoxProps {
  onSubmit: (query: string) => void;
  placeholder?: string;
  loading?: boolean;
  size?: "large" | "compact";
}

export default function SearchBox({
  onSubmit,
  placeholder = "Scrivi la tua domanda clinica\u2026",
  loading = false,
  size = "large",
}: SearchBoxProps) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (query.trim() && !loading) {
      onSubmit(query.trim());
    }
  };

  const isLarge = size === "large";

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div
        className={`relative flex items-center gap-3 bg-white rounded-xl border border-[var(--color-border)]
        shadow-sm transition-all duration-200
        focus-within:shadow-md focus-within:border-primary/30 focus-within:ring-2 focus-within:ring-primary/10
        ${isLarge ? "px-5 py-4" : "px-4 py-3"}`}
      >
        <svg
          className={`shrink-0 text-[var(--color-text-muted)] ${isLarge ? "w-6 h-6" : "w-5 h-5"}`}
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
          />
        </svg>

        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          disabled={loading}
          className={`flex-1 bg-transparent outline-none text-[var(--color-text)]
            placeholder:text-[var(--color-text-muted)]
            disabled:opacity-50
            ${isLarge ? "text-lg" : "text-base"}`}
        />

        <button
          type="submit"
          disabled={!query.trim() || loading}
          className={`shrink-0 rounded-lg font-medium transition-all duration-200
            bg-primary text-white
            hover:bg-primary-light
            disabled:opacity-40 disabled:cursor-not-allowed
            active:scale-95
            ${isLarge ? "px-5 py-2.5 text-base" : "px-4 py-2 text-sm"}`}
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Analisi...
            </span>
          ) : (
            "Cerca"
          )}
        </button>
      </div>
    </form>
  );
}
