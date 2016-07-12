#!/usr/bin/env python2
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time, re
from bs4 import BeautifulSoup
#for retrieve image
import urllib
import socket
#for time stamp
import datetime
driver = webdriver.Firefox()
driver.implicitly_wait(3)
socket.setdefaulttimeout(20)# prevent urlretrieve from halting full timeout
#scroll done
#for i in range(1,10):
#	driver.execute_script("document.getElementByClass('ember-view infinite-scroll').scrollTo(0,document.body.scrollHeight);")
#	time.sleep(1)

#retrieve the tree and download images
count = 0 

while count < 1000:
	driver.get("https://www.twitch.tv/directory/game/League%20of%20Legends/zh")
	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "directory-list")))
	except:
		print('maybe time out, again')
	driver.implicitly_wait(10)
	#prevent empty javascript content
	channels = []
	soup = BeautifulSoup("")
	while len(channels) == 0:
		soup = BeautifulSoup(driver.page_source)
		channels = soup.select('[class~=thumb]')
	for channel in channels:
	#	print 'list channel\n' , channel
		link = channel.select('[class~=cap]')
		if len(link) == 0:
			print 'empty ember-view'
			continue	
		print link[0]['href']
		print link[0].select('img')[0]['src']
		try:		
			urllib.urlretrieve(link[0].select('img')[0]['src'], 'train/' + str(count))
		except IOError as err:
			print (err)
			count = count - 1
		count = count + 1
	print datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S')
	print 'now : ', count
	time.sleep(300)
driver.close()

