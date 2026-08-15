from fastapi import APIRouter
from app.services.supabase import supabase_client

financeRouter = APIRouter()

supabase = supabase_client()

@financeRouter.get("/api/finance")
async def get_articles():

  try:
    response = (
       supabase.table('finance')
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

@financeRouter.delete("/api/finance/{id}")
async def delete_articles(id: str):
  try:
    response = (
      supabase.table("finance")
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