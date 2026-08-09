import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router'

import articleService from './services/articles'

import Navbar from './components/Navbar'
import Tech from './pages/Tech'

function App() {

  const [articles, setArticles] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const fetchArticles = async () => {
    setLoading(true)
    const result = await articleService.getArticles()

    if (result.error) {
      setError(result.error)
    } else {
      setArticles(result.data)
    }

    setLoading(false)
  }

  useEffect(() => {
    fetchArticles()
  }, [])

  return (
    <BrowserRouter>
    {loading? <p>Loading ... </p> : <></>}
    {error? <p>{`Error occurred: ${error}`} </p> : <></>}
    <Navbar />
      <Routes>
        <Route path='/' element={<Tech />} />
        <Route path='/finance' />
        <Route path='/fintech' />
      </Routes>
    </BrowserRouter>
  )
}

export default App
