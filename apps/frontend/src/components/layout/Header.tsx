import { Link, NavLink } from "react-router-dom";

export function Header() {
  return (
    <header className="border-b border-slate-800 bg-slate-950 text-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link to="/" className="text-lg font-bold tracking-tight">
          Math Learning Platform
        </Link>

        <nav className="flex items-center gap-6 text-sm font-medium">
          <NavLink to="/" className="hover:text-cyan-300">
            Home
          </NavLink>
          <NavLink to="/practice" className="hover:text-cyan-300">
            Practice
          </NavLink>
          <NavLink to="/pricing" className="hover:text-cyan-300">
            Pricing
          </NavLink>
          <NavLink
            to="/login"
            className="rounded-xl border border-cyan-400/30 bg-cyan-400/10 px-3 py-2 text-cyan-300 transition hover:bg-cyan-400/20"
          >
            Log in
          </NavLink>
        </nav>
      </div>
    </header>
  );
}