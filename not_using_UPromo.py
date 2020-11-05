import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time


def bs_find(elem, tag, innertag, search_name):
    return elem.find(tag, {innertag: search_name})


URL = 'https://www.youtube.com/user/dima91gordey/videos'

driver = webdriver.Chrome()
driver.get(URL)
time.sleep(1)
html = driver.page_source
driver.close()

soup = bs(html, 'html.parser')
videos = soup.find_all('ytd-grid-video-renderer', {'class': 'style-scope ytd-grid-renderer'})

for video in videos:
    a = bs_find(video, 'a', 'id', 'video-title')
    link = 'https://www.youtube.com' + a.get('href')
    linkhtml = requests.get(link)
    linksoup = bs(linkhtml.text, 'html.parser')
    #  <meta name='description' content='
    desc = linksoup.find('meta', {'name': 'description'})
    content = str(desc.get('content'))
    keywords = ['промокод', 'скидк', 'акци'] # розыгрыш
    promo = ''
    for keyword in keywords:
        low_content = content.lower()
        keypos = low_content.find(keyword)
        if keypos != -1:
            dotpos = content.find('.', keypos)
            linkpos = low_content.rfind('http')
            if linkpos != -1 and linkpos > dotpos:
                dotpos = content.find(' ', linkpos)
            else:
                if content[dotpos:dotpos + 3] == '.ru' or content[dotpos:dotpos + 4] == '.com':
                    dotpos = content.find('.', dotpos)

            promo = content[0:dotpos + 1]
            break
    if promo != '':
        print(link, promo)
