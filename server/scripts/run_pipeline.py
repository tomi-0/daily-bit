import logging
import feedparser
import json
from email.utils import parsedate_to_datetime
from app.services import (
  openai_client,
  supabase_client
)
from openai import AzureOpenAI
from pydantic import ValidationError

from app.models.articles import RawArticle, LLMOutput
from app.config import settings

LOGGER = logging.getLogger(__name__)

def build_raw_article(**kwargs) -> RawArticle | list:
  try:
      return RawArticle(**kwargs)
  except ValidationError as e:
      LOGGER.warning("Skipping invalid article: %s", e)
      return []


def fetch_tech_crunch() -> list[RawArticle]:
  # Fetch data from TechCrunch RSS Feed
  tech_crunch_url = "https://techcrunch.com/feed/"
  feed = feedparser.parse(tech_crunch_url)
  articles = []

  LOGGER.info("Fetched RSS Feed for TechCrunch")

  # Processes top 5 articles from feed
  for entry in feed.entries[:5]:
    article = build_raw_article(
      title= entry.get("title", ""),
      summary= entry.get("summary", ""),
      source_url= entry.get("link", ""),
      source_name= "TechCrunch",
      category= "TECH",
      published_at= parsedate_to_datetime(entry.published).date() if entry.get("published") else ""
    )
    articles.append(article)

  LOGGER.info("Finished processing articles into RawArticle model")

  return articles

# Fetches articles for financial news
def fetch_finance():
  pass

# Fetches articles for fintech news
def fetch_fintech():
  pass

def pick_top_articles(articles: list[RawArticle]) -> list[RawArticle]:
  pass


def process_article(client: AzureOpenAI, articles: list[RawArticle]) -> list[LLMOutput]:
  deployment = settings.deployment
  output = []

  # Collects structured LLMOutput from LLM
  LOGGER.info("Processing RawArticles")
  for article in articles:
    response = client.chat.completions.parse(
        messages=[
          {
            "role": "system",
            "content": "Summarize the article using ONLY the information provided below. "
                      "Do not add facts, figures, or details that are not present in the source text. "
                      "If the provided text is too short to summarize meaningfully, say so rather than inventing content."
                      "Add this summary to the {longer_summary} attribute",
          },
          {
              "role": "user",
              "content": f"Title: {article.title}\nSource: {article.source_name}\nText: {article.summary} Source URL:{article.source_url}",
          }
        ],
        max_tokens=4096,
        temperature=0.2,
        model=deployment,
        response_format=LLMOutput
    )

    llm_json = response.choices[0].message.content
    LOGGER.info(llm_json)

    try: 
      llm_output = LLMOutput.model_validate_json(llm_json)
    except ValidationError as e:
      LOGGER.warning("Skipping invalid article: %s", e)
      llm_output = None

    output.append(llm_output)

  LOGGER.info("Finished processing articles")

  return output

if __name__ == "__main__":
  # Initialise clients
  LOGGER.info("Initialising clients")
  openai_client = openai_client()
  supabase = supabase_client()

  # Fetch Data
  LOGGER.info("Fetching data from RSS feed")
  tech_crunch_raw_articles = fetch_tech_crunch()

  # Convert to pydantic LLMOutput models
  LOGGER.info("Processing articles into Pydantic models")
  processed_articles = process_article(openai_client, tech_crunch_raw_articles)

  # Store LLMOutput to Supabase for FE
  LOGGER.info("Saving to database")
  for a in processed_articles:
    try:
      response = (
          supabase.table("article")
            .insert(json.loads(a.model_dump_json()))
            .execute()
      )
    except Exception as exception:
      LOGGER.exception(exception)

  LOGGER.info("Finished processing articles")
