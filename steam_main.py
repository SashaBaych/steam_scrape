import grequests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from steam_game_classes import SteamGame, SteamGameCatalog
from tqdm import tqdm
import json
import steam_get_info as sgi
from steam_parser import parse_args
from steam_sql_tables import deploy_db
from steam_populate_database import populate_database
from steam_utils import get_logger


logger = get_logger(__file__)


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

        wait = WebDriverWait(driver, 3)

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


def get_games(url: str, num_of_games: int, games_per_loop: int, category: str):
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

        game_catalogue = SteamGameCatalog(category)
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

            infos = sgi.get_game_dicts(links)

            for j in range(games_per_loop):
                game_catalogue.add_game(rank=ratings[j], name=names[j], link=links[j], info=infos[j])
                games_retrieved += 1
                if games_retrieved == num_of_games:
                    break

        logger.info("get_games() process completed successfully.")
        print(game_catalogue)
        return game_catalogue

    except Exception as e:
        logger.error(f"Error in get_games(): {e}")
        logger.info("Terminating program gracefully.")
        exit()


def main():
    # runs a sample steam scraper
    # for a requested number of games of rpg genre
    args = parse_args()

    config = load_config(args.config_file_path)

    catalogue = get_games(config['urls'][args.category], args.num_games,
                          config['GAMES_PER_PAGE'], category=args.category)

    deploy_db(config['db_conf'], config['alch_conf']['database'])

    populate_database(catalogue, config['alch_conf'])


if __name__ == '__main__':
    main()











