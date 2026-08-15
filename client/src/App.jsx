import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router'

import techArticlesService from './services/techArticles'
import financeArticlesService from './services/financeArticles'

import Navbar from './components/Navbar'
import Finance from './pages/Finance'
import Tech from './pages/Tech'

function App() {

  const [techArticles, setTechArticles] = useState([])
  const [financeArticles, setFinanceArticles] = useState([])

  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const fetchArticles = async () => {
    setLoading(true)
    const techResult = await techArticlesService.getArticles()

    if (techResult.error) {
      setError(techResult.error)
    } else {
      setTechArticles(techResult.data)
    }

    const financeResult = await financeArticlesService.getArticles()
    
    if (financeResult.error) {
      setError(financeResult.error)
    } else {
      setFinanceArticles(financeResult.data)
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
        <Route path='/' element={<Tech techArticles={techArticles}/>} />
        <Route path='/finance' element={<Finance financeArticles={financeArticles}/>}/>
        <Route path='/fintech' />
      </Routes>
    </BrowserRouter>
  )
}

export default App
