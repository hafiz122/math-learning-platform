import { Link } from "react-router-dom";
import { Button } from "../components/common/Button";

export function NotFoundPage() {
  return (
    <div className="flex min-h-[50vh] flex-col items-center justify-center gap-4 text-center">
      <h1 className="text-4xl font-black text-white">Page not found</h1>
      <p className="max-w-lg text-slate-400">The page you requested does not exist.</p>
      <Link to="/">
        <Button>Go home</Button>
      </Link>
    </div>
  );
}
