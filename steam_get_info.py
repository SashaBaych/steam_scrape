from bs4 import BeautifulSoup
import requests


def get_dict(response):
    """
    Extracts game information from a BeautifulSoup response and returns it as a dictionary.

    This function attempts to extract the name, release date, price, currency, review summary,
    and genres of a game from a BeautifulSoup response object. If the extraction is successful,
    the data is stored in a dictionary and returned. If an exception occurs during the extraction,
    an error message is added to the dictionary and the dictionary is returned.

    Args:
       response (requests.Response): A response object containing the HTML content of the game's webpage.

    Returns:
       dict: A dictionary containing the extracted game information, or an error message if extraction fails.
    """
    game_dict = {}

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        name = (soup.find("div", class_="apphub_AppName")).text


        release = soup.find_all("div", class_="date")[0].text
        price_mata_tag = soup.find("meta", {"itemprop": "price"})
        price = price_mata_tag['content']
        currency_meta_tag = soup.find("meta", {"itemprop": "priceCurrency"})
        currency = currency_meta_tag['content']
        review_summary = (soup.select_one('span[class^="game_review_summary"]')).text
        span_tag = soup.find('span', {'data-panel': True})
        genres = [a_tag.text for a_tag in span_tag.find_all('a')]

    except Exception as e:
        game_dict['error_message'] = 'Unable to retrieve info, needs further browser automation'
        return game_dict

    game_dict['name'] = name
    game_dict['release_date'] = release
    game_dict['price'] = price
    game_dict['price_currency'] = currency
    game_dict['genres'] = genres

    return game_dict


