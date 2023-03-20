from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os
from steam_game_classes import SteamGame, SteamGameCatalog
from tqdm import tqdm


# log_file_name = 'sel.log'
#
# if os.path.exists(log_file_name):
#     os.remove(log_file_name)
#
# logging.basicConfig(filename=log_file_name, level=logging.INFO,
#                     format='%(levelname)s - %(message)s')


GAMES_PER_LOOP = 12

num_of_games_to_retrieve = 50


rpg_catalogue = SteamGameCatalog()


url = f"https://store.steampowered.com/category/rpg/?flavor=contenthub_topsellers"


def selenium_request(url: str) -> list:
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

    return rpgs_soup


def get_games(url: str, num_of_games: int):
    num_of_loops = num_of_games // GAMES_PER_LOOP + (1 if num_of_games_to_retrieve % GAMES_PER_LOOP > 0 else 0)
    link_extension = ''
    games_retrieved = 0
    for loop_num in tqdm(range(1, num_of_loops + 1), desc=f'Retrievng info for {num_of_games} games'):
        url = url + link_extension
        rpgs_soup = selenium_request(url)

        outer_games_divs = rpgs_soup.find_all('div', class_="salepreviewwidgets_SaleItemBrowserRow_y9MSd")

        inner_game_divs = [div.find('div', class_="salepreviewwidgets_StoreSaleWidgetHalfLeft_2Va3O") for div in outer_games_divs]
        links = [div.a['href'] for div in inner_game_divs]

        img_tags = [div.find('img', class_='salepreviewwidgets_CapsuleImage_cODQh') for div in outer_games_divs]
        names = [tag['alt'] for tag in img_tags]

        link_extension = f"&offset={12 * loop_num}"

        ratings = list(range(12 * (loop_num - 1) + 1, 12 * loop_num + 1))

        for j in range(GAMES_PER_LOOP):
            rpg_catalogue.create_game(rank=ratings[j], name=names[j], link=links[j])
            games_retrieved += 1
            if games_retrieved == num_of_games:
                break

    print(rpg_catalogue)


get_games(url, num_of_games_to_retrieve)









