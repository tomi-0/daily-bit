import Article from "../components/Article"

const Finance = ( { financeArticles } ) => {
  return (
    <>
      {financeArticles.map( (article) => <Article key={article.id} article={article}/> )}
    </>
  )
}

export default Finance