import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [apiStatus, setApiStatus] = useState<string>('Loading...')
  const [healthStatus, setHealthStatus] = useState<string>('Loading...')
  const [testMessage, setTestMessage] = useState<string>('Loading...')

  useEffect(() => {
    // Test root endpoint
    fetch('http://localhost:8000/')
      .then(response => response.json())
      .then(data => setApiStatus(JSON.stringify(data)))
      .catch(error => setApiStatus(`Error: ${error.message}`))

    // Test health endpoint
    fetch('http://localhost:8000/health')
      .then(response => response.json())
      .then(data => setHealthStatus(JSON.stringify(data)))
      .catch(error => setHealthStatus(`Error: ${error.message}`))

    // Test API endpoint
    fetch('http://localhost:8000/api/test')
      .then(response => response.json())
      .then(data => setTestMessage(JSON.stringify(data)))
      .catch(error => setTestMessage(`Error: ${error.message}`))
  }, [])

  return (
    <div className="container">
      <h1>QT.AI Trading Bot</h1>
      <div className="card">
        <h2>API Status</h2>
        <pre>{apiStatus}</pre>
      </div>
      <div className="card">
        <h2>Health Status</h2>
        <pre>{healthStatus}</pre>
      </div>
      <div className="card">
        <h2>Test Message</h2>
        <pre>{testMessage}</pre>
      </div>
    </div>
  )
}

export default App
