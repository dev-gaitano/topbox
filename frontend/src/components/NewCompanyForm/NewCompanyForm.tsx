import "./NewCompanyForm.css"

// Modules
import { useState } from "react"

function NewCompanyForm({ newCompanyForm }: { newCompanyForm: boolean }) {
  const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

  const [formData, setFormData] = useState({
    businessName: "",
    logo: "",
    industry: "",
    email: "",
    description: "",
    targetAudience: "",
    colorPalette: "",
    uniqueValue: "",
    mainCompetitors: "",
    personality: [],
    tone: "",
  })

  // Handle form submit event
  async function handleSubmit(e: React.SubmitEvent) {
    e.preventDefault()

    try {
      // Post to endpoint
      const res = await fetch(`${API_BASE}/api/companies`, {
        method: "POST",
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
      console.error('Error posting:', e);
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
    <div className={`ncf-container ${newCompanyForm ? "" : "hidden"}`}>
      <h2>Create new company</h2>
      <form className="ncf-form" onSubmit={handleSubmit}>
        <div className="ncf-input-container">
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
            value={formData.colorPalette}
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
        <button type="submit">Create company</button>
      </form>
    </div>
  )
}

export default NewCompanyForm
