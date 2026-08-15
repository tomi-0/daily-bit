from fastapi import APIRouter
from app.services.supabase import supabase_client

techRouter = APIRouter()

supabase = supabase_client()

@techRouter.get('/api/tech')
async def get_articles():

  try:
    response = (
       supabase.table('tech')
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

@techRouter.delete("/api/tech/{id}")
async def delete_article(id: str):
  try:
    response = (
      supabase.table("tech")
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