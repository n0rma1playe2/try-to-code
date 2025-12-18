import bs4
import requests
import re
from bs4 import BeautifulSoup

url="http://www.baidu.com"
r = requests.get(url)
soup =(bs4.BeautifulSoup(r.text,"lxml"))
print(soup.prettify())
