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

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction:
		show_match(1)
	elif parserfunction == 'show_match':
		show_match(url)
	elif parserfunction == 'show_quality':
		show_quality(url)

def show_quality(url):
	request = urllib2.urlopen(url)
	html = request.read()
	request.close()
	
	p = re.compile('href="((sop|acestream):.*?)" target="_blank">(.*?)<\/a>(.*?)<br')
	
	for item in p.findall(html):
		addDir(item[3] if item[3] != '' else item[2].replace('&gt;', ''),item[0],2 if item[1] == 'sop' else 1,"",1,False)
		
def show_match(page):
	page = int(page)
	
	if page > 1:
		addDir("Trang Truoc","%d" % (page -1),401,"",1,True,parser='8bongda',parserfunction='show_match')
	
	url = 'http://www.8bongda.com/link-sopcast/'
	if page > 1:
		url = '%spage/%d/' % (url, page)
		
	request = urllib2.urlopen(url)
	html = request.read()
	request.close()
	soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
	
	matchs = soup.find('ul', 'recent')
	if matchs:
		matchs = matchs.findAll('a', 'img-shadow')
		for match in matchs:
			title = match.get('title').replace(u'Link sopcast trận ', '').replace(u'Xem trực tiếp ', '')
			addDir(title.encode('utf-8'), match.get('href').encode('utf-8'),401,"",1,True,parser='8bongda',parserfunction='show_quality')
	
	addDir("Trang Sau","%d" % (page + 1),401,"",1,True,parser='8bongda',parserfunction='show_match')