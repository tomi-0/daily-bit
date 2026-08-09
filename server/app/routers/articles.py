from fastapi import APIRouter
from app.services.supabase import supabase_client

articlesRouter = APIRouter()

supabase = supabase_client()

@articlesRouter.get('/api/articles')
async def get_articles():

  try:
    response = (
       supabase.table('article')
       .select("*")
       .execute()
    )

    if not response:
      raise Exception("Couldn't find articles to fetch")
    
    return response.data
  except Exception as e:
    return {
      "error": f"Couldn't fetch articles from database: {e}"
    }

@articlesRouter.delete("/api/articles/{id}")
async def delete_articles(id: str):
  try:
    response = (
      supabase.table("article")
      .delete()
      .eq("id", id)
      .execute()
    )

    if not response:
      raise Exception("Couldn't find article to delete")

    return response.data
    
  except Exception as e:
    return {
      "error": f"Couldn't delete from database: {e}"
    }