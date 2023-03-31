import requests
from bs4 import BeautifulSoup as bs
import datetime
import logging
from fake_useragent import UserAgent
from requests_html import HTMLSession
import os

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
log_file_name = f"html_req_{timestamp}.log"

logging.basicConfig(filename=log_file_name, level=logging.INFO,
                    format='%(levelname)s - %(message)s')


url = "https://store.steampowered.com/category/rpg/"

top_rpgs_session = HTMLSession()
rpgs_request = top_rpgs_session.get(url)

rpgs_request.html.render(sleep=5)
games_in_tops = rpgs_request.html.xpath('//*[@id="SaleSection_13268"]/div[2]/div[2]', first=True)


logging.info(games_in_tops)


print(games_in_tops)

print(f"absolute_links {games_in_tops.absolute_links}")



