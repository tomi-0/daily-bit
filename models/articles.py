from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from enum import Enum
from datetime import date

# .model_dump() - converts to dictionary
# .model_dump_json() - converts to JSON string
# .model_validate() - create and validate instance from dictionary
# .model_validate_json() - validate and create a instance from JSON string
# .model_json_schema()- dictionary representing your model’s JSON schema

class Category(Enum):
  TECH= "TECH" 
  FINANCE= "FINANCE"
  FINTECH= "FINTECH"

class RawArticle(BaseModel):
  # id: UUID = Field(default_factory=uuid4) # callS function fresh, once per instance
  title: str
  summary: str 
  source_url: str
  source_name: str
  category: Category
  published_at: date

class Keyword(BaseModel):
  id: UUID = Field(default_factory=uuid4)
  term: str
  definition: str

class LLMOutput(RawArticle):
  longer_summary: str
  keywords: list[str]

class Article(RawArticle):
  pass