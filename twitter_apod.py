from twython import Twython
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

import urllib.request
from bs4 import BeautifulSoup
import random
from datetime import datetime, date, time
from time import sleep, strftime, time

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)


def apod():
	totalapod = abs(date.today()-date(1995,6,16)).days
	urlapod = "https://apod.nasa.gov/apod/archivepix.html"
	htmlapod = urllib.request.urlopen(urlapod).read()
	soupapod = BeautifulSoup(htmlapod, "lxml")
	num = random.randrange(3, totalapod)
	choseapod = soupapod.find_all('a')[num]
	link = choseapod.get('href')
	text = choseapod.getText()
	apodlink = "https://apod.nasa.gov/apod/%s" % link
	apodhtml = urllib.request.urlopen(apodlink).read()
	apodsoup = BeautifulSoup(apodhtml, "lxml")
	if apodsoup.find('img')!=None:
			imgsrc = apodsoup.img.get('src')
			img_link = "https://apod.nasa.gov/apod/%s" % imgsrc
			img = urllib.request.urlopen(img_link)
			message = "%s %s vai @apod" % (text, apodlink)
			response = twitter.upload_media(media=img)
			print(message)
			twitter.update_status(status=message, media_ids=[response['media_id']])
	elif apodsoup.find('iframe')!=None:
			#vidsrc = apodsoup.iframe.get('src')
			message = "%s %s vai @apod" % (text, apodlink)
			print(message)
			twitter.update_status(status=message)
	else:
			apod()

while True:
	apod()
	sleep(3600)
