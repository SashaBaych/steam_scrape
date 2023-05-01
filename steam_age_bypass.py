import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By


def selenium_age_bypass(url: str):
    """
    Bypasses age restriction on Steam pages using Selenium and returns the parsed HTML of the page.

    Parameters:
        url (str): The URL of the Steam page to bypass the age restriction on.

    Returns:
        BeautifulSoup object or False: If the age restriction is successfully bypassed, it returns a BeautifulSoup
        object containing the parsed HTML of the page. If an error occurs, it returns False.
    """
    ua_random = UserAgent().random
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={ua_random}")
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1024, 2000)
    driver.get(url)

    wait = WebDriverWait(driver, 2)

    # check for country error
    try:
        country_error = ec.presence_of_element_located((By.CLASS_NAME, "error"))
        wait.until(country_error)
        driver.quit()
        return False
    except Exception:
        pass

    try:
        element_present = ec.presence_of_element_located((By.ID, 'ageYear'))
        wait.until(element_present)

        year_select = Select(driver.find_element(By.ID, 'ageYear'))
        year_select.select_by_value('1980')

        view_page_button = driver.find_element(By.ID, 'view_product_page_btn')
        view_page_button.click()

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        page_source = driver.page_source

        game_soup = BeautifulSoup(page_source, 'html.parser')

        driver.quit()
        return game_soup
    except Exception:
        driver.quit()
        return False




# url ='https://store.steampowered.com/app/1091500/Cyberpunk_2077/'
#
# selenium_age_bypass(url)

