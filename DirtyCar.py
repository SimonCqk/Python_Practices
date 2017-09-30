#!/usr/bin/python
# -*- coding:utf-8 -*-

import os

import requests

URL = 'http://asiangirls.lihulab.net/news/album'  # url of primer.

while (URL is not None):
	try:
		req = requests.get(url=URL, timeout=50)
		car_j = req.json()
	except:
		break
	for result in car_j['results']:
		path = result['title'].strip()
		if not os.path.exists(path):
			os.mkdir(path)
		print("start downloading {0}.".format(path))
		urls = result['content'].split(' ')
		for index, url in enumerate(urls):
			try:
				img = requests.get(url, timeout=50)
			except:
				continue
			if img.status_code == 200:  # judge if succeed.
				with open(path + '/' + str(index) + '.jpg', 'wb') as f:
					f.write(img.content)
		print("finish downloading {0}.".format(path))
	URL = car_j['next']

print('complete all.JUST ENJOY IT!')
