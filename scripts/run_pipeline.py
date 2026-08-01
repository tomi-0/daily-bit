import logging
import feedparser
import json

LOGGER = logging.getLogger(__name__)

if __name__ == "__main__":
  # Fetch data from TechCrunch RSS Feed
  tech_crunch_url = "https://techcrunch.com/feed/"
  feed = feedparser.parse(tech_crunch_url)

  # Add feed data to new json file
  with open("tech_crunch.json", "w") as f:
    f.write(json.dumps(feed, indent=2))
  LOGGER.info("Saved feed from TechCrunch")

  
