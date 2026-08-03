import Header from "../components/dashboard/Header/Header";
import Main from "../components/dashboard/Main/Main";
import MobileNav, { Tab } from "../components/dashboard/MobileNav/MobileNav";
import { Analytics } from "@vercel/analytics/react";
import { useState } from "react";

function DashboardPage() {
  const [activeTab, setActiveTab] = useState<Tab>("playbook");

  return (
    <div>
      <div className="root-container">
        {Array.from({ length: 40 }).map((_, i) => (
          <div
            key={i}
            style={{
              position: "absolute",
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              width: Math.random() > 0.8 ? 2 : 1,
              height: Math.random() > 0.8 ? 2 : 1,
              borderRadius: "50%",
              background: "rgba(255,255,255,0.6)",
              animation: `twinkle ${2 + Math.random() * 4}s ease-in-out infinite`,
              animationDelay: `${Math.random() * 4}s`,
            }}
          />
        ))}
        <Header />
        <Main activeTab={activeTab} />
      </div>
      <MobileNav activeTab={activeTab} onTabChange={setActiveTab} />
      <Analytics />
    </div>
  );
}

export default DashboardPage;
