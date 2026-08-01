import "./NewCompanyForm.css";

// Modules
import { useState } from "react";

function NewCompanyForm({
  newCompanyForm,
  setNewCompanyForm,
}: {
  newCompanyForm: boolean;
  setNewCompanyForm: React.Dispatch<React.SetStateAction<boolean>>;
}) {
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
  });

  // Handle form submit event
  async function handleSubmit(e: React.SubmitEvent) {
    e.preventDefault();

    try {
      // Post to endpoint
      const res = await fetch(`${API_BASE}/api/companies`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      // Get response data
      const data = await res.json();

      // Check if response was ok
      if (!res.ok) {
        console.error(data);
        return;
      }

      console.log(data);
      alert("Company added successfully!");
      setNewCompanyForm(false);
    } catch (e) {
      console.error("Error posting:", e);
    }
  }

  // Handle input value change event
  function handleChange(
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >,
  ) {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  }

  return (
    <div className={`ncf-container ${newCompanyForm ? "" : "hidden"}`}>
      <div className="ncf-header">
        <h2>Create new company</h2>
        <button
          className="ncf-close-btn"
          onClick={() => setNewCompanyForm(false)}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="24px"
            viewBox="0 -960 960 960"
            width="24px"
            fill="#ABABAB"
          >
            <path d="m300-258-42-42 180-180-180-179 42-42 180 180 179-180 42 42-180 179 180 180-42 42-179-180-180 180Z" />
          </svg>
        </button>
      </div>
      <form className="ncf-form" onSubmit={handleSubmit}>
        <div className="ncf-input-container">
          <input
            name="businessName"
            placeholder="Company name"
            value={formData.businessName}
            onChange={handleChange}
            className="input-primary"
          />
          <input
            name="logo"
            placeholder="Logo"
            value={formData.logo}
            onChange={handleChange}
            className="input-primary"
          />
          <input
            name="industry"
            value={formData.industry}
            onChange={handleChange}
          />
          <input
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            className="input-primary"
          />
          <textarea
            name="description"
            placeholder="Description"
            value={formData.description}
            onChange={handleChange}
            className="input-primary"
          />
          <input
            name="targetAudience"
            placeholder="targetAudience"
            value={formData.targetAudience}
            onChange={handleChange}
            className="input-primary"
          />
          <input
            name="colorPalette"
            placeholder="Color palette"
            value={formData.colorPalette}
            onChange={handleChange}
            className="input-primary"
          />
          <input
            name="uniqueValue"
            placeholder="Unique value"
            value={formData.uniqueValue}
            onChange={handleChange}
            className="input-primary"
          />
          <input
            name="mainCompetitors"
            placeholder="Main competitors"
            value={formData.mainCompetitors}
            onChange={handleChange}
            className="input-primary"
          />
          <input
            name="personality"
            placeholder="Brand personality"
            value={formData.personality}
            onChange={handleChange}
            className="input-primary"
          />
          <input
            name="tone"
            placeholder="Brand tone"
            value={formData.tone}
            onChange={handleChange}
            className="input-primary"
          />
        </div>
        <button className="btn-primary" type="submit">
          Create company
        </button>
      </form>
    </div>
  );
}

export default NewCompanyForm;
