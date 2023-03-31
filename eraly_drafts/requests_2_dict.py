
import requests
from bs4 import BeautifulSoup as bs
import datetime
import logging
import json
from fake_useragent import UserAgent
import os

url = "https://store.steampowered.com/category/rpg/?flavor=contenthub_topsellers"

ua_random = UserAgent().random
req_header = {'User-Agent': ua_random}
r = requests.get(url, headers=req_header)
data = dict(r.json())

print(data)
