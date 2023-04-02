import grequests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import logging
from steam_age_bypass import sel_age_bypass


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
        logging.info("Starting grequests_for_game_info() process...")

        req_header = {'User-Agent': UserAgent().random}
        reqs = [grequests.get(url, headers=req_header) for url in urls]
        resp = grequests.map(reqs)

        logging.info("grequests_for_game_info() process completed successfully.")
        return resp

    except Exception as e:
        logging.error(f"Error in grequests_for_game_info(): {e}")
        logging.info("Terminating program gracefully.")
        exit()


def get_game_dicts(urls):
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

    responses = grequests_for_game_info(urls)
    dicts_list = []
    for i, response in enumerate(responses):
        game_dict = {}
        soup = BeautifulSoup(response.text, "html.parser")
        retried = False

        while True:
            try:
                name = (soup.find("div", class_="apphub_AppName")).text
            except Exception:
                if not retried:
                    game_soup = sel_age_bypass(urls[i])
                    if game_soup:
                        soup = game_soup
                        retried = True
                        continue
                    else:
                        game_dict['error_message'] = 'not available in your country or region'
                        dicts_list.append(game_dict)
                        break
                else:
                    name = 'not_available'
            game_dict['name'] = name
            break

        try:
            release = soup.find_all("div", class_="date")[0].text
        except Exception:
            release = 'not_available'
        game_dict['release_date'] = release

        try:
            developer_div = soup.find('div', {'id': 'developers_list'})
            developer = developer_div.a.text
        except Exception:
            developer = 'not_available'
        game_dict['developer'] = developer

        # try:
        #     publisher_div = soup.find('div', {'id': 'developers_list'})
        #     publisher = publisher_div.a.text
        # except Exception:
        #     release = 'not_available'
        # game_dict['developer']  = publisher

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

        dicts_list.append(game_dict)

    return dicts_list


