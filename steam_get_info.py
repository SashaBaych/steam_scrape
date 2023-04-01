from bs4 import BeautifulSoup


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
    except Exception:
        name = 'not_available'
    game_dict['name'] = name

    try:
        release = soup.find_all("div", class_="date")[0].text
    except Exception:
        release = 'not_available'
    game_dict['release_date'] = release

    try:
        price_meta_tag = soup.find("meta", {"itemprop": "price"})
        price = price_meta_tag['content']
        currency_meta_tag = soup.find("meta", {"itemprop": "priceCurrency"})
        currency = currency_meta_tag['content']
    except Exception:
        price = 'not_available'
        currency = 'not_available'
    game_dict['price'] = price
    game_dict['price_currency'] = currency

    try:
        span_tag = soup.find('span', {'data-panel': True})
        genres = [a_tag.text for a_tag in span_tag.find_all('a')]
    except Exception:
        genres = 'not_available'
    game_dict['genres'] = genres

    try:
        review_summary = (soup.select_one('span[class^="game_review_summary"]')).text
    except Exception:
        review_summary = 'not_available'
    game_dict['review_summary'] = review_summary

    try:
        score_div = soup.find('div', class_='score high')
        score = int(score_div.text.strip())
    except Exception:
        score = 'not_available'
    game_dict['metacritic_score'] = score

    return game_dict

    return game_dict


