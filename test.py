import requests
link = 'https://socialblade.com/youtube/top/country/ru/mostsubscribed'
response = requests.get(link)
print(response)
