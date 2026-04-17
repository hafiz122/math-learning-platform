import { createBrowserRouter } from "react-router-dom";
import { HomePage } from "../pages/HomePage";
import { PracticePage } from "../pages/PracticePage";
import { PricingPage } from "../pages/PricingPage";
import { CodeLoginPage } from "../pages/CodeLoginPage";
import { NotFoundPage } from "../pages/NotFoundPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: "/practice",
    element: <PracticePage />,
  },
  {
    path: "/practice/:moduleKey",
    element: <PracticePage />,
  },
  {
    path: "/pricing",
    element: <PricingPage />,
  },
  {
    path: "/login",
    element: <CodeLoginPage />,
  },
  {
    path: "*",
    element: <NotFoundPage />,
  },
]);