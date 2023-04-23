"""
Добавляет каналы в список из socialblade.com

"""

from bs4 import BeautifulSoup as BS
from selenium import webdriver
import time
import re
import psycopg2
import datetime
from webdriver_manager.chrome import ChromeDriverManager

con = psycopg2.connect(
    database='upromo_main',
    user="postgres",
    password="Zxcvbnm0+",
    host="127.0.0.1",
    port="5432"
)
cur = con.cursor()

URL = 'https://socialblade.com/youtube/top/country/ru/mostsubscribed'

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(URL)
time.sleep(1)
html = driver.page_source
driver.close()

soup = BS(html, 'html.parser')
channels = soup.find_all('a', {'href': re.compile('/youtube/channel/')})

for ch in channels:
    ch_str = str(ch)[26:]
    ch_str = ch_str[0:ch_str.find('>')-1]
    ch_link = 'https://www.youtube.com/channel/' + ch_str + '/videos'

    query = 'INSERT INTO CH_LIST (LINK,UPDATE_DATE) VALUES (%s,%s)'
    cur.execute(query, (ch_link, datetime.date.today()))

con.commit()
con.close()

