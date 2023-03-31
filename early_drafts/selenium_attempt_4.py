import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os

log_file_name = 'sel.log'

if os.path.exists(log_file_name):
    os.remove(log_file_name)

logging.basicConfig(filename=log_file_name, level=logging.INFO,
                    format='%(levelname)s - %(message)s')

url = "https://store.steampowered.com/category/rpg/"

ua_random = UserAgent().random
chrome_options = Options()
chrome_options.add_argument(f"user-agent={ua_random}")
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

wait = WebDriverWait(driver, 10)

# Scroll through the entire webpage
scroll_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    new_scroll_height = driver.execute_script("return document.body.scrollHeight")
    if new_scroll_height == scroll_height:
        break
    scroll_height = new_scroll_height

element_present = EC.presence_of_element_located((By.CLASS_NAME, "salepreviewwidgets_StoreSaleWidgetRight_1lRFu"))
wait.until(element_present)

page_source = driver.page_source
driver.quit()

rpgs_soup = BeautifulSoup(page_source, 'lxml')

games = rpgs_soup.find_all('div', class_="salepreviewwidgets_StoreSaleWidgetRight_1lRFu")

counter = 0
for game in games:
    counter += 1
    print(game.a.text)
    print()
    print()
    print()
print(counter)
