import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Analytics } from "@vercel/analytics/react";
import SignUpPage from "./pages/SignUpPage";
import DashboardPage from "./pages/DashboardPage";
import LogInPage from "./pages/LogInPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SignUpPage />} />
        <Route path="/login" element={<LogInPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
      <Analytics />
    </BrowserRouter>
  );
}

export default App;
