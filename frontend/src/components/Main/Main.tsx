import './Main.css'

import CompanySelection from '../CompanySelection/CompanySelection';
import BrandPlaybook from '../BrandPlaybook/BrandPlaybook';
import ContentCreation from '../ContentCreation/ContentCreation';

function Main() {
  return (
    <main className="section main-section">
      <CompanySelection />
      <BrandPlaybook />
      <ContentCreation />
    </main>
  )
}

export default Main
