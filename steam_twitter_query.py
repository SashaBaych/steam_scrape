import json
from requests_oauthlib import OAuth1
import datetime
import requests
import re
from steam_utils import logger_decorator


# set twitter API settings
CONSUMER_KEY = 'hQtk7NqtvWbBdvPqLaSthxIEq'
CONSUMER_SECRET = '2GcdFggetiV5saFMY6HYUDE5Vv4JJCN32QlQ5H9U8GQdQNYdwk'
ACCESS_TOKEN = '2280166748-3wPShETK9uATzc2VlXhL6OXxwT4lOJsHWnAkSKm'
ACCESS_TOKEN_SECRET = 'diEARpNDFkSGmRtOhtfgfK1mOidHmnUfjt2kaUA4wk6Y4'
API_URL = 'https://api.twitter.com/1.1/search/tweets.json'
REQUEST_ACCEPTED_CODE = 200
NUM_DAYS = 1


@logger_decorator
def get_oauth1_authentication():
    """
    Generates an OAuth1 object using the provided consumer key and consumer secret.

    Returns:
        OAuth1: An OAuth1 object used for authentication with the Twitter API.
    """
    oauth = OAuth1(client_key=CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET)
    return oauth


@logger_decorator
def search_tweets(query: str):
    """
    Searches for recent tweets containing the given query.

    Args:
        query (str): The search query used to find tweets.

    Returns:
        int: The number of tweets found containing the search query.
    """
    now = datetime.datetime.now()
    day_ago = now - datetime.timedelta(days=NUM_DAYS)
    now_str = now.strftime("%Y-%m-%d")
    day_ago_str = day_ago.strftime("%Y-%m-%d")

    params = {
        "q": query,
        "count": 100,
        "result_type": "recent",
        "until": now_str,
        "since": day_ago_str
    }

    total_mentions = 0
    max_id = None

    while True:
        if max_id is not None:
            params["max_id"] = max_id - 1

        response = requests.get(API_URL, params=params, auth=get_oauth1_authentication())

        if response.status_code != 200:
            print("Failed to fetch tweets: %s" % response.text)
            break

        data_dict = json.loads(response.content)

        for status in data_dict["statuses"]:
            if ''.join(query).lower() in ''.join(status["text"]).lower():
                total_mentions += 1

        if "next_results" not in data_dict["search_metadata"]:
            break

        next_results = data_dict["search_metadata"]["next_results"]
        max_id = int(re.search(r"max_id=(\d+)", next_results).group(1))

    return total_mentions


def clean_string(text: str) -> str:
    """
    Cleans the input text by removing special Unicode characters.

    Args:
        text (str): The input text to be cleaned.

    Returns:
        str: The cleaned text.
    """
    text = re.sub(r'[\u00AE\u2122\u00A9\u00B2\u00B3\u00B9\u2070-\u2079\u2080-\u2089\u207A-\u207F]', '', text)
    return text


def get_mentions_count(games):
    """
    Adds the mentions count and query date to the provided dictionary of games.

    Args:
        games (dict): A dictionary containing game names and their corresponding game_id and rank.

    Returns:
        dict: The enriched dictionary containing the game names, game_id, rank, mentions count, and query date.
    """
    query_time = datetime.datetime.now().strftime('%Y-%m-%d')

    for game_name, game_data in games.items():
        cleaned_game_name = clean_string(game_name)
        game_data["mentions_count"] = search_tweets(cleaned_game_name)
        game_data["query_date"] = query_time

    return games


