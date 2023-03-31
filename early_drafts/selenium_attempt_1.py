from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os

# timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
# log_file_name = f"steam_rpg_req_{timestamp}.log"
log_file_name = 'sel.log'

if os.path.exists(log_file_name):
    os.remove(log_file_name)

logging.basicConfig(filename=log_file_name, level=logging.INFO,
                    format='%(levelname)s - %(message)s')

url = "https://store.steampowered.com/category/rpg/?flavor=contenthub_topsellers&offset=24"

# Set up a random User-Agent
ua_random = UserAgent().random
chrome_options = Options()
chrome_options.add_argument(f"user-agent={ua_random}")

# Run in headless mode (without displaying the browser window)
chrome_options.add_argument("--headless")

# Create a new instance of the browser (e.g., Chrome) and navigate to the URL
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
element_present = EC.presence_of_element_located((By.CLASS_NAME, "salepreviewwidgets_StoreSaleWidgetRight_1lRFu"))
wait.until(element_present)

# Get the page source after JavaScript has been executed
page_source = driver.page_source

# Close the browser instance
driver.quit()

# Create a BeautifulSoup object with the rendered content
rpgs_soup = BeautifulSoup(page_source, 'lxml')

games = rpgs_soup.find_all('div', class_="salepreviewwidgets_StoreSaleWidgetRight_1lRFu")
# logging.info(f"{game}")

counter = 0
for game in games:
    counter += 1
    print(game.a.text)
    print()
    print()
    print()
print(counter)
