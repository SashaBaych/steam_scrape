from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from steam_utils import logger_decorator
from tqdm import tqdm


@logger_decorator
def selenium_request_all(url: str, user_game_count: int) -> list:
    ua_random = UserAgent().random
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={ua_random}")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    last_height = driver.execute_script("return document.body.scrollHeight")

    games = []
    game_count = 0

    with tqdm(desc='Retrieving global list of top games', total=user_game_count) as pbar:
        while game_count < user_game_count:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for the content to load using WebDriverWait
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".search_result_row:nth-child({})".format(game_count + 1))))

            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            games = soup.find_all('a', class_='search_result_row')
            game_count = len(games)

            # Update the progress bar
            pbar.update(game_count - pbar.n)

    driver.quit()

    games = games[:user_game_count]

    return games


@logger_decorator
def get_basic_game_info_all(url: str, user_game_count: int) -> list:

    soup_results_set = selenium_request_all(url, user_game_count)

    basic_game_info = []

    for index, game in enumerate(soup_results_set):
        title = game.find('span', class_='title').text
        link = game['href']
        rank = index + 1
        basic_game_info.append({'rank': rank, 'title': title, 'link': link})

    return basic_game_info

#
# url = 'https://store.steampowered.com/search/?filter=topsellers'
# game_info = get_basic_game_info_all(url, 30)
#
# for game in game_info:
#     print(game)
