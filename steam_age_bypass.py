from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By


def sel_age_bypass(url: str):
    ua_random = UserAgent().random
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={ua_random}")
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1024, 2000)
    driver.get(url)

    wait = WebDriverWait(driver, 5)

    try:
        country_error = EC.presence_of_element_located((By.CLASS_NAME, "error"))
        wait.until(country_error)
        return False
    except Exception:
        pass

    element_present = EC.presence_of_element_located((By.CLASS_NAME, "agegate_birthday_desc"))
    wait.until(element_present)

    year_select = Select(driver.find_element(By.ID, 'ageYear'))
    year_select.select_by_value('1980')

    submit_button = driver.find_element(By.ID, 'view_product_page_btn')
    submit_button.click()

    page_source = driver.page_source
    driver.quit()

    game_soup = BeautifulSoup(page_source, 'lxml')

    return game_soup



# url ='https://store.steampowered.com/app/1091500/Cyberpunk_2077/'
#
# sel_age_bypass(url)

