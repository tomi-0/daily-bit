import logging
import feedparser
import json
from email.utils import parsedate_to_datetime
from server.app.services import (
  openai_client,
  supabase_client
)
from openai import AzureOpenAI
from pydantic import ValidationError

from server.app.models.articles import RawArticle, LLMOutput
from server.app.config import settings

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

  # Processes top 5 articles from feed
  for entry in feed.entries[:1]:
    article = build_raw_article(
      title= entry.get("title", ""),
      summary= entry.get("summary", ""),
      source_url= entry.get("link", ""),
      source_name= "TechCrunch",
      category= "TECH",
      published_at= parsedate_to_datetime(entry.published).date() if entry.get("published") else ""
    )
    articles.append(article)

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
  deployment = "gpt-4o-mini"
  output = []

  # Collects structured LLMOutput from LLM
  for article in articles:
    response = client.chat.completions.parse(
        messages=[
          {
            "role": "system",
            "content": "Summarize the article using ONLY the information provided below. "
                      "Do not add facts, figures, or details that are not present in the source text. "
                      "If the provided text is too short to summarize meaningfully, say so rather than inventing content.",
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

    output.append(response.choices[0].message.content)
    print(response.choices[0].message.content)

  return articles

if __name__ == "__main__":

  openai_client = openai_client()
  supabase = supabase_client()

  tech_crunch_raw_articles = fetch_tech_crunch()
  
  print(tech_crunch_raw_articles[0])
  processed_articles = process_article(openai_client, tech_crunch_raw_articles)

  print(f"\nSaving to database\n")
  for a in processed_articles:
    try:
      response = (
          supabase.table("article")
            .insert(json.loads(a.model_dump_json()))
            .execute()
      )
      print(response)
    except Exception as exception:
      print(exception)


  # Add feed data to new json file
  # with open("tech_crunch.json", "w") as f:
  #   f.write(json.dumps(feed, indent=2))
  # LOGGER.info("Saved feed from TechCrunch")
