from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

  model_config = SettingsConfigDict(env_nested_delimiter='__', env_file='.env')

  # Azure Settings
  azure_openai_api_key: str
  azure_openai_endpoint: str
  model_name: str
  deployment: str
  api_version: str

  # Supabase Settings
  supabase_url: str 
  supabase_key: str

settings = Settings()




