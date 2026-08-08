import { Company } from "../../../props";
import "./CompanyUpdateForm.css";

import { useState, useEffect, useMemo, ChangeEvent } from "react";
import { authHeaders } from "../../../utils/auth";
import ColorPalettePicker from "../../ui/ColorPalettePicker/ColorPalettePicker";

type FormState = {
  businessName: string;
  logo: string;
  industry: string;
  email: string;
  description: string;
  targetAudience: string;
  colorPalette: string[];
  uniqueValue: string;
  mainCompetitors: string;
  personality: string;
  tone: string;
};

const INITIAL_STATE: FormState = {
  businessName: "",
  logo: "",
  industry: "",
  email: "",
  description: "",
  targetAudience: "",
  colorPalette: [],
  uniqueValue: "",
  mainCompetitors: "",
  personality: "",
  tone: "",
};

function validate(form: FormState) {
  const errors: Partial<Record<keyof FormState, string>> = {};

  if (!form.businessName.trim()) errors.businessName = "Enter company name.";
  if (!form.logo.trim()) errors.logo = "Enter logo URL.";
  if (!form.industry) errors.industry = "Select industry.";
  if (!form.email.trim()) errors.email = "Enter email.";

  if (!form.description.trim()) errors.description = "Enter description.";
  if (!form.targetAudience.trim())
    errors.targetAudience = "Enter target audience.";
  if (form.colorPalette.length < 5)
    errors.colorPalette = "Pick at least 5 colors.";

  if (!form.personality) errors.personality = "Enter brand personality.";
  if (!form.tone.trim()) errors.tone = "Enter brand tone.";

  return errors;
}

const STEP_FIELDS = {
  1: ["businessName", "logo", "industry", "email"],
  2: ["description", "targetAudience", "colorPalette"],
  3: ["uniqueValue", "mainCompetitors"],
  4: ["personality", "tone"],
} as const;

