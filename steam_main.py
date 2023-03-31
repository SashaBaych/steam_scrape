import grequests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import datetime
from steam_game_classes import SteamGame, SteamGameCatalog
from tqdm import tqdm
import json
import steam_get_info as sgf
from steam_parser import parse_args


# number of games displayed at once in a chart at the steam genre webpage
games_per_page = 12

# logger setup
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
log_file_name = f"steam_scrape_{timestamp}.log"
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fh = logging.FileHandler(log_file_name)
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def load_config(config_file_path: str) -> dict:
    """
    Load configuration from the specified JSON file.

    Args:
        config_file_path (str): A string representing the path to the configuration file.

    Returns:
        dict: A dictionary containing the configuration data.

    Raises:
        Exception: If there's an error while loading the configuration from the file.
    """
    try:
        logger.info(f"Loading configuration from {config_file_path}...")
        with open(config_file_path, 'r') as f:
            config = json.load(f)
        logger.info("Configuration loaded successfully.")
        return config
    except Exception as e:
        logger.error(f"Error while loading configuration: {e}")
        logger.info("Terminating program gracefully.")
        exit()


def selenium_request(url: str):
    """
    Send a request to the specified URL using Selenium and return the parsed HTML content.

    Args:
        url (str): A string representing the URL to be accessed.

    Returns:
        BeautifulSoup: A BeautifulSoup object containing the parsed HTML content of the requested webpage.

    Raises:
        Exception: If there's an error while sending the request or processing the webpage content.
    """
    try:
        logger.info("Starting selenium_request() process...")

        ua_random = UserAgent().random
        chrome_options = Options()
        chrome_options.add_argument(f"user-agent={ua_random}")
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1024, 3000)
        driver.get(url)

        wait = WebDriverWait(driver, 10)

        element_present = EC.presence_of_element_located((By.CLASS_NAME, "salepreviewwidgets_SaleItemBrowserRow_y9MSd"))
        wait.until(element_present)

        page_source = driver.page_source
        driver.quit()

        rpgs_soup = BeautifulSoup(page_source, 'lxml')

        logger.info("Selenium_request() process completed successfully.")
        return rpgs_soup

    except Exception as e:
        logger.error(f"Error in selenium_request(): {e}")
        logger.info("Terminating program gracefully.")
        exit()


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


def get_game_info(urls: list) -> list:
    """
    Get the detailed information about the game from the given URLs using grequests
    and process the responses with get_dict function.

    Args:
        urls (list): A list of strings representing the URLs to be accessed.

    Returns:
        list: A list of dictionaries containing the extracted information from the URLs.

    Raises:
        Exception: If there's an error while sending the requests, processing the responses, or extracting information.
    """
    try:
        logger.info("Starting get_info() process...")

        web_sources = grequests_for_game_info(urls)
        info_dicts = []

        for source in web_sources:
            info_dicts.append(sgf.get_dict(source))

        logger.info("get_game_info() process completed successfully.")
        return info_dicts

    except Exception as e:
        logger.error(f"Error in get_info(): {e}")
        logger.info("Terminating program gracefully.")
        exit()


def get_games(url: str, num_of_games: int, games_per_loop: int):
    """
    Retrieve information for the specified number of games from the provided URL using Selenium and grequests.
    This function first uses Selenium to bypass potential filters and access the main page containing the game information.
    Then, it extracts game details by sending requests to the individual game pages using grequests.

    The retrieved game information is stored in a SteamGameCatalog object and printed at the end of the process.

    Args:
        url (str): The URL of the main page containing the list of games.
        num_of_games (int): The number of games for which to retrieve information.

    Raises:
        Exception: If there's an error while accessing the URL, processing the page source, or extracting game information.
    """
    try:
        logger.info("Starting get_games() process...")

        rpg_catalogue = SteamGameCatalog()
        num_of_loops = num_of_games // games_per_loop + (1 if num_of_games % games_per_loop > 0 else 0)
        link_extension = ''
        games_retrieved = 0

        for loop_num in tqdm(range(1, num_of_loops + 1), desc=f'Retrieving info for {num_of_games} games'):
            url = url + link_extension
            rpgs_soup = selenium_request(url)

            outer_games_divs = rpgs_soup.find_all('div', class_="salepreviewwidgets_SaleItemBrowserRow_y9MSd")

            inner_game_divs = [div.find('div', class_="salepreviewwidgets_StoreSaleWidgetHalfLeft_2Va3O") for div in
                               outer_games_divs]
            links = [div.a['href'] for div in inner_game_divs]

            img_tags = [div.find('img', class_='salepreviewwidgets_CapsuleImage_cODQh') for div in outer_games_divs]
            names = [tag['alt'] for tag in img_tags]

            if num_of_loops > 1:
                link_extension = f"&offset={games_per_loop * loop_num}"

            ratings = list(range(games_per_loop * (loop_num - 1) + 1, games_per_loop * loop_num + 1))

            info = get_game_info(links)

            for j in range(games_per_page):
                rpg_catalogue.add_game(rank=ratings[j], name=names[j], link=links[j], info=info[j])
                games_retrieved += 1
                if games_retrieved == num_of_games:
                    break

        logger.info("get_games() process completed successfully.")
        print(rpg_catalogue)

    except Exception as e:
        logger.error(f"Error in get_games(): {e}")
        logger.info("Terminating program gracefully.")
        exit()


def main():
    # runs a sample steam scraper
    # for a requested number of games of rpg genre
    args = parse_args()

    config = load_config(args.config_file_path)
    
    get_games(config['urls'][args.category], args.num_games, config['GAMES_PER_PAGE'])


if __name__ == '__main__':
    main()











