from bs4 import BeautifulSoup
import urllib, cStringIO
def findLink(url):
	if not url.startswith('http://'):
		url = 'http://' + url
	try:	
		url = urllib.urlopen(url).geturl()
	except:
		return False
	return url

def getsize(url):
	try:
		file = urllib.urlopen(url)
		return len(file.read())
	except:
		return 0

def addhttp(link, domain):
	if link is None:
		return ''
	if link.startswith('http://') or link.startswith('https://'):
		return link
	else:
		return domain+link

def retrieveImage(url):
	if not url.startswith('http://'):
		url = 'http://' + url
	try:	
		html = urllib.urlopen(url).read()
		url = urllib.urlopen(url).geturl()
	except:
		return ''
	domain = url
	soup = BeautifulSoup(html)
	imgs = soup.find_all('img')
	links = [addhttp(img.get('src'),domain) for img in imgs]
	sizes = [getsize(link) for link in links]
	max_value = max(sizes)
	max_index = sizes.index(max_value)
	return links[max_index]

print findLink('reddit.com')
print retrieveImage('news.ycombinator.com')