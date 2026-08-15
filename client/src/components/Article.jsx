const Article = ( { article } ) => {

  return (
    <div>
      <h1>{article.title}</h1>
      <p>{article.summary}</p>
      <a href={article.source_url}>Link to article</a>
      <p>Source: {article.source_name}</p>
      <p>Date: {article.published_at}</p>
      <p>Summary: {article.longer_summary}</p>
    </div>
  )
}

export default Article