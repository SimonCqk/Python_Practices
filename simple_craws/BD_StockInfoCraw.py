#!/usr/bin/python
# -*- coding:utf-8 -*-
import re

import requests
from bs4 import BeautifulSoup


def getHTMLText(url, encode="utf-8") -> str:
	try:
		r = requests.get(url)
		r.raise_for_status()
		r.encoding = encode
		return r.text
	except:
		return ""


def getStockList(lst, stockURL):
	html = getHTMLText(stockURL, "GB2312")
	soup = BeautifulSoup(html, 'html.parser')
	a = soup.find_all('a')
	for i in a:
		try:
			href = i.attrs['href']
			lst.append(re.findall(r"[s][hz]\d{6}", href)[0])
		except:
			continue


def getStockInfo(lst, stockURL, filename):
	for count, stock in enumerate(lst, start=0):
		url = stockURL + stock + ".html"
		html = getHTMLText(url)
		try:
			if html == "":
				continue
			infoDict = dict()
			soup = BeautifulSoup(html, 'html.parser')
			stockInfo = soup.find('div', attrs={'class': 'stock-bets'})

			name = stockInfo.find_all(attrs={'class': 'bets-name'})[0]
			infoDict.update({'股票名称': name.text.split()[0]})

			keyList = stockInfo.find_all('dt')
			valueList = stockInfo.find_all('dd')
			for i in range(len(keyList)):
				key = keyList[i].text
				val = valueList[i].text
				infoDict[key] = val

			with open(filename, 'a', encoding='utf-8') as f:
				f.write(str(infoDict) + '\n')
				print("\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
		except:
			print("\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
			continue


def main():
	stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
	stock_info_url = 'https://gupiao.baidu.com/stock/'
	output_file = 'BaiduStockInfo.txt'
	slist = list()
	getStockList(slist, stock_list_url)
	getStockInfo(slist, stock_info_url, output_file)


main()
