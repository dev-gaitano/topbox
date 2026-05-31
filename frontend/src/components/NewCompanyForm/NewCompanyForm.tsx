import "./NewCompanyForm.css"

function NewCompanyForm({ newCompanyForm }: { newCompanyForm: boolean }) {

  return (
    <div className={`ncf-container ${newCompanyForm ? "" : "hidden"}`}>
      <h2>Create new company</h2>
      <form className="ncf-form">
        <div className="ncf-input-container">
          <input placeholder="Company name" />
          <input placeholder="logo" />
          <select></select>
          <input placeholder="email" />
          <textarea />
          <input placeholder="target audience" />
          <input placeholder="color palette" />
          <input placeholder="unique value" />
          <input placeholder="main competitors" />
          <input placeholder="tone" />
        </div>
        <button type="submit">Create company</button>
      </form>
    </div>
  )
}

export default NewCompanyForm
