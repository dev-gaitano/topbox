import "./Main.css";

// Components
import CompanySelection from "../CompanySelection/CompanySelection";
import BrandPlaybook from "../BrandPlaybook/BrandPlaybook";
import ContentManagement from "../ContentManagement/ContentManagement";

// Props
import { Company } from "../../../props";

// Modules
import { useState } from "react";

// Types
import { Tab } from "../MobileNav/MobileNav";

interface MainProps {
  activeTab: Tab;
}

function Main({ activeTab }: MainProps) {
  // Define state variable to manage state of selected company
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);

  return (
    <main className="section main-section">
      {/* Always visible */}
      <CompanySelection
        selectedCompany={selectedCompany}
        onSelectCompany={setSelectedCompany}
      />

      {/* Tab-switched on mobile, always visible on desktop */}
      <div className={`main-tab-panel${activeTab === "playbook" ? " main-tab-panel--visible" : ""}`}>
        <BrandPlaybook selectedCompany={selectedCompany} />
      </div>
      <div className={`main-tab-panel${activeTab === "content" ? " main-tab-panel--visible" : ""}`}>
        <ContentManagement />
      </div>
    </main>
  );
}

export default Main;
