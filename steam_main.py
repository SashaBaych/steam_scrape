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
import argparse
import json

# number of games displayed at once in a chart at the steam genre webpage
GAMES_PER_LOOP = 12

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


def parse_args():
    try:
        logger.info("Parsing command line arguments...")
        parser = argparse.ArgumentParser(
            description='Retrieve detailed info on the given number of top selling rpg games on steam.')
        parser.add_argument('config_file_path', type=str, help='path to configuration file')
        args = parser.parse_args()
        logger.info("Command line arguments parsed successfully.")
        return args
    except Exception as e:
        logger.error(f"Error while parsing command line arguments: {e}")
        logger.info("Terminating program gracefully.")
        exit()


def load_config(config_file_path):
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


def selenium_request(url: str) -> list:
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


def get_games(url: str, num_of_games: int):
    try:
        logger.info("Starting get_games() process...")

        rpg_catalogue = SteamGameCatalog()
        num_of_loops = num_of_games // GAMES_PER_LOOP + (1 if num_of_games % GAMES_PER_LOOP > 0 else 0)
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
                link_extension = f"&offset={12 * loop_num}"

            ratings = list(range(12 * (loop_num - 1) + 1, 12 * loop_num + 1))

            for j in range(GAMES_PER_LOOP):
                rpg_catalogue.add_game(rank=ratings[j], name=names[j], link=links[j])
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
    args = parse_args()
    if not args.config_file_path:
        print("Error: You must provide the path to the configuration file.")
        exit()

    config = load_config(args.config_file_path)

    get_games(config['url'], config['num_of_games_to_retrieve'])


if __name__ == '__main__':
    main()











