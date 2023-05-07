import grequests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from steam_age_bypass import selenium_age_bypass
import datetime
from dateutil.parser import parse
from typing import Optional, List
from steam_utils import get_logger


logger = get_logger(__file__)


def grequests_for_game_info(urls: list) -> list:
    """
    Send asynchronous requests to the specified URLs using grequests and return the list of responses.

    Args:
        urls (list): A list of strings representing the URLs to be accessed.

    Returns:
        list: A list of Response objects containing the responses for the requested URLs.

    Raises:
        Exception: If there's an error while sending the requests or processing the responses.
    """
    try:
        logger.info("Starting grequests_for_game_info() process...")

        req_header = {'User-Agent': UserAgent().random}
        reqs = [grequests.get(url, headers=req_header) for url in urls]
        resp = grequests.map(reqs)

        logger.info("grequests_for_game_info() process completed successfully.")
        return resp

    except Exception as e:
        logger.error(f"Error in grequests_for_game_info(): {e}")
        logger.info("Terminating program gracefully.")
        exit()


def extract_release_date(soup: BeautifulSoup) -> Optional[datetime.date]:
    """
    Extracts the release date of a game from a BeautifulSoup response object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup response object containing the HTML content of the game's webpage.

    Returns:
        datetime.date object or None: The release date of the game, or None if the release date cannot be extracted.
    """
    try:
        logger.info("Extracting release date...")
        release = soup.find_all("div", class_="date")[0].text
        release_date_object = parse(release).date()
        logger.info("Release date extracted successfully.")
        return release_date_object
    except Exception as e:
        logger.error(f"Error in extract_release_date(): {e}")
        return None


