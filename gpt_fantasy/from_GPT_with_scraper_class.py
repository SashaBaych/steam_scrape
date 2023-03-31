import os
import json
import datetime
import argparse
import logging
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from steam_game_classes_m1 import SteamGame, SteamGameCatalog


def setup_logging():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    log_file_name = f"steam_scrape_{timestamp}.log"
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_file_name)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def parse_args():
    parser = argparse.ArgumentParser(
        description='Retrieve detailed info on the given number of top selling rpg games on steam.')
    parser.add_argument('config_file_path', type=str, help='path to configuration file')
    return parser.parse_args()


def load_config(config_file_path):
    with open(config_file_path, 'r') as f:
        return json.load(f)


class SteamScraper:
    def __init__(self, config):
        self.config = config
        self.rpg_catalogue = SteamGameCatalog()
        self.GAMES_PER_LOOP = 12

    def selenium_request(self, url):
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

        return BeautifulSoup(page_source, 'lxml')

    def get_games(self):
        num_of_games = self.config['num_of_games_to_retrieve']
        num_of_loops = num_of_games // self.GAMES_PER_LOOP + (1 if num_of_games % self.GAMES_PER_LOOP > 0 else 0)
        link_extension = ''
        games_retrieved = 0
        url = self.config['url']

        for loop_num in tqdm(range(1, num_of_loops + 1), desc=f'Retrievng info for {num_of_games} games'):
            url = url + link_extension
            rpgs_soup = self.selenium_request(url)

            outer_games_divs = rpgs_soup.find_all('div', class_="salepreviewwidgets_SaleItemBrowserRow_y9MSd")
            inner_game_divs = [div.find('div', class_="salepreviewwidgets_StoreSaleWidgetHalfLeft_2Va3O") for div in outer_games_divs]
            links = [div.a['href'] for div in inner_game_divs]
            img_tags = [div.find('img', class_='salepreviewwidgets_CapsuleImage_cODQh') for div in outer_games_divs]
            names = [tag['alt'] for tag in img_tags]

            link_extension = f"&offset={12 * loop_num}"
            ratings = list(range(12 * (loop_num - 1) + 1, 12 * loop_num + 1))

            for j in range(self.GAMES_PER_LOOP):
                self.rpg_catalogue.create_game(rank=ratings[j], name=names[j], link=links[j])
                games_retrieved += 1
                if games_retrieved == num_of_games:
                    break

        def run(self):
            self.get_games()
            logger.info("Success")
            print(self.rpg_catalogue)

        def main():
            args = parse_args()
            if not args.config_file_path:
                print("Error: You must provide the path to the configuration file.")
                exit()

            config = load_config(args.config_file_path)
            logger = setup_logging()

            scraper = SteamScraper(config)
            scraper.run()

        if __name__ == '__main__':
            main()
            for j in range(self.GAMES_PER_LOOP):
                self.rpg_catalogue.create_game(rank=ratings[j], name=names[j], link=links[j])
                games_retrieved += 1
                if games_retrieved == num_of_games:
                    break

    def run(self):
        self.get_games()
        logger.info("Success")
        print(self.rpg_catalogue)


def main():
    args = parse_args()
    if not args.config_file_path:
        print("Error: You must provide the path to the configuration file.")
        exit()

    config = load_config(args.config_file_path)
    logger = setup_logging()

    scraper = SteamScraper(config)
    scraper.run()


if __name__ == '__main__':
    main()
