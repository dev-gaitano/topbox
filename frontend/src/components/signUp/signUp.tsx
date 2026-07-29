import { useState, useMemo, FormEvent, ChangeEvent } from "react";
import "./signUp.css";
import { SignUpFormState } from "../../props";
import { SignUpFormErrors } from "../../props";
import SuccessToast from "../ui/SuccessToast/SuccessToast";

const INITIAL_STATE: SignUpFormState = {
  username: "",
  email: "",
  password: "",
  confirmPassword: "",
};

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function validate(form: SignUpFormState): SignUpFormErrors {
  const errors: SignUpFormErrors = {};

  if (!form.username.trim()) {
    errors.username = "Enter your username.";
  }

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

  if (!form.confirmPassword) {
    errors.confirmPassword = "Confirm your password.";
  } else if (form.confirmPassword !== form.password) {
    errors.confirmPassword = "Passwords don't match.";
  }

  return errors;
}

export default function SignUp() {
  const [form, setForm] = useState<SignUpFormState>(INITIAL_STATE);
  const [touched, setTouched] = useState<
    Partial<Record<keyof SignUpFormState, boolean>>
  >({});
  const [submitAttempted, setSubmitAttempted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const errors = useMemo(() => validate(form), [form]);

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    const { name, value } = event.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  }

  function handleBlur(event: ChangeEvent<HTMLInputElement>) {
    const { name } = event.target;
    setTouched((prev) => ({ ...prev, [name]: true }));
  }

  function showError(field: keyof SignUpFormErrors): string | undefined {
    if (!touched[field] && !submitAttempted) return undefined;
    return errors[field];
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitAttempted(true);

    if (Object.keys(errors).length > 0) {
      return;
    }

    setIsSubmitting(true);
    // Replace with a request to signup endpoint.
    await new Promise((resolve) => setTimeout(resolve, 900));
    setIsSubmitting(false);
    setIsSuccess(true);
  }

  return (
    <div className="auth-screen">
      <div className="auth-card">
        <div className="logo-container">
          <img src="https://res.cloudinary.com/diwkfbsgv/image/upload/v1775206748/logo_u4sz9t.svg" />
        </div>

        <h1 className="auth-heading">Create your account</h1>
        <p className="auth-subtext">Set up your workspace in under a minute.</p>

        <form className="auth-form" onSubmit={handleSubmit} noValidate>
          <div>
            <div>
              <div className="field">
                <label htmlFor="username">Username</label>
                <input
                  id="username"
                  name="username"
                  type="text"
                  autoComplete="name"
                  placeholder="Jordan Rivers"
                  value={form.username}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  aria-invalid={Boolean(showError("username"))}
                  aria-describedby={
                    showError("username") ? "username-error" : undefined
                  }
                  className={
                    showError("username")
                      ? "input-primary input--error"
                      : "input-primary"
                  }
                />
                {showError("username") && (
                  <p className="field-error" id="username-error">
                    {errors.username}
                  </p>
                )}
              </div>

              <div className="field">
                <label htmlFor="email">Email</label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  placeholder="jordan@company.com"
                  value={form.email}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  aria-invalid={Boolean(showError("email"))}
                  aria-describedby={
                    showError("email") ? "email-error" : undefined
                  }
                  className={
                    showError("email")
                      ? "input-primary input--error"
                      : "input-primary"
                  }
                />
                {showError("email") && (
                  <p className="field-error" id="email-error">
                    {errors.email}
                  </p>
                )}
              </div>
            </div>

            <div>
              <div className="field">
                <label htmlFor="password">Password</label>
                <div className="input-with-action">
                  <input
                    id="password"
                    name="password"
                    autoComplete="new-password"
                    placeholder="At least 8 characters"
                    value={form.password}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    aria-invalid={Boolean(showError("password"))}
                    aria-describedby={
                      showError("password") ? "password-error" : undefined
                    }
                    className={
                      showError("password")
                        ? "input-primary input--error"
                        : "input-primary"
                    }
                  />
                </div>
                {showError("password") && (
                  <p className="field-error" id="password-error">
                    {errors.password}
                  </p>
                )}
              </div>

              <div className="field">
                <label htmlFor="confirmPassword">Confirm password</label>
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  autoComplete="new-password"
                  placeholder="Type it again"
                  value={form.confirmPassword}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  aria-invalid={Boolean(showError("confirmPassword"))}
                  aria-describedby={
                    showError("confirmPassword")
                      ? "confirmPassword-error"
                      : undefined
                  }
                  className={
                    showError("confirmPassword")
                      ? "input-primary input--error"
                      : "input-primary"
                  }
                />
                {showError("confirmPassword") && (
                  <p className="field-error" id="confirmPassword-error">
                    {errors.confirmPassword}
                  </p>
                )}
              </div>
            </div>
          </div>

          <button
            type="submit"
            className="signup-submit-btn btn-primary"
            disabled={isSubmitting}
          >
            {isSubmitting ? <Spinner /> : "Create account"}
          </button>
        </form>

        <p className="auth-footer">
          Already have an account? <a href="#login">Log in</a>
        </p>
      </div>
      {isSuccess && (
        <SuccessToast
          title={`You're in, ${form.username.split(" ")[0]}`}
          subtext="Taking you to your dashboard..."
          success="green"
        />
      )}
    </div>
  );
}

function Spinner() {
  return <span className="spinner" aria-hidden="true" />;
}