def extract_developer(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the developer of a game from a BeautifulSoup response object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup response object containing the HTML content of the game's webpage.

    Returns:
        str or None: The developer of the game, or None if the developer cannot be extracted.
    """
    try:
        logger.info("Extracting developer...")
        developer_div = soup.find('div', {'id': 'developers_list'})
        developer = developer_div.a.text
        logger.info("Developer extracted successfully.")
        return developer
    except Exception as e:
        logger.error(f"Error in extract_developer(): {e}")
        return None


def extract_publisher(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the publisher of a game from a BeautifulSoup response object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup response object containing the HTML content of the game's webpage.

    Returns:
        str or None: The publisher of the game, or None if the publisher cannot be extracted.
    """
    try:
        logger.info("Extracting publisher...")
        publisher_dev_row = None
        for dev_row in soup.find_all(class_='dev_row'):
            if 'Publisher:' in dev_row.text:
                publisher_dev_row = dev_row
                break
        if publisher_dev_row:
            publisher = publisher_dev_row.a.get_text()
            logger.info("Publisher extracted successfully.")
            return publisher
    except Exception as e:
        logger.error(f"Error in extract_publisher(): {e}")
        return None


def extract_price(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the price of a game from a BeautifulSoup response object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup response object containing the HTML content of the game's webpage.

    Returns:
        str or None: The price of the game, or None if the price cannot be extracted.
    """
    try:
        logger.info("Extracting price...")
        price_meta_tag = soup.find("meta", {"itemprop": "price"})
        price = price_meta_tag['content']
        logger.info("Price extracted successfully.")
        return price
    except Exception as e:
        logger.error(f"Error in extract_price(): {e}")
        return None


def extract_currency(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the currency of a game from a BeautifulSoup response object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup response object containing the HTML content of the game's webpage.

    Returns:
        str or None: The currency of the game, or None if the currency cannot be extracted.
    """
    try:
        logger.info("Extracting currency...")
        currency_meta_tag = soup.find("meta", {"itemprop": "priceCurrency"})
        currency = currency_meta_tag['content']
        logger.info("Currency extracted successfully.")
        return currency
    except Exception as e:
        logger.error(f"Error in extract_currency(): {e}")
        return None


def extract_genres(soup: BeautifulSoup) -> Optional[List[str]]:
    """
    Extracts the genres of a game from a BeautifulSoup response object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup response object containing the HTML content of the game's webpage.

    Returns:
        list of str or None: The genres of the game, or None if the genres cannot be extracted.
    """
    try:
        logger.info("Extracting genres...")
        span_tag = soup.find('span', {'data-panel': True})
        genres = [a_tag.text for a_tag in span_tag.find_all('a')]
        logger.info("Genres extracted successfully.")
        return genres
    except Exception as e:
        logger.error(f"Error in extract_genres(): {e}")
        return None


def extract_review_summary(soup: BeautifulSoup) -> Optional[str]:
    """
    Extracts the review summary of a game from a BeautifulSoup response object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup response object containing the HTML content of the game's webpage.

    Returns:
        str or None: The review summary of the game, or None if the review summary cannot be extracted.
    """
    try:
        logger.info("Starting extract_review_summary() process...")
        review_summary = (soup.select_one('span[class^="game_review_summary"]')).text
        logger.info("extract_review_summary() process completed successfully.")
        return review_summary
    except Exception as e:
        logger.error(f"Error in extract_review_summary(): {e}")
        return None


def extract_metacritic_score(soup: BeautifulSoup) -> Optional[int]:
    """
    Extracts the Metacritic score of a game from a BeautifulSoup response object.

    Args:
        soup (BeautifulSoup): A BeautifulSoup response object containing the HTML content of the game's webpage.

    Returns:
        int or None: The Metacritic score of the game, or None if the Metacritic score cannot be extracted.
    """
    try:
        logger.info("Starting extract_metacritic_score() process...")
        score_div = soup.find('div', class_='score high')
        score = int(score_div.text.strip())
        logger.info("extract_metacritic_score() process completed successfully.")
        return score
    except Exception as e:
        logger.info(f"Error in extract_metacritic_score(): {e}")
        return None


def get_game_dicts(urls: list) -> list:
    """
    Extracts game information from a list of URLs and returns it as a list of dictionaries.

    This function attempts to extract the name, release date, developer, publisher, price, currency,
    genres, review summary, and Metacritic score of a game from a list of URLs. It sends requests to the
    provided URLs using grequests, creates a BeautifulSoup object for each response, and extracts the
    relevant information. If the extraction is successful, the data is stored in a dictionary and
    appended to a list. If an exception occurs during the extraction, an error message is added to
    the dictionary and the dictionary is appended to the list.

    Args:
       urls (list): A list of strings representing the URLs to be accessed.

    Returns:
       list: A list of dictionaries containing the extracted game information, or an error message
             if extraction fails.
    """

    logger.info("Starting get_game_dicts() process...")

    responses = grequests_for_game_info(urls)
    dicts_list = []
    for i, response in enumerate(responses):
        game_dict = {}
        soup = BeautifulSoup(response.text, "html.parser")
        retried = False
        name = None
        while True:
            try:
                name = (soup.find("div", class_="apphub_AppName")).text
            except Exception:
                if not retried:
                    logger.info("Trying selenium_age_bypass() for age-restricted content...")
                    game_soup = selenium_age_bypass(urls[i])
                    if game_soup:
                        soup = game_soup
                        retried = True
                        continue
                    else:
                        game_dict['error_message'] = 'detailed info not available'
                break
            else:
                break
        game_dict['name'] = name
        logger.info(f"Getting detailed info for game: {name}")
        game_dict['release_date'] = extract_release_date(soup)
        game_dict['developer'] = extract_developer(soup)
        game_dict['publisher'] = extract_publisher(soup)
        game_dict['price'] = extract_price(soup)
        game_dict['price_currency'] = extract_currency(soup)
        game_dict['genres'] = extract_genres(soup)
        game_dict['review_summary'] = extract_review_summary(soup)
        game_dict['metacritic_score'] = extract_metacritic_score(soup)
        game_dict['sample_date'] = datetime.date.today()

        dicts_list.append(game_dict)

    logger.info("get_game_dicts() process completed successfully.")
    return dicts_list