function CompanyUpdateForm({
  companyUpdateForm,
  setCompanyUpdateForm,
  company,
  onSuccess,
}: {
  companyUpdateForm: boolean;
  setCompanyUpdateForm: React.Dispatch<React.SetStateAction<boolean>>;
  company: Company | null;
  onSuccess?: () => void;
}) {
  const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<FormState>(INITIAL_STATE);
  const [touched, setTouched] = useState<
    Partial<Record<keyof FormState, boolean>>
  >({});
  const [submitAttempted, setSubmitAttempted] = useState(false);

  // Get fresh company data on render
  useEffect(() => {
    if (company) {
      setFormData({
        businessName: company.name || "",
        logo: company.logo || "",
        industry: company.industry || "",
        email: company.email || "",
        description: company.description || "",
        targetAudience: company.target_audience || "",
        colorPalette: Array.isArray(company.color_palette)
          ? company.color_palette
          : company.color_palette
            ? [company.color_palette]
            : [],
        uniqueValue: company.unique_value || "",
        mainCompetitors: Array.isArray(company.main_competitors)
          ? company.main_competitors.join(", ")
          : company.main_competitors || "",
        personality: Array.isArray(company.personality)
          ? company.personality.join(", ")
          : company.personality || "",
        tone: company.tone || "",
      });
    }
  }, [company]);

  const errors = useMemo(() => validate(formData), [formData]);

  function handleChange(
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>,
  ) {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  }

  function handleBlur(
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>,
  ) {
    const { name } = e.target;
    setTouched((prev) => ({ ...prev, [name]: true }));
  }

  function showError(field: keyof FormState): string | undefined {
    if (!touched[field] && !submitAttempted) return undefined;
    return errors[field];
  }

  // Handle form submit event
  async function handleSubmit(companyId: number) {
    setSubmitAttempted(true);

    const currentStepFields = STEP_FIELDS[step as keyof typeof STEP_FIELDS];
    const hasErrorsInCurrentStep = currentStepFields.some(
      (field) => errors[field as keyof FormState],
    );

    if (hasErrorsInCurrentStep) {
      return;
    }

    if (step < 4) {
      setStep((prev) => prev + 1);
      setSubmitAttempted(false); // Reset for next step
      return;
    }

    try {
      // Post to endpoint
      const res = await fetch(`${API_BASE}/api/companies/${companyId}`, {
        method: "PATCH",
        headers: authHeaders({ "Content-Type": "application/json" }),
        body: JSON.stringify({
          ...formData,
          personality: formData.personality ? [formData.personality] : [],
          mainCompetitors: formData.mainCompetitors
            ? [formData.mainCompetitors]
            : [],
          colorPalette: formData.colorPalette,
        }),
      });

      // Get response data
      const data = await res.json();

      // Check if response was ok
      if (!res.ok) {
        console.error(data);
        return;
      }

      console.log(data);
      if (onSuccess) onSuccess();
      setStep(1);
      setSubmitAttempted(false);
    } catch (e) {
      console.error("Error patching:", e);
    }
  }

  return (
    <div className={`cuf-container ${!companyUpdateForm ? "hidden" : ""}`}>
      <div className="cuf-header">
        <h2>Update {company?.name}</h2>
        <button
          className="cuf-close-btn"
          type="button"
          onClick={() => {
            setCompanyUpdateForm(false);
            setStep(1);
            setSubmitAttempted(false);
            setTouched({});
          }}
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
      <form
        className="cuf-form"
        onSubmit={(e) => {
          e.preventDefault();
          if (company?.id) {
            handleSubmit(company.id);
          }
        }}
        noValidate
      >
        <div className="cuf-input-container">
          {step === 1 && (
            <>
              <div className="cuf-field">
                <input
                  name="businessName"
                  placeholder="Company name"
                  value={formData.businessName}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("businessName") ? "cuf-input--error" : ""}`}
                />
                {showError("businessName") && (
                  <p className="cuf-field-error">{errors.businessName}</p>
                )}
              </div>

              <div className="cuf-field">
                <input
                  name="logo"
                  placeholder="Logo"
                  value={formData.logo}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("logo") ? "cuf-input--error" : ""}`}
                />
                {showError("logo") && (
                  <p className="cuf-field-error">{errors.logo}</p>
                )}
              </div>

              <div className="cuf-field">
                <select
                  name="industry"
                  value={formData.industry}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("industry") ? "cuf-input--error" : ""}`}
                >
                  <option value="" disabled>
                    Select industry
                  </option>
                  <option value="Technology">Technology</option>
                  <option value="Healthcare">Healthcare</option>
                  <option value="Finance">Finance</option>
                  <option value="Education">Education</option>
                  <option value="Retail">Retail</option>
                  <option value="Manufacturing">Manufacturing</option>
                  <option value="Entertainment">Entertainment</option>
                  <option value="Other">Other</option>
                </select>
                {showError("industry") && (
                  <p className="cuf-field-error">{errors.industry}</p>
                )}
              </div>

              <div className="cuf-field">
                <input
                  name="email"
                  placeholder="Email"
                  value={formData.email}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("email") ? "cuf-input--error" : ""}`}
                />
                {showError("email") && (
                  <p className="cuf-field-error">{errors.email}</p>
                )}
              </div>
            </>
          )}

          {step === 2 && (
            <>
              <div className="cuf-field">
                <textarea
                  name="description"
                  placeholder="Description"
                  value={formData.description}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("description") ? "cuf-input--error" : ""}`}
                />
                {showError("description") && (
                  <p className="cuf-field-error">{errors.description}</p>
                )}
              </div>

              <div className="cuf-field">
                <input
                  name="targetAudience"
                  placeholder="Target Audience"
                  value={formData.targetAudience}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("targetAudience") ? "cuf-input--error" : ""}`}
                />
                {showError("targetAudience") && (
                  <p className="cuf-field-error">{errors.targetAudience}</p>
                )}
              </div>

              <div className="cuf-field">
                <ColorPalettePicker
                  colors={formData.colorPalette}
                  onChange={(colors) =>
                    setFormData((prev) => ({ ...prev, colorPalette: colors }))
                  }
                  error={showError("colorPalette")}
                  minColors={5}
                />
              </div>
            </>
          )}

          {step === 3 && (
            <>
              <div className="cuf-field">
                <input
                  name="uniqueValue"
                  placeholder="Unique value"
                  value={formData.uniqueValue}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("uniqueValue") ? "cuf-input--error" : ""}`}
                />
                {showError("uniqueValue") && (
                  <p className="cuf-field-error">{errors.uniqueValue}</p>
                )}
              </div>

              <div className="cuf-field">
                <input
                  name="mainCompetitors"
                  placeholder="Main competitors"
                  value={formData.mainCompetitors}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("mainCompetitors") ? "cuf-input--error" : ""}`}
                />
                {showError("mainCompetitors") && (
                  <p className="cuf-field-error">{errors.mainCompetitors}</p>
                )}
              </div>
            </>
          )}

          {step === 4 && (
            <>
              <div className="cuf-field">
                <input
                  name="personality"
                  placeholder="Brand personality"
                  value={formData.personality}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("personality") ? "cuf-input--error" : ""}`}
                />
                {showError("personality") && (
                  <p className="cuf-field-error">{errors.personality}</p>
                )}
              </div>

              <div className="cuf-field">
                <input
                  name="tone"
                  placeholder="Brand tone"
                  value={formData.tone}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("tone") ? "cuf-input--error" : ""}`}
                />
                {showError("tone") && (
                  <p className="cuf-field-error">{errors.tone}</p>
                )}
              </div>
            </>
          )}
        </div>

        <div
          style={{ display: "flex", gap: "16px", justifyContent: "flex-end" }}
        >
          {step > 1 && (
            <button
              className="btn-secondary"
              type="button"
              onClick={() => {
                setStep((prev) => prev - 1);
                setSubmitAttempted(false);
              }}
            >
              Back
            </button>
          )}
          <button className="btn-primary" type="submit">
            {step < 4 ? "Next" : "Update company"}
          </button>
        </div>
      </form>
    </div>
  );
}

export default CompanyUpdateForm;
