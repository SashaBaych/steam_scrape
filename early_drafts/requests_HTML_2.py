from requests_html import HTMLSession
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
import logging
import os

# timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
# log_file_name = f"html_req_{timestamp}.log"

log_file_name = 'html_req_log'

# if os.path.exists(log_file_name):
#     os.remove(log_file_name)

logging.basicConfig(filename=log_file_name, level=logging.INFO,
                    format='%(levelname)s - %(message)s')

url = "https://store.steampowered.com/category/rpg/"

ua_random = UserAgent().random
req_header = {'User-Agent': ua_random}

session = HTMLSession()
response = session.get(url, headers=req_header)

# Render the JavaScript content
response.html.render(sleep=5)

# Create a BeautifulSoup object with the rendered content
rpgs_soup = bs(response.html.html, 'lxml')

# game = rpgs_soup.find_all('div', class_="salepreviewwidgets_StoreSaleWidgetRight_1lRFu")
# logging.info(game)

twelve_games = rpgs_soup.find('div', class_="salepreviewwidgets_SaleItemBrowserRow_y9MSd")
# logging.info(f"{game}")

print(twelve_games)

# counter = 0
# for game in twelve_games:
#     counter += 1
#     print(game.a.text)
#     print()
#     print()
#     print()
# print(counter)
# #
