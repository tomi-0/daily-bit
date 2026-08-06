from fastapi import FastAPI
from app.config import settings
from app.services.supabase import supabase_client

app = FastAPI()
supabase = supabase_client()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/articles")
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

@app.delete("/api/articles/{id}")
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