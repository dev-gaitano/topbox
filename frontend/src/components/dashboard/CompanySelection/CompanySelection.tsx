import "./CompanySelection.css";

// Components
import NewCompanyForm from "../NewCompanyForm/NewCompanyForm";

// Props
import { Company } from "../../../props";
import { CompanySelectionProps } from "../../../props";
import { useEffect, useState, useCallback } from "react";
import CompanyUpdateForm from "../CompanyUpdateForm/CompanyUpdateForm";
import { authHeaders } from "../../../utils/auth";
import SuccessToast from "../../ui/SuccessToast/SuccessToast";

// Destructure interface to get keys as function parameters
function CompanySelection({
  selectedCompany,
  onSelectCompany,
}: CompanySelectionProps) {
  const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

  const [companies, setCompanies] = useState<Company[]>([]);
  const [newCompanyForm, setNewCompanyForm] = useState(false);
  const [isHoveredId, setIsHoveredId] = useState<number | null>(null);
  const [companyUpdateForm, setCompanyUpdateForm] = useState(false);
  const [company, setCompany] = useState<Company | null>(null);
  const [toastInfo, setToastInfo] = useState<{title: string, subtext: string} | null>(null);

  const fetchCompanies = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/api/companies`, {
        headers: authHeaders(),
      });
      if (res.ok) {
        const resJson = await res.json();
        setCompanies(resJson);
      } else {
        console.error("Failed to fetch companies");
        console.log(res);
      }
    } catch (e) {
      console.error("Error fetching companies:", e);
      setCompanies([]);
    }
  }, [API_BASE]);

  // Fetch companies from api
  useEffect(() => {
    fetchCompanies();
  }, [fetchCompanies]);

  function handleNewCompany() {
    setNewCompanyForm(true);
  }

  async function handleCompanyUpdateForm(selectedCompany: Company) {
    try {
      const res = await fetch(
        `${API_BASE}/api/companies/${selectedCompany.id}`,
        { headers: authHeaders() },
      );
      const resJson = await res.json();

      if (!res.ok) {
        console.error("Failed to fetch company");
        console.log(res);
        console.log(resJson);
        return;
      }

      setCompany(selectedCompany);
      setCompanyUpdateForm(true);
      console.log(selectedCompany);
      console.log(company);
    } catch (e) {
      console.error("Error fetching company:", e);
      setCompany(selectedCompany);
    }
  }

  async function handleDelete(companyId: number) {
    try {
      const res = await fetch(`${API_BASE}/api/companies/${companyId}`, {
        method: "DELETE",
        headers: authHeaders({ "Content-Type": "application/json" }),
      });

      const data = await res.json();

      // Check if response was ok
      if (!res.ok) {
        console.error(data);
        return;
      }

      console.log(data);
    } catch (e) {
      console.error(`Error deleting: ${e}`);
    }
  }

  return (
    <section className="company-selection component">
      <div className="section-title">
        <h2>+ COMPANIES</h2>
      </div>
      <div className="cs-container">
        <button className="cs-add-new" onClick={handleNewCompany}>
          <svg
            viewBox="0 0 48 48"
            xmlns="http://www.w3.org/2000/svg"
            width="48"
            height="48"
          >
            {/* Horizonatal bar */}
            <rect x="8" y="22" width="32" height="4" rx="1" fill="#FFFFFF" />
            {/* Vertical bar */}
            <rect x="22" y="8" width="4" height="32" rx="1" fill="#FFFFFF" />
          </svg>
          <svg style={{ display: "none" }}>
            <defs>
              <filter id="displacementFilter">
                <feTurbulence
                  type="turbulence"
                  baseFrequency="0.01"
                  numOctaves="2"
                  result="turbulence"
                />
                <feDisplacementMap
                  in="SourceGraphic"
                  in2="displacementMap"
                  xChannelSelector="R"
                  yChannelSelector="G"
                  scale="200"
                />
              </filter>
            </defs>
          </svg>
        </button>
        <div className="cs-carousel">
          {/* Map saved companies */}
          {companies.map((company) => (
            <div
              key={company.id}
              className={`cs-item-wrapper ${selectedCompany?.id === company.id ? "selected" : ""}`}
              onMouseEnter={() => setIsHoveredId(company.id)}
              onMouseLeave={() => setIsHoveredId(null)}
            >
              <button
                className={`cs-action-btn cs-delete-btn ${selectedCompany?.id === company.id && isHoveredId === company.id ? "" : "hidden"}`}
                onClick={() => handleDelete(company.id)}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  height="48px"
                  viewBox="0 -960 960 960"
                  width="48px"
                  fill="#ABABAB"
                >
                  <path d="m300-258-42-42 180-180-180-179 42-42 180 180 179-180 42 42-180 179 180 180-42 42-179-180-180 180Z" />
                </svg>
              </button>
              <div
                onClick={() => onSelectCompany?.(company)}
                className="cs-company-item"
              >
                <img
                  className="cs-company-logo"
                  src={company.logo}
                  alt="logo-img"
                />
                {selectedCompany?.id === company.id ? (
                  <h2 className="cs-company-name">
                    {company.name.toUpperCase()}
                  </h2>
                ) : (
                  <h2 className="cs-company-name"></h2>
                )}
              </div>
              <button
                onClick={() => handleCompanyUpdateForm(company)}
                className={`cs-action-btn cs-edit-btn ${selectedCompany?.id === company.id &&
                    isHoveredId === company.id
                    ? ""
                    : "hidden"
                  }`}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  height="32px"
                  viewBox="0 -960 960 960"
                  width="32px"
                  fill="hsla(0, 0%, 67%, 1)"
                >
                  <path d="M180-180h44l472-471-44-44-472 471v44Zm-60 60v-128l575-574q8-8 19-12.5t23-4.5q11 0 22 4.5t20 12.5l44 44q9 9 13 20t4 22q0 11-4.5 22.5T823-694L248-120H120Zm659-617-41-41 41 41Zm-105 64-22-22 44 44-22-22Z" />
                </svg>
              </button>
            </div>
          ))}
        </div>
      </div>
      <NewCompanyForm
        newCompanyForm={newCompanyForm}
        setNewCompanyForm={setNewCompanyForm}
        onSuccess={() => {
          setNewCompanyForm(false);
          fetchCompanies();
          setToastInfo({ title: "Company created!", subtext: "Successfully added company." });
          setTimeout(() => setToastInfo(null), 1600);
        }}
      />
      <CompanyUpdateForm
        companyUpdateForm={companyUpdateForm}
        setCompanyUpdateForm={setCompanyUpdateForm}
        company={company}
        onSuccess={() => {
          setCompanyUpdateForm(false);
          fetchCompanies();
          setToastInfo({ title: "Company updated!", subtext: "Successfully saved changes." });
          setTimeout(() => setToastInfo(null), 1600);
        }}
      />
      {toastInfo && (
        <SuccessToast
          title={toastInfo.title}
          subtext={toastInfo.subtext}
          success="green"
        />
      )}
    </section>
  );
}

export default CompanySelection;
