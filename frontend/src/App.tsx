import Header from './components/Header/Header';
import Main from './components/Main/Main';
import Footer from './components/Footer/Footer';
import { Analytics } from '@vercel/analytics/react'

function App() {
  return (
    <div className="app">
      <div className="root-container">
        <Header />
        <Main />
        <Footer />
      </div>
      <Analytics />
    </div>
  );
}

export default App;
