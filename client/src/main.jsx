import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
)
// Setup global resize handlers for panels to avoid errors
window.addEventListener('error', e => {
  if (e.message === 'ResizeObserver loop limit exceeded') {
    e.stopImmediatePropagation();
  }
});
