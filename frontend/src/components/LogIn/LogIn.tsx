import { useState, useEffect, useMemo, FormEvent, ChangeEvent } from "react";
import { useNavigate } from "react-router-dom";

import { FormErrors, LogInFormState } from "../../props";
import SuccessToast from "../ui/SuccessToast/SuccessToast";
import "./LogIn.css";

const INITIAL_STATE: LogInFormState = {
  email: "",
  password: "",
};

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function validate(form: LogInFormState): FormErrors {
  const errors: FormErrors = {};

  if (!form.email.trim()) {
    errors.email = "Enter your email.";
  } else if (!EMAIL_PATTERN.test(form.email)) {
    errors.email = "That email doesn't look right.";
  }

  if (!form.password) {
    errors.password = "Choose a password.";
  } else if (form.password.length < 8) {
    errors.password = "Use at least 8 characters.";
  }

  return errors;
}

export default function LogIn() {
  const [form, setForm] = useState<LogInFormState>(INITIAL_STATE);
  const [touched, setTouched] = useState<
    Partial<Record<keyof LogInFormState, boolean>>
  >({});
  const [submitAttempted, setSubmitAttempted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const navigate = useNavigate();
  const errors = useMemo(() => validate(form), [form]);

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    const { name, value } = event.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
    if (apiError) setApiError(null);
  }

  function handleBlur(event: ChangeEvent<HTMLInputElement>) {
    const { name } = event.target;
    setTouched((prev) => ({ ...prev, [name]: true }));
  }

  function showError(field: keyof LogInFormState): string | undefined {
    if (!touched[field] && !submitAttempted) return undefined;
    return errors[field];
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitAttempted(true);
    setApiError(null);

    if (Object.keys(errors).length > 0) {
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: form.email,
          password: form.password,
        }),
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        setApiError(data.message || "Failed to login to account.");
        return;
      }

      setIsSuccess(true);
    } catch (err) {
      setApiError("Network error. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  }

  useEffect(() => {
    if (!isSuccess) return;
    const timer = setTimeout(() => {
      navigate("/dashboard");
    }, 1600);
    return () => clearTimeout(timer);
  }, [isSuccess, navigate]);

  return (
    <div className="login-auth-screen">
      <div className="login-auth-card">
        <div className="login-logo-container">
          <img src="https://res.cloudinary.com/diwkfbsgv/image/upload/v1775206748/logo_u4sz9t.svg" />
        </div>

        <h1 className="login-auth-heading">Welcome back!</h1>
        <p className="login-auth-subtext">
          We'll get you right back to where you left off
        </p>

        <form className="login-auth-form" onSubmit={handleSubmit} noValidate>
          <div>
            <div className="login-field">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                name="email"
                autoComplete="email"
                placeholder="zawadi@company.com"
                type="email"
                value={form.email}
                onChange={handleChange}
                onBlur={handleBlur}
                aria-invalid={Boolean(showError("email"))}
                aria-describedby={
                  showError("email") ? "email-error" : undefined
                }
                className={
                  showError("email")
                    ? "input-primary login-input--error"
                    : "input-primary"
                }
              />
              {showError("email") && (
                <p className="login-field-error" id="email-error">
                  {errors.email}
                </p>
              )}
            </div>

            <div className="login-field">
              <label htmlFor="password">Password</label>
              <div className="login-input-with-action">
                <input
                  id="password"
                  name="password"
                  autoComplete="current-password"
                  placeholder="Enter password"
                  type="password"
                  value={form.password}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  aria-invalid={Boolean(showError("password"))}
                  aria-describedby={
                    showError("password") ? "password-error" : undefined
                  }
                  className={
                    showError("password")
                      ? "input-primary login-input--error"
                      : "input-primary"
                  }
                />
              </div>
              {showError("password") && (
                <p className="login-field-error" id="password-error">
                  {errors.password}
                </p>
              )}
            </div>
          </div>

          <button
            type="submit"
            className={`login-submit-btn btn-primary ${isSubmitting || isSuccess ? "disabled" : ""}`}
            disabled={isSubmitting || isSuccess}
          >
            {isSubmitting ? <Spinner /> : "Continue to dashboard"}
          </button>
        </form>

        <p className="login-auth-footer">
          New here? <a href="/">Create account</a>
        </p>
      </div>
      {apiError && <SuccessToast subtext={apiError} success="red" />}
      {isSuccess && (
        <SuccessToast
          title={`Welcome Back, ${form.email.trim()}!`}
          subtext="Taking you to your dashboard..."
          success="green"
        />
      )}
    </div>
  );
}

function Spinner() {
  return <span className="login-spinner" aria-hidden="true" />;
}
