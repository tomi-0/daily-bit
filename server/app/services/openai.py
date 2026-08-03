from dotenv import load_dotenv
from openai import AzureOpenAI
import os

def openai_client():
  load_dotenv(".env")

  azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
  azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

  client = AzureOpenAI(
    api_version="2024-12-01-preview",
    api_key=azure_openai_api_key,
    azure_endpoint=azure_openai_endpoint
  )

  return client