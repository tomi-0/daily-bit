from pydantic import BaseModel
from uuid import uuid4
from enum import Enum
from datetime import date

# .model_dump() - converts to dictionary
# .model_dump_json() - converts to JSON string
# .model_validate() - create and validate instance from dictionary
# .model_validate_json() - validate and create a instance from JSON string
# .model_json_schema()- dictionary representing your model’s JSON schema

class Category(Enum):
  TECH = "TECH",
  FINANCE = "FINANCE"

class RawArticle(BaseModel):
  id = uuid4()
  title: str
  summary: str 
  source_url: str
  source_name: str
  category: Category
  published_at: date

class Keyword(BaseModel):
  id = uuid4()
  term: str
  definition: str