import requests

URL = 'http://asiangirls.lihulab.net/news/album'

req = requests.get(url=URL, timeout=30)
req.encoding = 'utf-8'
plain_text = req.json()
f = open('test.json', mode='w')
print(plain_text, file=f, flush=True)
