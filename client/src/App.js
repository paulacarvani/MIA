import React, { useEffect, useState } from 'react'
import Navbar from './components/navbar'
import Slider from './components/slider'
import Footer from './components/footer'

function App() {

  const [backendData, setBackendData] = useState ([{}])
  useEffect(() => {
    fetch("/api").then(
      response => response.json()
    ).then(
      data => {
        setBackendData(data)
      }
    )
  }, [])
  return (
    <div>
      <Navbar />
      <Slider/>
      <Footer/>
    </div>
  )
}

export default App