import requests
from bs4 import BeautifulSoup
from tqdm import tqdm 
from alive_progress import alive_bar
import pandas as pd 
import unidecode 
import time
import datetime

date_now = datetime.date.today()


url = "https://www.oddsportal.com/matches/tennis/"+str(date_now.strftime("%Y"))+str(date_now.strftime("%m"))+str(int(date_now.strftime("%d"))+1)+"/"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
print(url)
for i in soup.find_all("tr"):
    print("\n==============================")
    print(i)