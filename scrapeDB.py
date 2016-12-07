from bs4 import BeautifulSoup
import requests
import re
import yaml

r = requests.get("http://www.rsdb.org/full")
data = r.text

soup = BeautifulSoup(data, 'html.parser')
f = open("slurs.yaml", "w")
for link in soup.find_all('a'):
    if "slur" in link.get('href'):
        _,_,slur = link.get('href').partition('/slur/')
        if "_" in slur:
            slur = slur.replace("_", " ")
        f.write(slur)
        f.write(': [negative]\n')
f.closed

