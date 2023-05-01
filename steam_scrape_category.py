from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from steam_utils import logger_decorator
import time
from tqdm import tqdm


@logger_decorator
def selenium_request_category(url: str, num_of_games: int):
    """
    Retrieves a list of games for a specific category using Selenium.

    Args:
        url (str): The URL of the category page to scrape.
        num_of_games (int): The number of games to retrieve.

    Returns:
        BeautifulSoup: A BeautifulSoup object containing the parsed HTML of the loaded category page.
    """
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

    games_retrieved = 0
    with tqdm(total=num_of_games, desc='Retrieving top list for given category') as pbar:
        while games_retrieved < num_of_games:
            try:
                # Keep scrolling down until the "Show more" button is found
                show_more_button = None
                while show_more_button is None:
                    try:
                        show_more_button = WebDriverWait(driver, 1).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[text()='Show more']")))
                    except TimeoutException:
                        # If the "Show more" button is not found, scroll down
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)  # Wait for the content to load

                show_more_button.click()
                time.sleep(2)  # Wait for the content to load

                # Count the number of games loaded so far
                soup = BeautifulSoup(driver.page_source, 'lxml')
                games = soup.find_all('div', class_="salepreviewwidgets_SaleItemBrowserRow_y9MSd")
                games_retrieved = len(games)

                # Update the progress bar
                pbar.update(games_retrieved - pbar.n)
            except TimeoutException:
                # If the "Show more" button is not found after scrolling, break the loop
                break

    page_source = driver.page_source
    driver.quit()

    games_soup = BeautifulSoup(page_source, 'lxml')

    return games_soup


@logger_decorator
def get_basic_game_info_category(url: str, user_game_count: int) -> list:
    """
    Retrieves basic information (rank, title, and link) for the specified number of games in a given category.

    Args:
        url (str): The URL of the category page to scrape.
        user_game_count (int): The number of games to retrieve.

    Returns:
        list: A list of dictionaries containing basic information for each game (rank, title, and link).
    """
    category_soup = selenium_request_category(url, user_game_count)

    basic_game_info = []

    outer_games_divs = category_soup.find_all('div', class_="salepreviewwidgets_SaleItemBrowserRow_y9MSd")
    inner_game_divs = [div.find('div', class_="salepreviewwidgets_StoreSaleWidgetHalfLeft_2Va3O") for div in
                       outer_games_divs]
    links = [div.a['href'] for div in inner_game_divs]
    img_tags = [div.find('img', class_='salepreviewwidgets_CapsuleImage_cODQh') for div in outer_games_divs]
    names = [tag['alt'] for tag in img_tags]

    for i in range(user_game_count):
        rank = i + 1
        title = names[i]
        link = links[i]
        basic_game_info.append({'rank': rank, 'title': title, 'link': link})

    return basic_game_info


# url = 'https://store.steampowered.com/category/action/?flavor=contenthub_topsellers'
# print(get_basic_game_info_category(url, 50))
