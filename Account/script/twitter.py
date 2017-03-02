from bs4 import BeautifulSoup
import requests

def getfollowedby(url):

	link = 'https://www.twitter.com/%s'
	tag = link % (url)
	user=requests.get(tag)
	soup = BeautifulSoup(user.content,"html.parser")
	data=soup.find('a',{'data-nav':'followers'}).find('span',class_='ProfileNav-value')
	
	return int(data.string.replace(".",""))

def getname(url):
	return url.replace("http://","").replace("https://","").replace("www.","").replace("twitter.com/","").replace("/","")

	