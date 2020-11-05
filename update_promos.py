import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import datetime
import time
import psycopg2


def bs_find(elem, tag, innertag, search_name):
    return elem.find(tag, {innertag: search_name})

def convert_date(date_str):
    # 1 сент. 2020 г.
    months = {
        'янв.': 1,
        'февр.': 2,
        'мар.': 3,
        'апр.': 4,
        'мая': 5,
        'июн.': 6,
        'июл.': 7,
        'авг.': 8,
        'сент.': 9,
        'окт.': 10,
        'нояб.': 11,
        'дек.': 12
    }

    date_str = date_str[0:len(date_str) - 3]

    sp1_pos = date_str.find(' ')
    sp2_pos = date_str.rfind(' ')
    d = int(date_str[0:sp1_pos])
    m = int(months[date_str[sp1_pos+1:sp2_pos]])
    y = int(date_str[sp2_pos+1:])

    return datetime.date(y, m, d)


con = psycopg2.connect(
    database='upromo_main',
    user="postgres",
    password="Zxcvbnm0+",
    host="127.0.0.1",
    port="5432"
)

cur = con.cursor()

cur.execute('SELECT LINK FROM PROMOS')
promo_links = list(cur.fetchall())


cur.execute('SELECT LINK FROM CH_LIST')

rows = cur.fetchall()
for row in rows:
    URL = row[0]

    driver = webdriver.Chrome()
    driver.get(URL)
    time.sleep(1)
    html = driver.page_source
    driver.close()
    driver.quit()

    soup = bs(html, 'html.parser')
    videos = soup.find_all('ytd-grid-video-renderer', {'class': 'style-scope ytd-grid-renderer'})

    for video in videos:
        a = bs_find(video, 'a', 'id', 'video-title')
        link = 'https://www.youtube.com' + a.get('href')
        if promo_links.count(link) != 0:
            continue
        linkhtml = requests.get(link)
        linksoup = bs(linkhtml.text, 'html.parser')
        #  <meta name='description' content='
        desc = linksoup.find('meta', {'name': 'description'})
        content = str(desc.get('content'))

        keywords = ['промокод', 'скидк', 'акци']  # розыгрыш
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

                #date
                linksoup_str = str(linksoup)
                search_str = '"dateText":{"simpleText":"'
                date_pos1 = linksoup_str.find(search_str) + len(search_str)
                date_pos2 = linksoup_str.find('"', date_pos1)
                release_date = linksoup_str[date_pos1:date_pos2]
                release_date = convert_date(str(release_date))
                break
        if promo != '':
            query = 'INSERT INTO PROMOS (LINK, RELEASE_DATE, PROMO) VALUES (%s,%s, %s)'
            cur.execute(query, (link, release_date, promo))

con.commit()
con.close()