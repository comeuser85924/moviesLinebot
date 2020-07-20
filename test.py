import requests
from bs4 import BeautifulSoup
import json
 
insta_url = 'https://www.instagram.com/p/BUlPxCIAgPn/?taken-by=thekellyyang'
 
res = requests.get(insta_url)
 
soup = BeautifulSoup(res.text, "lxml")
json_part = soup.find_all("script", type="text/javascript")[1].string
print(json_part)
