import Article from "../components/Article"

const Tech = ( {techArticles} ) => {

  return (
    <>
      {techArticles.map( article => <Article key={article.id} article={article}/>)}
    </>
  )
}

export default Tech