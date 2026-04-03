import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Analytics } from '@vercel/analytics/react'

function App() {
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <div className="root-container">
              <header></header>
              <main></main>
              <footer></footer>
            </div>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <Analytics />
    </Router>
  );
}

export default App;
