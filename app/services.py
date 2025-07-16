import re
import requests
import logging
from typing import List, Dict
from app import mock_data
from dotenv import load_dotenv
import os

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Environment configurations
DUCKDUCKGO_URL = os.getenv("DUCKDUCKGO_URL", "https://api.duckduckgo.com/")
WIKIPEDIA_SUMMARY_API = os.getenv("WIKIPEDIA_SUMMARY_API", "https://en.wikipedia.org/api/rest_v1/page/summary/")
DEFAULT_LOCATION = os.getenv("DEFAULT_LOCATION", "Indore")


# ✅ Function: extract_intent_and_location
# Purpose: Extracts "intent" (e.g., 'dentists') and "location" (e.g., 'Indore') from user query.
def extract_intent_and_location(query: str):
    query = query.lower().strip()
    location = DEFAULT_LOCATION

    if "near me" in query:
        # Assume default location if "near me"
        intent = query.replace("near me", "").strip()
        return intent, location

    # Try to extract location using regex patterns
    patterns = [
        (r"within \d+ km of ([\w, ]+)", 1),
        (r"around ([\w, ]+)", 1),
        (r"in ([\w ]+)$", 1)
    ]
    for pattern, group in patterns:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            location = match.group(group).strip()
            intent = query.replace(match.group(0), "").strip()
            return intent, location

    # Default case: no location specified
    return query, location


# ✅ Function: is_general_question
# Purpose: Checks if the user query is general (like "what is X") so that we use Wikipedia.
def is_general_question(query: str) -> bool:
    return query.lower().startswith(("what is", "who is", "define", "explain"))


# ✅ Function: get_wikipedia_summary
# Purpose: For general queries, fetch summary from Wikipedia API.
def get_wikipedia_summary(query: str) -> List[Dict]:
    try:
        topic = query.strip().rstrip("?").split(" ", 2)[-1]
        url = WIKIPEDIA_SUMMARY_API + topic.replace(" ", "_")
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            extract = data.get("extract", "")

            if extract and "may refer to:" not in extract.lower():
                sentences = extract.strip().split(". ")
                summary_points = sentences[:3]  # Limit to 3 points
                logger.info(f"Wikipedia success for topic '{topic}'")
                return [{"name": data.get("title", topic), "address": f"{i+1}. {pt.strip()}."} for i, pt in enumerate(summary_points)]
    except Exception as e:
        logger.error(f"Wikipedia error: {e}")

    return []


# ✅ Function: get_services_duckduckgo
# Purpose: For local service queries, try DuckDuckGo Instant Answer API first,
#          then fallback to mock data if no good result.
def get_services_duckduckgo(query: str) -> List[Dict]:
    if is_general_question(query):
        wiki_result = get_wikipedia_summary(query)
        if wiki_result:
            return wiki_result

    try:
        intent, location = extract_intent_and_location(query)
        search_text = f"{intent} in {location}"

        params = {
            "q": search_text,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1
        }

        response = requests.get(DUCKDUCKGO_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        results = []
        related_topics = data.get("RelatedTopics", [])

        # Parse DuckDuckGo's RelatedTopics
        for item in related_topics:
            if isinstance(item, dict) and "Text" in item and "FirstURL" in item:
                results.append({
                    "name": item["Text"].split(" - ")[0],
                    "address": item["FirstURL"]
                })

        if results:
            logger.info(f"DuckDuckGo success for query '{query}' with {len(results)} results.")
            return results
        else:
            logger.warning(f"No DuckDuckGo results for '{query}', trying mock data.")
            return get_from_mock(query)

    except Exception as e:
        logger.error(f"DuckDuckGo error: {e}")
        return get_from_mock(query)


# ✅ Function: get_from_mock
# Purpose: If both Wikipedia and DuckDuckGo fail, use local mock data as final fallback.
def get_from_mock(query: str) -> List[Dict]:
    cleaned_query = query.lower().strip().rstrip("?")

    # Try exact match
    if cleaned_query in mock_data.mock_data:
        logger.info(f"Mock data used for exact match: '{cleaned_query}'")
        return mock_data.mock_data[cleaned_query]

    # Try partial/fuzzy match
    for key in mock_data.mock_data:
        if key in cleaned_query or cleaned_query in key:
            logger.info(f"Mock data used for fuzzy match: '{cleaned_query}' ~ '{key}'")
            return mock_data.mock_data[key]

    logger.warning(f"No results found for query: '{query}'")
    return []
