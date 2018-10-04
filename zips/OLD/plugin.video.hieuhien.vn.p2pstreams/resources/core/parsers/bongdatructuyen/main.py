# -*- coding: utf-8 -*-
import sys,os,urllib2,re
current_dir = os.path.dirname(os.path.realpath(__file__))
basename = os.path.basename(current_dir)
core_dir =  current_dir.replace(basename,'').replace('parsers','')
sys.path.append(core_dir)
from peertopeerutils.webutils import *
from peertopeerutils.pluginxbmc import *
from peertopeerutils.directoryhandle import *
from BeautifulSoup import BeautifulSoup
import acestream as ace
import sopcast as sop

base_url = 'http://www.bongdatructuyen.vn'

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction:
		show_group()
	elif parserfunction == 'show_match':
		show_match(url)
	elif parserfunction == 'show_link':
		show_link(url)

def send_request(url):
	request = urllib2.Request(url)
	request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0')
	request.add_header('Referer', 'http://www.bongdatructuyen.vn/')
	request = urllib2.urlopen(request)
	html = request.read()
	request.close()
	
	return html
		
		
def show_group():
	html = send_request('http://www.bongdatructuyen.vn/truc-tiep')
	
	soup = BeautifulSoup(html)
	menu = soup.find('div', id = 'left-side')
	if menu:
		menu = menu.ul.findAll('li')
		p = re.compile('[0-9]*')
		
		for item in menu:
			group = item.a
			url = '%s%s' % (base_url, group.get('href').encode('utf-8'))
			text = group.text.encode('utf-8')
			text = p.sub('', text)
			
			num_of_match = '0'
			if group.span:
				num_of_match = group.span.string.encode('utf-8')
			
			if item.parent.get('class') == 'sub-menu':
				addDir('------ %s (%s)' % (text, num_of_match),url,401,"",1,True,parser='bongdatructuyen',parserfunction='show_match')
			else:
				addDir('%s (%s)' % (text, num_of_match),url,401,"",1,True,parser='bongdatructuyen',parserfunction='show_match')
	
		
def show_link(url):
	html = send_request(url)
	
	soup = BeautifulSoup(html)
	links = soup.find('div', id = 'list-channel')
	if links:
		for li in links.findAll('li', 'chanel_sopcast'):
			link = li.find('span', 'name').a.get('href')
			addDir(link,link,2,"",1,False)
		
		
def show_match(url):
	html = send_request(url)
	soup = BeautifulSoup(html)
	games_list = soup.find('div', id = 'gamesList')
	
	for ul in games_list.findAll('ul'):
		for a in ul.findAll('a'):
			addDir('%s - %s: %s' % (ul.findPrevious('h2').string[-10:].encode('utf-8'), a.find('div', 'hour').string, a.get('title')[14:].encode('utf-8')),'%s%s' %(base_url, a.get('href').encode('utf-8')),401,"",1,True,parser='bongdatructuyen',parserfunction='show_link')
			
	pager = games_list.find('div', 'pager')
	if pager:
		a = pager.findAll('a')
		if len(a) > 0:
			a = a[len(a) - 1]
			if not a.string.isnumeric():
				addDir('Trang Sau', '%s%s' % (base_url, a.get('href').encode('utf-8')),401,"",1,True,parser='bongdatructuyen',parserfunction='show_match')