#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import re


def getHTMLText(url):
	try:
		r = requests.get(url, timeout=30)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return ""


def parsePage(ilt, html):
	try:
		plt = re.findall(r'data-price\=\"[\d\.]*\"', html)
		tlt = re.findall(r'title\=\".*?\"', html)
		for i in range(len(plt)):
			price = eval(plt[i].split('=')[1])
			title = eval(tlt[i].split('=')[1])
			ilt.append([price, title])
	except:
		print("")


def printGoodsList(ilt):
	tplt = "{:4}\t{:8}\t{:16}"
	print(tplt.format("Number", "Price", "Name of Good"))
	count = 0
	for g in ilt:
		count = count + 1
		print(tplt.format(count, g[0], g[1]))


def saveData(filename: str, ilt):
	file = open(filename, 'w',encoding='utf-8')
	tplt = "{:4}\t{:8}\t{:16}"
	print(tplt.format("Number", "Price", "Name of Good"), file=file)
	count = 0
	for item in ilt:
		print(tplt.format(count, item[0], item[1]),file=file)
	file.close()


def main():
	goods = 'Python'
	depth = 10
	url = 'https://search.jd.com/Search?keyword=' + goods + '&enc=utf-8'  # https://s.taobao.com/search?q=
	infoList = list()
	for i in range(depth):
		try:
			html = getHTMLText(url)
			parsePage(infoList, html)
		except:
			continue
	saveData("CrawedData_JD.txt", infoList)
	printGoodsList(infoList)


main()
