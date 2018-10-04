# -*- coding: utf-8 -*-
from utils import re, xread, xsearch, s2c, namecolor

c = 'FFF9571F'

def fixLink(url):
	if not url.startswith('http'):
		url = 'http://thvl.vn' + url
	return url



def getLink(url):
	if 'http://thvl.vn/jwplayer/' not in url:
		b   = xread(url, {"Referer":"http://thvl.vn/"})
		url = xsearch('<iframe src="(.+?)"',b)
		
		if 'youtu.be' in url or 'youtube.com' in url:
			return url
		
	b    = xread(fixLink(url), {"Referer":"http://thvl.vn/"})
	link = xsearch('file: *"(.+?)"',b)
	return link


def home():
	img1   = 'http://thvl.vn/wp-content/uploads/2014/12/THVL1Online.jpg'
	img2   = 'http://thvl.vn/wp-content/uploads/2014/12/THVL2Online.jpg'
	items = [
		(namecolor("Lịch phát sóng THVL",c),"http://thvl.vn/?cat=40&kenh=THVL1","","schedule",True),
		(namecolor("Kênh THVL 1",c),"http://thvl.vn/jwplayer/?l=rtmp",img1,"live",False),
		(namecolor("Kênh THVL 2",c),"http://thvl.vn/jwplayer/?l=rtmp2",img2,"live",False),
		(namecolor("Tồng hợp",c),"http://thvl.vn/?cat=27276","","tonghop",True),
		(namecolor("Chương trình 21g",c),"http://thvl.vn/?cat=52","","21h",True),
		(namecolor("Phim mới cập nhật",c),"http://thvl.vn/?cat=8753","","phim",True)
	]
	return items


def schedule(url):
	href = "http://thvl.vn/jwplayer/?l=rtmp"
	if "THVL1" in url:
		href = "http://thvl.vn/jwplayer/?l=rtmp2"
	
	s = xsearch('(<table.+?/table>)',xread(url))
	s = [' '.join(re.sub('<.+?>',' ',i).split()) for i in re.findall('(<tr.+?/tr>)',s)]
	
	return [(i,href,"","live",False) for i in s if i]
		

def tonghop(url):
	b     = xread(url)
	items = []
	
	for s in re.findall('(<div class="post-content clearfix".+?"content clearfix">)',b,re.S):
		title = '[COLOR cyan]%s[/COLOR]'%xsearch('class="date">([^<].+?)<',s)
		title = title + ' ' + s2c(xsearch('alt="([^"].+?)"',s))
		href = xsearch('href="([^"].+?)"',s)
		img = xsearch('src="([^"].+?)"',s)
		items.append((namecolor(title,c), fixLink(href), img, 'eps', True))
	
	pageNext(b, items, 'tonghop')
		
	return items


def pageNext(b, items, query):
	s    = xsearch("(<div class='wp-pagenavi'.+?/div>)",b,1,re.S)
	href = xsearch("<span class='current'>\d+</span><a href='([^']+?)'",s).replace('#038;','')
	if href:
		next = xsearch('paged=(\d+)',href)
		last = xsearch("<a href='[^']+?(\d+)' class='last'>Cuối »</a>",s)
		
		if not last:
			last = re.findall('>(\d+)</a>',s)
			last = last[-1] if last else ''
		
		title = "Trang kế: %s/%s"%(next, last)
		items.append((namecolor(title,'lime'), fixLink(href), "", query, True))


def episode(name, url, img):
	b     = xread(url)
	
	if 'paged=' not in url and '<h3>&raquo; <a href="' not in b:
		hrefs = re.findall('<a href="(http://thvl.vn/\?cat=\d+)" title="(.+?)">',b)
		
		if not hrefs:
			return [(namecolor(name), url, img, "live", False)]

		href  = [i for i in hrefs if i[1] in name]
		if href:
			href = href[0][0]
		else:
			href = hrefs[0][0]
		
		b = xread(href)
	
	if '<h3>&raquo; <a href="' not in b:
		b = b[b.find('<div id="main-content">'):]
	else:
		b = b[b.find('<h3>&raquo; <a href="'):]
	
	s = re.findall('(<div class="video-clip-box".+?/div)',b,re.S)
	if not s:
		s = re.findall('(<div class="post-content clearfix".+?"content clearfix">)',b,re.S)
	
	items = []
	for s in s:	
		title = xsearch('class="date">([^<].+?)<',s)
		if title:
			title = '[COLOR cyan]%s[/COLOR] '%title
		title = title + s2c(xsearch('alt="([^"].+?)"',s))
		href = xsearch('href="([^"].+?)"',s)
		img = xsearch('src="([^"].+?)"',s)
		items.append((title, fixLink(href), img, 'live', False))
	
	pageNext(b, items, 'eps')
	
	return items

def chuongtrinh21h(url):
	b     = xread(url)
	items = []
	for s in re.findall('(<h3>&raquo;.+?"post-info">)',b,re.S):
		title = s2c(xsearch('>([^<]+?)</a>',s))
		href = xsearch('href="([^"]+?)"',s)
		
		if not title or not href:
			continue
		
		img = xsearch('src="([^"].+?)"',s)
		items.append((namecolor(title, c), fixLink(href), img, 'eps', True))
	
	return items



def phim(url):
	b     = xread(url)
	b = b[b.find('<div id="main-content">'):]
	
	s = re.findall('(<div class="video-clip-box".+?/div)',b,re.S)
	items = []
	for s in s:	
		title = xsearch('class="date">([^<].+?)<',s)
		if title:
			title = '[COLOR cyan]%s[/COLOR] '%title
		title = title + s2c(xsearch('alt="([^"].+?)"',s))
		href = xsearch('href="([^"].+?)"',s)
		img = xsearch('src="([^"].+?)"',s)
		items.append((namecolor(title, c), fixLink(href), img, 'eps', True))
	
	pageNext(b, items, 'phim')
	
	return items

	