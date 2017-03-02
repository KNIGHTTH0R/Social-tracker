import requests


def getfollowedby(url):

	link = 'https://www.instagram.com/%s/?__a=1'
	tag = link % (url)
	user=requests.get(tag)
	return (user.json()['user']['followed_by']['count'])

def getname(url):
	return url.replace("http://","").replace("https://","").replace("www.","").replace("instagram.com/","").replace("/","")

