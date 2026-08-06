from app.config import settings
from supabase import create_client, Client

def supabase_client():
  supabase_url = settings.supabase_url
  supabase_key = settings.supabase_key

  client = create_client(
    supabase_url,
    supabase_key
  )

  return client