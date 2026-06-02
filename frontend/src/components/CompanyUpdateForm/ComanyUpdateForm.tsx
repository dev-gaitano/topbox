import { Company } from "../../props";
import "./ComanyUpdateForm.css"

import { useState, useEffect } from "react";

function CompanyUpdateForm(
  { companyUpdateForm, company }: { companyUpdateForm: boolean, company: Company | null }
) {
  const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

  const [formData, setFormData] = useState({
    businessName: company?.name,
    logo: company?.logo,
    industry: company?.industry,
    email: company?.email,
    description: company?.description,
    targetAudience: company?.target_audience,
    colorPalette: company?.color_palette,
    uniqueValue: company?.unique_value,
    mainCompetitors: company?.main_competitors,
    personality: company?.personality,
    tone: company?.tone,
  })

  // Get fresh company data on render
  useEffect(() => {
    if (company) {
      setFormData({
        businessName: company.name,
        logo: company.logo,
        industry: company.industry,
        email: company.email,
        description: company.description,
        targetAudience: company.target_audience,
        colorPalette: company.color_palette,
        uniqueValue: company.unique_value || "",
        mainCompetitors: company.main_competitors || [],
        personality: company.personality,
        tone: company.tone || "",
      });
    }
  }, [company])


  // Handle form submit event
  async function handleSubmit(companyId: number) {
    try {
      // Post to endpoint
      const res = await fetch(`${API_BASE}/api/companies/${companyId}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData)
      })

      // Get response data
      const data = await res.json()

      // Check if response was ok
      if (!res.ok) {
        console.error(data);
        return
      }

      console.log(data);
    } catch (e) {
      console.error('Error patching:', e);
    }
  }

  // Handle input value change event
  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  return (
    <div className={`cuf-container ${!companyUpdateForm ? "hidden" : ""}`}>
      <h2>Update {company?.name}</h2>
      <form className="cuf-form" onSubmit={(e) => {
        e.preventDefault()
        handleSubmit(company.id)
      }}>
        <div className="cuf-input-container">
          <input
            name="businessName"
            placeholder="Company name"
            value={formData.businessName}
            onChange={handleChange}
          />
          <input
            name="logo"
            placeholder="Logo"
            value={formData.logo}
            onChange={handleChange}
          />
          <select
            name="industry"
            value={formData.industry}
            onChange={handleChange}
          ></select>
          <input
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
          />
          <textarea
            name="description"
            placeholder="Description"
            value={formData.description}
            onChange={handleChange}
          />
          <input
            name="targetAudience"
            placeholder="targetAudience"
            value={formData.targetAudience}
            onChange={handleChange}
          />
          <input
            name="colorPalette"
            placeholder="Color palette"
            value={formData.colorPalette}
            onChange={handleChange}
          />
          <input
            name="uniqueValue"
            placeholder="Unique value"
            value={formData.uniqueValue}
            onChange={handleChange}
          />
          <input
            name="mainCompetitors"
            placeholder="Main competitors"
            value={formData.mainCompetitors}
            onChange={handleChange}
          />
          <input
            name="personality"
            placeholder="Brand personality"
            value={formData.personality}
            onChange={handleChange}
          />
          <input
            name="tone"
            placeholder="Brand tone"
            value={formData.tone}
            onChange={handleChange}
          />
        </div>
        <button type="submit">Update company</button>
      </form>
    </div>
  )
}

export default CompanyUpdateForm
