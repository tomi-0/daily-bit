from dotenv import load_dotenv
import os
from supabase import create_client, Client

def supabase_client():
  supabase_url = os.getenv("SUPABASE_URL")
  supabase_key = os.getenv("SUPABASE_KEY")

  client = create_client(
    supabase_url,
    supabase_key
  )

  return client