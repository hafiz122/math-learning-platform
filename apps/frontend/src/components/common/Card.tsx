import type { PropsWithChildren } from "react";

interface CardProps {
  className?: string;
}

export function Card({ children, className = "" }: PropsWithChildren<CardProps>) {
  return (
    <div className={`rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-panel ${className}`}>
      {children}
    </div>
  );
}
