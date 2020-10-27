import requests
from bs4 import BeautifulSoup as BS
from selenium import webdriver
import time

URL = 'https://www.youtube.com/user/dima91gordey/videos'

driver = webdriver.Chrome()
driver.get(URL)
time.sleep(1)
html = driver.page_source
driver.close()

soup = BS(html, 'html.parser')
videos = soup.find_all('ytd-grid-video-renderer', {'class': 'style-scope ytd-grid-renderer'})
for video in videos:
    a = video.find('a', {'id': 'video-title'})
    link = 'https://www.youtube.com' + a.get('href')
    linkhtml = requests.get(link)
    linksoup = BS(linkhtml.text, 'html.parser')
    #  <meta name='description' content='
    desc = linksoup.find('meta', {'name': 'description'})
    content = str(desc.get('content'))
    keywords = ['промокод', 'скидк', 'акци']
    promo = ''
    for keyword in keywords:
        keypos = content.lower().find(keyword)
        if keypos != 0:
            dotpos = content.find('.', keypos)
            promo = content[0:dotpos + 1]
            break
    if promo != '':
        print(link, promo)