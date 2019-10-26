from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen
from collections import Counter
import re
import csv
from test_selenium import Interactive_Website
import time

#User defination
MAX_TIMES = 40
URL_Link = "https://vietlott.vn/vi/trung-thuong/ket-qua-trung-thuong/winning-number-655"

COUNTER = 0
Line_Merge = 7
Str_Merge = ""
ARAWDATA = []
BRAWDATA = []
OFFICIALDATA = {}
iw = Interactive_Website()

# Using Selenium to direction for beautiful soup 4
iw.open_url(URL_Link)

while COUNTER < MAX_TIMES:
	iw.Wait_page_load("id", "divResultContent", 10)
	# Using to get data Soup
	# soup = urlopen(iw.driver.page_source)
	# RAW = soup.read()
	# soup.close()
	PARSED = Soup(iw.driver.page_source, 'html.parser')
	
	# Get date to ARAW Data
	for line in PARSED.findAll('div',{'id':'divResultContent'}):
		pRAW = re.findall("<td>([0-9]{2}.*?)<", str(line))
		for pline in pRAW:
			ARAWDATA.append(pline)

	# Get result of website
	for line in PARSED.findAll('div',{'id':'divResultContent'}):
		pRAW = re.findall("<span.*?([0-9]{2})<", str(line))
		for pline in pRAW:
			Line_Merge = Line_Merge - 1
			if Line_Merge==7:
				Str_Merge = str(pline)
			else:
				Str_Merge = Str_Merge + " " + str(pline)
			if Line_Merge == 0:
				Line_Merge = 7
				BRAWDATA.append(Str_Merge)
				Str_Merge = ""

	COUNTER_CSV = 0
	# Collect data to file csv
	for date in ARAWDATA:
		OFFICIALDATA[date] = BRAWDATA[COUNTER_CSV]
		COUNTER_CSV += 1

	#Using change page result
	iw.Wait_page_load("xpath", "/html/body/div/div[5]/div/div/div[2]/div/div[2]/div/div/ul/li[7]/a", 10)
	iw.Wait_page_load("xpath_click", "/html/body/div/div[5]/div/div/div[2]/div/div[2]/div/div/ul/li[7]/a", 10)
	lenOfPage = iw.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
	match=False
	while(match==False):
		lastCount = lenOfPage
		time.sleep(1)
		lenOfPage = iw.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
		if lastCount==lenOfPage:
			match=True
	# Execution Jquery to changed next page
	cmd = "href = document.querySelector(\"a[href='javascript:NextPage({0});']\").href; \
			window.location.href = href;".format(COUNTER+1)
	iw.driver.execute_script(cmd)
	time.sleep(2)
	print("Debug: {}".format(COUNTER))
	COUNTER += 1

with open('lotto.csv', 'w') as data:
	file = csv.writer(data)
	file.writerows(OFFICIALDATA.items())

def frequence(list):
	global zc
	BUFFED = []
	# Get all element in list
	for line in list:
		buffer = line.split()
		# Seperate number data by space
		for bbuffer in buffer:
			BUFFED.append(bbuffer)
	# To count sequence number in data
	STORED = Counter(BUFFED)
	zc = len(STORED) # Store len of BUFFED

	# Writesequence to file csv
	with open('occurrence.csv', 'w') as data:
		file = csv.writer(data)
		file.writerows(STORED.items())

def solution():
	with open('occurrence.csv', 'r') as data:
		fileReader = csv.reader(data)
		for row in fileReader:
			NUMBERS.append(row[0])
			TIMES.append(row[1])
			a = str((int(row[1]) / len(BRAWDATA)))
			CHANCE.append(a[2:4])

REPORT = {
	'Number':NUMBERS,
	'Times': TIMES,
	'Chance': CHANCE,
}

frequence(BRAWDATA)
solution()

for key,val in REPORT:
	print("{0}: {1}".format(key, val))