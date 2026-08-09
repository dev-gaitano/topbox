import "./MobileNav.css";

export type Tab = "playbook" | "content";

interface MobileNavProps {
  activeTab: Tab;
  onTabChange: (tab: Tab) => void;
}

function MobileNav({ activeTab, onTabChange }: MobileNavProps) {
  return (
    <nav className="mobile-nav">
      <button
        className={`mobile-nav-item${activeTab === "playbook" ? " active" : ""}`}
        onClick={() => onTabChange("playbook")}
        aria-label="Playbook"
      >
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
          <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
          <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
          <line x1="9" y1="7" x2="15" y2="7" />
          <line x1="9" y1="11" x2="15" y2="11" />
          <line x1="9" y1="15" x2="12" y2="15" />
        </svg>
        <span>Playbook</span>
      </button>

      <button
        className={`mobile-nav-item${activeTab === "content" ? " active" : ""}`}
        onClick={() => onTabChange("content")}
        aria-label="Content"
      >
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
          <rect x="3" y="3" width="18" height="18" rx="2" />
          <path d="M3 9h18" />
          <path d="M9 21V9" />
        </svg>
        <span>Content</span>
      </button>
    </nav>
  );
}

export default MobileNav;
