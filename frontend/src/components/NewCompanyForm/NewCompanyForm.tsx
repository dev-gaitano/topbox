import "./NewCompanyForm.css";

// Modules
import { useState, useMemo, FormEvent, ChangeEvent } from "react";
import { authHeaders } from "../../utils/auth";
import ColorPalettePicker from "../ui/ColorPalettePicker/ColorPalettePicker";

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

  if (!form.personality.trim()) errors.personality = "Enter brand personality.";
  if (!form.tone.trim()) errors.tone = "Enter brand tone.";

  return errors;
}

const STEP_FIELDS = {
  1: ["businessName", "logo", "industry", "email"],
  2: ["description", "targetAudience", "colorPalette"],
  3: ["uniqueValue", "mainCompetitors"],
  4: ["personality", "tone"],
} as const;

function NewCompanyForm({
  newCompanyForm,
  setNewCompanyForm,
  onSuccess,
}: {
  newCompanyForm: boolean;
  setNewCompanyForm: React.Dispatch<React.SetStateAction<boolean>>;
  onSuccess?: () => void;
}) {
  const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<FormState>(INITIAL_STATE);
  const [touched, setTouched] = useState<
    Partial<Record<keyof FormState, boolean>>
  >({});
  const [submitAttempted, setSubmitAttempted] = useState(false);

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
  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
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
      const res = await fetch(`${API_BASE}/api/companies`, {
        method: "POST",
        headers: authHeaders({ "Content-Type": "application/json" }),
        body: JSON.stringify({
          ...formData,
          personality: [formData.personality], // API expects array
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        console.error(data);
        return;
      }

      console.log(data);
      if (onSuccess) {
        onSuccess();
      }
      setStep(1);
      setFormData(INITIAL_STATE);
      setTouched({});
      setSubmitAttempted(false);
    } catch (e) {
      console.error("Error posting:", e);
    }
  }

  return (
    <div className={`ncf-container ${newCompanyForm ? "" : "hidden"}`}>
      <div className="ncf-header">
        <h2>Create new company</h2>
        <button
          className="ncf-close-btn"
          type="button"
          onClick={() => {
            setNewCompanyForm(false);
            setStep(1); // Reset on close
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
      <form className="ncf-form" onSubmit={handleSubmit} noValidate>
        <div className="ncf-input-container">
          {step === 1 && (
            <>
              <div className="ncf-field">
                <input
                  name="businessName"
                  placeholder="Company name"
                  value={formData.businessName}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("businessName") ? "ncf-input--error" : ""}`}
                />
                {showError("businessName") && (
                  <p className="ncf-field-error">{errors.businessName}</p>
                )}
              </div>

              <div className="ncf-field">
                <input
                  name="logo"
                  placeholder="Logo"
                  value={formData.logo}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("logo") ? "ncf-input--error" : ""}`}
                />
                {showError("logo") && (
                  <p className="ncf-field-error">{errors.logo}</p>
                )}
              </div>

              <div className="ncf-field">
                <select
                  name="industry"
                  value={formData.industry}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary industry${showError("industry") ? "ncf-input--error" : ""}`}
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
                  <option value="Fashion & Apparel">Fashion & Apparel</option>
                  <option value="Other">Other</option>
                </select>
                {showError("industry") && (
                  <p className="ncf-field-error">{errors.industry}</p>
                )}
              </div>

              <div className="ncf-field">
                <input
                  name="email"
                  placeholder="Email"
                  value={formData.email}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("email") ? "ncf-input--error" : ""}`}
                />
                {showError("email") && (
                  <p className="ncf-field-error">{errors.email}</p>
                )}
              </div>
            </>
          )}

          {step === 2 && (
            <>
              <div className="ncf-field">
                <textarea
                  name="description"
                  placeholder="Description"
                  value={formData.description}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("description") ? "ncf-input--error" : ""}`}
                />
                {showError("description") && (
                  <p className="ncf-field-error">{errors.description}</p>
                )}
              </div>

              <div className="ncf-field">
                <input
                  name="targetAudience"
                  placeholder="Target Audience"
                  value={formData.targetAudience}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("targetAudience") ? "ncf-input--error" : ""}`}
                />
                {showError("targetAudience") && (
                  <p className="ncf-field-error">{errors.targetAudience}</p>
                )}
              </div>

              <div className="ncf-field">
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
              <div className="ncf-field">
                <input
                  name="uniqueValue"
                  placeholder="Unique value"
                  value={formData.uniqueValue}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("uniqueValue") ? "ncf-input--error" : ""}`}
                />
                {showError("uniqueValue") && (
                  <p className="ncf-field-error">{errors.uniqueValue}</p>
                )}
              </div>

              <div className="ncf-field">
                <input
                  name="mainCompetitors"
                  placeholder="Main competitors"
                  value={formData.mainCompetitors}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("mainCompetitors") ? "ncf-input--error" : ""}`}
                />
                {showError("mainCompetitors") && (
                  <p className="ncf-field-error">{errors.mainCompetitors}</p>
                )}
              </div>
            </>
          )}

          {step === 4 && (
            <>
              <div className="ncf-field">
                <input
                  name="personality"
                  placeholder="Brand personality"
                  value={formData.personality}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("personality") ? "ncf-input--error" : ""}`}
                />
                {showError("personality") && (
                  <p className="ncf-field-error">{errors.personality}</p>
                )}
              </div>

              <div className="ncf-field">
                <input
                  name="tone"
                  placeholder="Brand tone"
                  value={formData.tone}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={`input-primary ${showError("tone") ? "ncf-input--error" : ""}`}
                />
                {showError("tone") && (
                  <p className="ncf-field-error">{errors.tone}</p>
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
            {step < 4 ? "Next" : "Create company"}
          </button>
        </div>
      </form>
    </div>
  );
}

export default NewCompanyForm;
