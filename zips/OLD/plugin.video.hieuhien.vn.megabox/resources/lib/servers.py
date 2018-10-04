# -*- coding: utf-8 -*-
import urllib,urllib2,urlfetch, re, os, json
from time import sleep
from setting import *
from utils import *
from urlfetch import get,post

import random
import xbmc

def resolu(s):
	s=s.replace('HDG','').replace('HD','1080').replace('SD','640').replace('large','640').replace('medium','480').replace('small','360')
	result=xsearch('(\d+)',s)
	return result if result else '240'
	
def dl(l):#Direct link
	o=make_request(l,resp='o',maxr=5);h=''
	try:s=int(o.headers.get('content-length'))
	except:s=0
	s=0 if s<10**7 else s
	if s and o.history:h=o.history[-1].headers['location']
	elif s:h=l
	return h

color={'trangtiep':'[COLOR lime]','cat':'[COLOR green]','search':'[COLOR red]','phimbo':'[COLOR tomato]','phimle':'[COLOR yellow]','imdb':'[COLOR yellow]','namphathanh':'[COLOR yellow]','theloai':'[COLOR green]','quocgia':'[COLOR blue]'}

hd={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/600.1.4 Gecko/20100101 Firefox/41.0'}		
def make_request(url,headers=hd,resp='b',maxr=0):
	try:
		if maxr==0:response=get(url,headers=headers)#,timeout=2)
		else:response=get(url,headers=headers,max_redirects=maxr)#,timeout=2)
		if resp=='o':resp=response
		else:
			if resp=='j':resp=response.json
			elif resp=='s':resp=response.status
			elif resp=='u':resp=response.text
			elif resp=='c':resp=response.cookiestring
			else:resp=response.body
			response.close()
	except:
		if resp=='j':resp=dict()
		elif resp=='s':resp=500
		else:resp=''
		if 'vaphim.com' not in url:
			link=xsearch('//(.{5,20}\.\w{2,3})',s2u(url))
			if not link:link=url
			notify(u'Lỗi kết nối tới: %s!'%xsearch('//(.{5,20}\.\w{2,3})',s2u(url)),'make_request')
		print 'Lỗi kết nối tới: %s!'%u2s(url);
	return resp#unicode:body=response.text		
		
def json_rw(file,dicts={},key=''):
	if dicts:makerequest(joinpath(datapath,file),json.dumps(dicts),'w')
	else:
		try:dicts=json.loads(makerequest(joinpath(datapath,file)))
		except:dicts={}
		if key:dicts=dicts.get(key,())
	return dicts

class serversList:
	def __init__(self):
		self.servers=[('anime47.com', '37'), ('tvhay.org', '41'), ('hdviet.com', '22'), ('fptplay.net', '07'), ('hayhaytv.vn', '23'), ('bilutv.com', '36'), ('phimmoi.net', '24'), ('hdonline.vn', '30'), ('megabox.vn', '17'), ('phim3s.net', '32'), ('phim14.net', '39'), ('kenh88.com', '26'), ('phimdata.com', '27'), ('phimsot.com', '29'), ('phim47.com', '28'), ('phimbathu.com', '43'), ('kphim.tv', '33'), ('phimnhanh.com', '35'), ('dangcaphd.com', '18'), ('phim.media', '40'), ('hdsieunhanh.com', '44'), ('imovies.vn', '48'), ('vuahd.tv', '21'), ('pubvn.tv', '19'), ('vietsubhd.com', '54'), ('mphim.net', '55')]
		try:self.ordinal=[int(i) for i in xrw('free_servers.dat').split(',')]
		except:self.ordinal=[]
		l=len(self.servers);update=False
		for i in range(l):
			if i not in self.ordinal:self.ordinal.append(i);update=True
		for i in self.ordinal:
			if i >= l:self.ordinal.remove(i);update=True
		if update:xrw('free_servers.dat',','.join(str(i) for i in self.ordinal))
		
	def mylist(self):
		return [self.servers[i] for i in self.ordinal]

	def move(self,server,step):#sl:server location, ol: ordinal location, step:up=-1,down=+1
		sl=self.servers.index([i for i in self.servers if i[0]==server][0])
		ol=self.ordinal.index([i for i in self.ordinal if i==sl][0])
		temp=self.ordinal[ol+step];self.ordinal[ol+step]=sl;self.ordinal[ol]=temp
		xrw('free_servers.dat',','.join(str(i) for i in self.ordinal))

	def moveDown(self,server):
		sl=self.servers.index([i for i in self.servers if i[0]==server][0])
		ol=self.ordinal.index([i for i in self.ordinal if i==sl][0])
		temp=self.ordinal[ol+1];self.ordinal[ol+1]=sl;self.ordinal[ol]=temp
		xrw('free_servers.dat',','.join(str(i) for i in self.ordinal))

	def search(self,url):
		try:j=json.loads(xsearch('\((\{.+?\})\)',xread(url)))
		except:j={}
#		if not j.get('results',{}):
#			notify(u'Tìm gần đúng','i-max.vn')
#			try:j=json.loads(xsearch('\((\{.+?\})\)',xread(url.replace('%22',''))))
#			except:j={}
#			if not j:return []
		
		def detail(l):
			title=l.get('titleNoFormatting','').encode('utf-8')
			href=l.get('unescapedUrl','').encode('utf-8')
			try:img=l['richSnippet']['cseImage']['src'].encode('utf-8')
			except:img=''
			return title,href,img
		l=[detail(i) for i in j.get('results',{}) if i.get('titleNoFormatting') and i.get('unescapedUrl')]
		
		cursor=j.get('cursor',{});currentPage=cursor.get('currentPageIndex',100);pages=cursor.get('pages',{})
		start=''.join(i.get('start','') for i in pages if i.get('label',0)==cursor.get('currentPageIndex')+2)
		if start:
			title='[COLOR lime]Page next: %d[/COLOR]'%(cursor.get('currentPageIndex')+2)
			l.append((title,start,''))
		return l

			
class fshare:
    
	def __init__(self):
		self.hd={'User-Agent':'Mozilla/5.0 Gecko/20100101 Firefox/44.0','x-requested-with':'XMLHttpRequest'}

	def fetch_data2(self,url,headers='',data=None):
		try:response=urlfetch(url,headers=self.hd,data=data)
		except:response= None
		return response

	def fetch_data(self,url, headers=None, data=None):
		if headers is None:
			headers = self.hd
		try:
			if data:
				response = urlfetch.post(url, headers=headers, data=data)
			else:
				response = urlfetch.get(url, headers=headers)
			return response
		except:return None
			
	def getLink(self,url,username='', password=''):
		login_url = 'https://www.fshare.vn/login'
		logout_url = 'https://www.fshare.vn/logout'
		download_url = 'https://www.fshare.vn/download/get'

		#username = myaddon.getSetting('usernamef')
		#password = myaddon.getSetting('usernamef')

		try:
			url_account = 'http://www.aku.vn/linksvip'
			headers = { 
				'Referer'			: 'http://aku.vn/linksvip',
				'User-Agent'		: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
			}
			response = self.fetch_data('http://www.aku.vn/linksvip',headers=headers,data={ 'url_download' : url })
			if response.status==404:response = self.fetch_data('http://aku.vn/linksvip',headers=headers,data={ 'url_download' : url })
			link_match=re.search("<a href=http://download(.*?)\starget=_blank", response.body)
			if link_match:
				return 'http://download' + link_match.group(1)

		except Exception as e:
			pass


		#print 'username: '+username
		#print 'password: '+password
			
		if len(username) == 0  or len(password) == 0:
			alert(u'Bạn chưa nhập tài khoản fshare'.encode("utf-8"))
			return
		

		
		response = self.fetch_data(login_url)
		if not response:
			return
		
		csrf_pattern = '\svalue="(.+?)".*name="fs_csrf"'

		csrf=re.search(csrf_pattern, response.body)
		fs_csrf = csrf.group(1)

		headers = { 
					'User-Agent' 	: 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 VietMedia/1.0',
					'Cookie'		: response.cookiestring
				}
		
		data = {
				"LoginForm[email]"		: username,
				"LoginForm[password]"	: password,
				"fs_csrf"				: fs_csrf
			}

		response = self.fetch_data(login_url, headers, data)
		headers['Cookie'] = response.cookiestring
		headers['Referer'] = url
		direct_url = ''
		attempt = 1
		MAX_ATTEMPTS = 5
		file_id = os.path.basename(url)
		if response and response.status == 302:
			notify (u'Đăng nhập fshare thành công'.encode("utf-8"))
			while attempt < MAX_ATTEMPTS:
				if attempt > 1: sleep(2)
				notify (u'Lấy link lần thứ #%s'.encode("utf-8") % attempt)
				attempt += 1

				response = self.fetch_data(url, headers, data)
				if response.status == 200:
					csrf=re.search(csrf_pattern, response.body)
					fs_csrf = csrf.group(1)
					data = {
							'fs_csrf'					: fs_csrf,
							'ajax'						: 'download-form',
							'DownloadForm[linkcode]'	: file_id
						}
					
					response=self.fetch_data(download_url, headers, data);
					
					json_data = json.loads(response.body)
					
					if json_data.get('url'):
						direct_url = json_data['url']
						break
					elif json_data.get('msg'):
						notify(json_data['msg'].encode("utf-8"))
				elif response.status == 302:
					direct_url = response.headers['location']
					break
				else:
					notify (u'Lỗi khi lấy link, mã lỗi #%s. Đang thử lại...'.encode("utf-8") % response.status) 

			response = self.fetch_data(logout_url, headers)
			if response.status == 302:
				notify (u'Đăng xuất fshare thành công'.encode("utf-8"))
		else:
			notify (u'Đăng nhập không thành công, kiểm tra lại tài khoản'.encode("utf-8"))
		if len(direct_url) > 0:
			notify (u'Đã lấy được link'.encode("utf-8"))
		else:
			notify (u'Không được link, bạn vui lòng kiểm tra lại tài khoản'.encode("utf-8"))
			
		return direct_url
	


class fptPlay:#from resources.lib.servers import fptPlay;fpt=fptPlay(c)
	def __init__(self):
		self.hd={'User_Agent':'Mozilla/5.0','X-Requested-With':'XMLHttpRequest'}
		self.hd['referer']='https://fptplay.net/fptplay/gioi-thieu'
		#self.hd['Cookie']=xrw('fptplay.cookie') if filetime('fptplay.cookie')<30 else self.login()
		
	def login(self):
		phone_fptplay=get_setting('phone_fptplay');password=get_setting('pass_fptplay')
		if not phone_fptplay:
			mess(u'Bạn đang sử dụng account Fptplay của xshare')
			phone_fptplay,password=urllib2.base64.b64decode('MDkxMzc2MTQ0NDphZGRvbnhzaGFyZQ==').split(':')
		data=urllib.urlencode({'phone':phone_fptplay,'password':password})
		cookie=urllib2.HTTPCookieProcessor();opener=urllib2.build_opener(cookie);urllib2.install_opener(opener)
		#try:b=opener.open(self.hd['referer'])
		#except:pass
		opener.addheaders=self.hd.items();url='https://fptplay.net/user/login'
		req=urllib2.Request('https://fptplay.net/user/login',data)
		try:b=urllib2.urlopen(req,timeout=30)
		except:pass
		cookie=xcookie(cookie);print cookie
		if 'laravel_id' in cookie:mess(u'Login thành công','fptplay.net');xrw('fptplay.cookie',cookie)
		else:mess(u'Login không thành công!','fptplay.net')
		return cookie	

	def detail(self,s):
		title=vnu(xsearch('title="([^"]+?)"',s))
		if not title:title=vnu(xsearch('alt="([^"]+?)"',s))
		label=' '.join(re.findall('<p[^<]*?>(.+?)</p>',s))+title
		dir=True if 'tập' in (title+label).lower() else False
		if xsearch('(\d+/\d+)',label):dir=True;title+=' [COLOR blue]%s[/COLOR]'%xsearch('(\d+/\d+)',label)
		if 'thuyếtminh' in (title+label).replace(' ','').lower():title='[COLOR blue]TM[/COLOR] '+title
		if 'phụđề' in (title+label).replace(' ','').lower():title='[COLOR green]PĐ[/COLOR] '+title
		href=xsearch('href="([^"]+?)"',s)
		if not href:href=xsearch('data-href="(.+?)"',s)
		if 'Đang diễn ra' in s:dir=None
		img=xsearch('src="([^"]+?\.jpg)',s)
		if not img:
			img=xsearch('data-original="([^"]+?\.jpg)',s)
			if not img:img=xsearch('data-original="([^"]+?\.png)',s)
		return title,href,img,dir
		
	
	def eps(self,url,page):
		data='film_id=%s&page=%d'%(xsearch('(\w{20,30})',url),page);items=[]
		b=xread('https://fptplay.net/show/episode',self.hd,data)
		for s in [i for i in re.findall('(<li.+?/li>)',b,re.S) if '"title_items"' in i]:
			title=xsearch('title="(.+?)"',s)
			epi=xsearch('<p class="title_items">.+? (\d+)',s)
			if epi:title=epi+'-'+title
			if 'phụđề' in title.replace(' ','').lower():title='[COLOR green]PĐ[/COLOR] '+title
			elif 'thuyếtminh' in title.replace(' ','').lower():title='[COLOR blue]TM[/COLOR] '+title
			#href=xsearch('(\w{20,30})',xsearch('href="(.+?)"',s))+'?'+xsearch('id="episode_(\d{1,4})"',s)
			href=xsearch('href="(.+?)"',s)
			items.append((vnu(title),href))

		if '&rsaquo;&rsaquo;' in b:items.append(('[COLOR lime]Các tập tiếp theo ...[/COLOR]',''))
		return items
	
	def liveLink(self,url):
		id=urllib2.os.path.basename(url)
		if not id:id='vtv3-hd'
		data='mobile=web&quality=3&type=newchannel&id=%s'%id
		b=xread('https://fptplay.net/show/getlinklivetv',self.hd,data)#;print self.hd
		try:link=json.loads(b).get('stream')
		except:link=''
		if link:link+='|User-Agent=xshare'
		return link
	
	def stream(self,url,epi='1'):	
		match = re.search(r'\-([\w]+)\.html', url)
		if not match:return

		id = match.group(1)
		match = re.search(r'#tap-([\d]+)$', url)
		
		if match:epi = match.group(1)
		else:epi = 1	
		
		#data=urllib.urlencode({'id':id,'type':'newchannel','quality':'3','episode':epi,'mobile':'web'})
		data='mobile=web&quality=3&type=newchannel&id=%s&episode=%s'%(id,epi)
		link=json.loads(xread('https://fptplay.net/livetv',hd,data)).get('stream')#;xbmcsetResolvedUrl(link)
		return link
	

class hayhayvn:
	def __init__(self):
		self.hd={'User-Agent':'Mozilla/5.0','Referer':'http://www.hayhaytv.vn/dieu-khoan-su-dung.html'}

	def getLink(self,url):
		tap=xsearch('-Tap-(\d+)-',url)
		if tap:tap='_'+tap
		if '/show-' in url:url='http://www.hayhaytv.vn/getsourceshow/%s'%(xsearch('-(\w+)\.html',url)+tap)
		else:url='http://www.hayhaytv.vn/getsource/%s'%(xsearch('-(\w+)\.html',url)+tap)
		b=xread(url,self.hd)
		try:items=ls([(i.get('file','').replace('\\',''),rsl(i.get('label',''))) for i in eval(b)])
		except:items=[]
		return items
		
		
	def getLink2(self,url):
		b=xread(url)
		link=xsearch('file.{,5}"(.+?)"',b);sub=''
		if link:sub=xsearch("var track.{,5}'(.+?)'",b)
		else:
			url='http://www.hayhaytv.vn/getsource/%s'%xsearch("FILM_KEY = '(.+?)'",b)
			b=xread(url,self.hd)
			try:j=eval(b)
			except:j=[]
			links=[(i.get('file').replace('\\',''),i.get('label')) for i in j]
			for href,r in ls([(i[0],rsl(i[1])) for i in links]):
				g=xget(href)
				if g:link=g.geturl();break
		return link,sub
		
class hdonline:
	def __init__(self):
		self.home='http://hdonline.vn'

	def additems(self,body,mode,page):
		items=[]
		for content in re.findall('<li>\s*<div class="tn-bxitem">(.+?)</li>',body,re.S):
			titleVn=xsearch('<p class="name-en">(.+?)</p>',content).strip()
			titleEn=xsearch('<p class="name-vi">(.+?)</p>',content).strip()
			
			href=xsearch('<a href="(.+?)"',content).strip()

			IMDb=xsearch('<p>Đánh giá:(.+?)</p>',content).strip()
			year=xsearch('<p>Năm sản xuất:(.+?) </p>',content).strip()
			
			#lay desc truc tiep thau </li> = <div class="clearfix"> o content
			#desc=xsearch('<div class="tn-contentdecs mb10">(.+?)</div>',content,1,re.DOTALL)											
			
			href='http://hdonline.vn'+href
			img=xsearch('<img src="(.+?)"',content).strip()

			if 'Cinderella Girls 2nd Season' in titleVn:titleVn='The iDOLM@STER Cinderella Girls 2nd Season'
			if 'Cinderella Girls 2nd Season' in titleEn:titleEn='The iDOLM@STER Cinderella Girls 2nd Season'
			if titleVn==titleEn:titleEn=''
			if titleEn:title = titleVn + ' (' + titleEn + ')'
			else:title = titleVn
			if year in title:title=title.replace(year,'').strip()			

			esp = xsearch('Số Tập: (.+?) </p>',content)				
			
			b = xread(href)
			desc=xsearch('itemprop="description">(.+?)</div>',b,1,re.DOTALL)
			desc=re.sub('<(.+?)>','',desc).replace('\n','')

			v_theloai=xsearch('<li>Thể loại:(.+?)</li>',b)
			theloai=', '.join(i for i in re.findall('<a href=".+?">Phim (.+?)</a>',v_theloai))
			
			v_quocgia=xsearch('<li>Quốc gia:(.+?)</li>',b)
			quocgia=', '.join(i for i in re.findall('<a href=".+?">Phim (.+?)</a>',v_quocgia))
			
			thoiluong=xsearch('<li>Thời lượng: (.+?)</li>',b).strip()
			
			v_daodien=xsearch('Đạo diễn: .*?">(.+?)</li>',b).strip()				
			daodien=', '.join(i.strip() for i in re.findall('<a href=".+?">(.+?)</a>',v_daodien))			
			dienvien=', '.join(i.strip() for i in re.findall('<a href=".+?" class="tn-pcolor1">(.+?)</a>',b))
									
			info='{'
			info+='"id":"hdonline-'+xsearch('-(\d+?)\.html',href)+'"'
			info+=',"href":[{"label":"","url":'+json.dumps(href)+',"subtitle":""}]'
			info+=',"titleVn":'+json.dumps(titleVn)		
			info+=',"titleEn":'+json.dumps(titleEn)
			info+=',"country":'+json.dumps(quocgia)
			info+=',"genre":'+json.dumps(theloai)
			info+=',"year":'+json.dumps(year)
			info+=',"writer":'+json.dumps(daodien)
			info+=',"director":'+json.dumps(dienvien)
			info+=',"duration":'+json.dumps(thoiluong)
			info+=',"thumb":'+json.dumps(img)
			info+=',"rating":'+json.dumps(IMDb)				
			info+=',"episode":'+json.dumps(esp)				
			info+=',"plot":'+json.dumps(desc)
			info+='}'
			info=info.replace('/','\/')					
			
			tag = '%s[]%s'%(fixString(daodien), fixString(dienvien))				
			items.append(('%03d'%(page),titleVn,'%s[]%s'%(fixString(quocgia), fixString(theloai)),tag,titleEn,year,info))			
		return items
		
	def eps(self,id,page):
		page=1;items=[]
		while True:		
			b=xread('http://hdonline.vn/episode/ajax?film=%s&episode=&page=%d&search='%(id,page))
			items+=[('http://hdonline.vn'+j[0],j[1]) for j in re.findall('href="(.+?)".*data-order="(.+?)"',b)]
			page+=1			
			
			pn=xsearch('<a class="active"[^<]+>\d+</a><[^<]+>(\d+)</a>',b)
			if not pn:break
			
		return items
				
class hdviet:
	def __init__(self):
		self.hd={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/600.1.4 Gecko/20100101 Firefox/41.0'}
		
	def additems(self,body,mode):
		items=[]
	
		pattern='<li class="mov-item".+?href="(.+?)".+?src="(.+?)".+?title="Phim (.+?)".+?<span(.+?) data-id="(.+?)">'	
		data=re.findall(pattern,body,re.DOTALL);listitems=list()
		for href,img,title,detail,id_film in data:
			epi=xsearch('"labelchap2">(\d{1,3})</span>',detail);title=unescape(title)
			res=xsearch('id="fillprofile" class="icon-(.+?)11">',detail)
			res='[COLOR gold]SD[/COLOR]' if 'SD' in res else '[COLOR gold]HD[/COLOR]%s'%res
			phim18=xsearch('class="children11".+?>(.+?)</label></span>',detail)
			TM=xsearch('id="fillaudio" class="icon-(.+?)">',detail)
			TM='%s[COLOR green]%s[/COLOR][COLOR red]%s[/COLOR]'%(res,TM,phim18)
			plot=xsearch('<span class="cot1">(.+?)</span>',detail)
			year=xsearch('<span class="chil-date".+?>(.*?)</label></span>',detail)
			act=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dien-vien/.+?">(.+?)</a>',detail))
			drt=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dao-dien/.+?">(.+?)</a>',detail))
			IMDb=xsearch('<span class="fl-left">.+?<span>(.+?)</span>',detail)
			upl=xsearch('<span class="fl-right">.+?<span>(.+?)</span>',detail)

			if '(' in title and ')' in title:title=title.replace('(','[B]').replace(')','[/B]')
			if IMDb:title+=color['imdb']+' IMDb: '+IMDb+'[/COLOR]'			
			
			href='hdviet.com|'+str(id_film)
			
			#if 'moicapnhat' in mode:
				#title+='[B]'+quocgia+'[/B] '
				#title+=color['theloai']+theloai+'[/COLOR]'

			
			isFolder=True
			v_mode=''
			titleVn=title
			titleEn=title
			if epi:
				title = '(' + epi + ') ' + title
				v_mode='episodes';
			else:v_mode='stream';isFolder=False
					
			items.append((title,href,'%s&query=%s'%(v_mode,titleVn+'[]'+titleEn+'[]'+str(year)),img,isFolder))					
			
		return items
		
	def getResolvedUrl(self,id_film,loop=0):#Phim le/phim chieu/ke doi dau thien ac		
		data=json_rw('hdviet.cookie')
		token = data.get('access_token')
		#token = '22bb07a59d184383a3c0cd5e3db671fc'
		#id_film=id_film.replace('_e','&ep=')
		direct_link='https://api-v2.hdviet.com/movie/play?accesstokenkey=%s&movieid=%s'%(token,id_film)		
				
		result=xread(direct_link)
		try:links=json.loads(result)["r"]
		except:links=dict()
		
		#try:print json.dumps(links,indent=2,ensure_ascii=True)
		#except:pass			
		
		link=links.get('LinkPlay')
		#if not link:return '',''
		#elif '0000000000000000000000' in link:
			#data=login_hdviet();links=getlinkhdviet(data.get('access_token'),id_film);link=links.get('LinkPlay')	
		
		if link:
			#max_resolution='_1920_' if myaddon.getSetting('hdvietresolution')=='1080' else '_1280_'
			max_resolution='_1920_'
			resolutions=['_1920_','_1885_','_1876_','_1866_','_1792_','_1280_','_1024_','_800_','_640_','_480_']
			if '_e' in id_film:link=re.sub('%s_e\d{1,3}_'%id_film.split('_')[0],'%s_'%id_film,link)
			
			r=''.join([s for s in resolutions if s in link]);response=''
			if r:
				href=link[:link.rfind(r)]+link[link.rfind(r):].replace(r,'%s')
				for i in resolutions:
					if i>max_resolution:continue
					response=make_request(href%i)
					if len(response)>0:link=href%i;break
			else:
				href=link.replace('playlist.m3u8','playlist_h.m3u8')
				response=make_request(href)
				if not response or '#EXT' not in response:
					for s in range(1,6):
						#print re.sub('http://n0\d.vn-hd.com','http://n0%d.vn-hd.com'%s,href)
						if 'http://n0%d'%s in href:continue
						elif re.search('http://n0\d.vn-hd.com',href):
							response=make_request(re.sub('http://n0\d.vn-hd.com','http://n0%d.vn-hd.com'%s,href))
						if response and  '#EXT' in response:break
				if not response:response=make_request(link)
			
			if response and '#EXT' in response:
				items=re.findall('RESOLUTION=(\d+?)x.*\s(.+m3u8)',response)
				if items:
					res=0;hr=''
					for r,h in items:
						#print r,h
						if int(r)>res:res=int(r);hr=h
					if hr and 'http://' in hr:link=hr
					else:link=os.path.dirname(link)+'/'+hr
				else:
					items=re.findall('(.+m3u8)',response)
					if items and 'http://' in items[0]:link=items[len(items)-1]#;print items[0]
					elif items:link=os.path.dirname(link)+'/'+items[0]
				
			else:link=''
		if not link:return '',''
		audio=links.get('AudioExt',list());audioindex=-1;linksub=''
		if not audio:pass
		elif len(audio)>1:
			#audio_choice=myaddon.getSetting('hdvietaudio')
			audio_choice='Hỏi khi xem-'
			if audio_choice=='Hỏi khi xem':
				title=u'[COLOR green]Chọn Audio[/COLOR]';line1= u'[COLOR yellow]Vui lòng chọn Audio[/COLOR]'
				audioindex=notify_yesno(title,line1,'',audio[0].get("Label",'0'),audio[1].get("Label",'1'))
			else:audioindex=0 if u2s(audio[0].get("Label")) in audio_choice else 1
			if 'Thuyết' not in u2s(audio[audioindex].get("Label")):linksub='yes'#bật cờ download sub
			try:link=link+'?audioindex=%d'%(int(audio[audioindex].get("Index",'0'))-1)
			except:pass
		elif u2s(audio[0].get("Label"))=='Thuyết Minh':audioindex=0
		if audioindex<0 or linksub:
			for source in ['Subtitle','SubtitleExt','SubtitleExtSe']:
				try:linksub=links[source]['VIE']['Source']
				except:linksub=''
				if linksub:break
		#print 'getResolvedUrl: %s - %s'%(link,linksub)
		return link,linksub					

class megabox:		
	def __init__(self):
		self.hd={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/600.1.4 Gecko/20100101 Firefox/41.0'}
		
	def additems(self,body,mode,page):
		items=[]
		
		for content in re.findall('<div class="item">(.+?)</div><!--',body,re.S):
			item=re.search('src="(.+?)">\s*.*<span class="features">\s*</span>\s*</a>\s*<div class="meta">\s*<h3 class="H3title">\s*<a href="(.+?)">(.+?)</a>',content)
			if item:
				#title=item.group(3)
				href=item.group(2)
				img=item.group(1)							
				
				thoiluong = xsearch('Thời lượng:</strong>(.+?)</li>',content).strip()
				IMDb = xsearch('<span class=\'rate\'>(.+?)</span>',content).strip()
				title=xsearch('<h3 class=\'H3title\'>(.+?)</h3>',content).strip()
				title=vnu(title)				
				id=xsearch('-(\d+?)\.html',href)
				if id == '15740':year='1978'
				else:year = xsearch('Năm phát hành:.*(\d{4})</li>',content).strip()
				if year in title:title=title.replace(year,'').strip()
				quocgia=xsearch('Quốc gia:</strong> (.+?)</li>',content).strip()
				daodien=xsearch('Đạo diễn:</strong> (.+?)</li>',content).strip()
				dienvien=xsearch('Diễn viên:</strong> (.+?)</li>',content).strip()					
			
				theloai=xsearch('Thể loại:</strong> (.+?)</li>',content).strip()
				theloai=theloai.replace('Ma k','K').replace('Khoa học v','V').replace('Sử thi','Lịch sử')
				
				desc=xsearch('<div class=\'des\'>(.+?)</div>',content)
				
				try:					
					titleVn = title.split(" (")[0]
					titleEn = title.split(" (")[1].replace(')','')
					#title = titleVn + ' - ' + titleEn												
				except:titleVn=title;titleEn=''

				esp = xsearch('class=.esp.><i>(.+?)</span>',content).replace('</i>','')					
				
				info='{'
				info+='"id":"megabox-'+id+'"'
				info+=',"href":[{"label":"","url":'+json.dumps(href)+',"subtitle":""}]'
				info+=',"titleVn":'+json.dumps(titleVn)		
				info+=',"titleEn":'+json.dumps(titleEn)
				info+=',"country":'+json.dumps(quocgia)
				info+=',"genre":'+json.dumps(theloai)
				info+=',"year":'+json.dumps(year)
				info+=',"writer":'+json.dumps(daodien)
				info+=',"director":'+json.dumps(dienvien)
				info+=',"duration":'+json.dumps(thoiluong)
				info+=',"thumb":'+json.dumps(img)
				info+=',"rating":'+json.dumps(IMDb)				
				info+=',"episode":'+json.dumps(esp)				
				info+=',"plot":'+json.dumps(desc)
				info+='}'
				info=info.replace('/','\/')									
				
				tag = '%s[]%s'%(fixString(daodien), fixString(dienvien))											
				items.append(('%03d'%(page),titleVn,'%s[]%s'%(fixString(quocgia), fixString(theloai)),tag,titleEn,year,info))											
		return items		

	def getLink2(self,url):	
		url='/'.join((os.path.dirname(url),urllib.quote(os.path.basename(url))))
		body=make_request(url,resp='o',maxr=5);link=xsearch("changeStreamUrl\('(.+?)'\)",body.body)
		if not link:
			link = xsearch("\'(https://www.youtube.com/watch\?v=.+?)\'",body.body)
			link = link.replace('https://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/?action=play_video&videoid=')
		else:
			hd['Cookie']=body.cookiestring;href='http://phim.megabox.vn/content/get_link_video_lab'
			maxspeedlink=make_post(href,{'Referer':url},data={"link":"%s"%link},resp='j')
			if maxspeedlink.get('link'):
				link=maxspeedlink.get('link')+'|'+urllib.urlencode(hd)
			 
		return link		
		
	def getLink(self,url):		
		url='/'.join((os.path.dirname(url),urllib.quote(os.path.basename(url))))
		content = make_request(url)
		links = re.compile('var iosUrl = "(.+?)";').findall(content)
		  
		link=''
		if len(links) > 0:
			link = links[0]
		if 'youtube' in link:
			link = url.replace('https://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/?action=play_video&videoid=')
		else:
			link = link.replace('media21.megabox.vn', '113.164.28.47')
			link = link.replace('media22.megabox.vn', '113.164.28.48')		
			link = link+'|'+urllib.urlencode(hd)
		return link
		
class phimnhanh:				
	def __init__(self):
		self.hd={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/600.1.4 Gecko/20100101 Firefox/41.0'}
		
	def additems(self,body,mode,page):
		items=[]

		hrefs=[]
		for  s in re.findall('(<li  class="serial">.+?</li>)',body,re.DOTALL):
			href=xsearch('href="(.+?)"',s)
			if href not in hrefs:hrefs.append(href)
			else:continue
			#title=xsearch('title="(.+?)"',s)
			titleVn=xsearch('<span class="title display">(.+?)</span>',s)
			titleEn=xsearch('<span class="title real">(.+?) \(',s)
			year=xsearch('<span class="title real">.+? \((.+?)\)</span>',s)
			img=xsearch('data-original="(.+?)"',s)
			label=xsearch('<span class="m-label q">(.+?)</span>',s)
			lang=xsearch('<span class="m-label lang">(.+?)</span>',s)
			IMDb=xsearch('<span class="m-label imdb"><span class="rate">(.+?)</span>',s)
			ep=xsearch('<span class="m-label ep">(.+?)</span>',s)
			if 'tập' in ep:esp=ep;thoiluong=''
			else:thoiluong=ep;esp=''
			
			if titleEn:title = titleVn + ' (' + titleEn + ')'
			else:title = titleVn
			if year in title:title=title.replace(year,'').strip()
			
			b=xread(href)		

			v_theloai=xsearch('<p>Thể loại:(.+?)</p>',b)
			theloai=', '.join(i.replace('Kinh Dị - Ma','Kinh Dị').replace('Tâm Lý - Tình Cảm','Tâm Lý, Tình Cảm') for i in re.findall('<a href=".+?" title="(.+?)">',v_theloai))						
			
			v_quocgia=xsearch('<p>Quốc gia:(.+?)</p>',b)
			quocgia=', '.join(i.replace('Mỹ - Châu Âu','Âu-Mỹ') for i in re.findall('<a href=".+?" title="(.+?)">',v_quocgia))
			
			v_daodien=xsearch('<p>Đạo diễn:(.+?)</p>',b)
			daodien=', '.join(i for i in re.findall('<a href=".+?" title="(.+?)">',v_daodien))
			v_dienvien=xsearch('<p>Diễn viên:(.+?)</p>',b)
			dienvien=', '.join(i for i in re.findall('<a href=".+?" title="(.+?)">',v_dienvien))		
												
			desc=''#xsearch('<p>(.+?)<br></p>',b,1,re.DOTALL)

			info='{'
			info+='"id":"phimnhanh-'+xsearch("javascript:download\('(.+?)'",b)+'"'
			info+=',"href":[{"label":"","url":'+json.dumps(href)+',"subtitle":""}]'
			info+=',"titleVn":'+json.dumps(titleVn)		
			info+=',"titleEn":'+json.dumps(titleEn)
			info+=',"country":'+json.dumps(quocgia)
			info+=',"genre":'+json.dumps(theloai)
			info+=',"year":'+json.dumps(year)
			info+=',"writer":'+json.dumps(daodien)
			info+=',"director":'+json.dumps(dienvien)
			info+=',"duration":'+json.dumps(thoiluong)
			info+=',"thumb":'+json.dumps(img)
			info+=',"rating":'+json.dumps(IMDb)				
			info+=',"episode":'+json.dumps(esp)				
			info+=',"plot":'+json.dumps(desc)
			info+='}'
			info=info.replace('/','\/')					
												
			tag = '%s[]%s'%(fixString(daodien), fixString(dienvien))
			items.append(('%03d'%(page),titleVn,'%s[]%s'%(fixString(quocgia), fixString(theloai)),tag,titleEn,year,info))
						
		return items	
			
		np=xsearch('<a href="([^>]+?)" rel="next">',body)
		if np:
			np=np.replace('amp;','');pn=xsearch('page=(\d+?)\Z',np)
			ps=xsearch('<a href="[^>]+?">(\d+?)</a></li> <li><a href="[^>]+?" rel="next">',body)
			t=color['trangtiep']+' Trang tiep theo...trang %s/%s[/COLOR]'%(pn,ps)
			#addir_info(t,np,ico,'',mode,page+1,query,True)
			
	def getLink(self,url):					
		
		a=make_request(url.replace('/phim/','/xem-phim/'))
		link=xsearch('playlist: "(.+?)"',a);a=make_request(link)
		for s in re.findall('(label="\d+p")',a):a=re.sub(s,'label="'+xsearch('label="(\d+)p"',s)+'"',a)
		a=a.replace('hd1080','1080').replace('hd720','720').replace('large','640').replace('medium','480')
		items=re.findall('file[^"]+"(.+?)"[^"]+"(\d+)"',a)
		items=sorted(items, key=lambda k: int(k[1]),reverse=True)		
		if items:
			link=''
			for href,label in items:
				response=make_request(href.replace('amp;',''),resp='o')
				if response and response.status==302:
					href=response.headers.get('location')
					if make_request(href,resp='s')==200:link=href;break
				if not link:xbmc.sleep(1000)
		else:
			link=xsearch('file="(.+?)"',a).replace('amp;','')
			if link and '.youtube.com' in link:
				link = link.replace('https://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/?action=play_video&videoid=')
		
		return link

class phimmoi:		
	def additems(self,body,mode,page):
		items=[]
		
		for s in re.findall('(<li class="movie-item">.+?</li>)',body,re.DOTALL):
			#title=xsearch('title="(.+?)"',s)
			titleVn=xsearch('<span class="movie-title-1">(.+?)</span>',s)
			titleEn=xsearch('<span class="movie-title-2">(.+?)</span>',s)
			if '(' in titleVn and ')' in titleVn:titleVn=titleVn.replace(' (', ' - ').replace(')', '')			
			if '(' in titleEn and ')' in titleEn:titleEn=titleEn.replace(' (', ' - ').replace(')', '')
			#duration=xsearch('>(\d{1,3}.?phút)',s)
			#label=xsearch('"ribbon">(.+?)</span>',s)
			href=xsearch('href="(.+?)"',s)
			if 'phimmoi.net' not in href:href='http://www.phimmoi.net/'+href
			img=xsearch('url=(.+?)%',s)
			
			b=xread(href)
			thoiluong = xsearch('Thời lượng:</dt><dd class="movie-dd">(.+?)</dd>',b)
			IMDb = xsearch('<dd class="movie-dd imdb">(.+?)</dd>',b)			
			quocgia=', '.join(i for i in re.findall('<a class="country" href=".+?" title=".+?">(.+?)</a>',b))
														
			theloai = ', '.join(i for i in re.findall('<a class="category" href=".+?" title="(.+?)">',b,re.S) if 'lẻ' not in i and 'bộ' not in i)#Phim bộ Hàn 
			theloai=theloai.replace('Phim Bí ẩn-Siêu nhiên','Phim Bí ẩn').replace('Phim hồi hộp-Gây cấn','Phim hồi hộp')
			theloai=theloai.replace('Phim tình cảm-Lãng mạn','Phim tình cảm').replace('Phim ','')
						
			desc=xsearch('id="film-content"><p>(.+?)\s*</p>',b,1,re.DOTALL)#<br><br>
			desc=re.sub('<(.+?)>','',desc)

			if 'Năm:</dt><dd class="movie-dd">' in b:
				year = xsearch('Năm:</dt><dd class="movie-dd">.+?(\d{1,4})</a>',b,1,re.DOTALL)
			elif 'Ngày phát hành:</dt><dd class="movie-dd">' in b:
				year = xsearch('Ngày phát hành:</dt><dd class="movie-dd">.+?/.+?/(.+?)</dd>',b,1,re.DOTALL)
			else:
				year = xsearch('Ngày ra rạp:</dt><dd class="movie-dd">.+?/.+?/(.+?)</dd>',b,1,re.DOTALL)			
			
			if '(' in titleVn: titleVn=titleVn.replace('(','- ').replace(')','')
			if '(' in titleEn: titleEn=titleEn.replace('(','- ').replace(')','')
			title = titleVn + ' (' + titleEn + ')'
			if year in title:title=title.replace(year,'').strip()
			#title=title.replace('(phần 2)','- phần 2')
						
			eps=xsearch('Tập ?(\d{,4}/\d{,4}|\?/\d{,4}|\d{,4})',s)
			if not eps:
				epi=xsearch('class="eps">Trọn bộ ?(\d{1,4}) ?tập</div>',s)
				if epi:eps='%s/%s'%(epi,epi)
			else:epi=eps.split('/')[0]
			try:epi=int(epi)
			except:epi=0
			
			daodien=', '.join(i for i in re.findall('<a class="director" href=".+?" title="(.+?)">',b))
			dienvien=', '.join(i for i in re.findall('<span class="actor-name-a">(.+?)</span>',b))
			
			if xsearch('<dd class="movie-dd status">Trailer',b,0):continue						
			
			info='{'
			info+='"id":"phimmoi-'+xsearch('-(\d+?)\/',href)+'"'
			info+=',"href":[{"label":"","url":'+json.dumps(href)+',"subtitle":""}]'
			info+=',"titleVn":'+json.dumps(titleVn)		
			info+=',"titleEn":'+json.dumps(titleEn)
			info+=',"country":'+json.dumps(quocgia)
			info+=',"genre":'+json.dumps(theloai)
			info+=',"year":'+json.dumps(year)
			info+=',"writer":'+json.dumps(daodien)
			info+=',"director":'+json.dumps(dienvien)
			info+=',"duration":'+json.dumps(thoiluong)
			info+=',"thumb":'+json.dumps(img)
			info+=',"rating":'+json.dumps(IMDb)				
			info+=',"episode":'+json.dumps(eps)				
			info+=',"plot":'+json.dumps(desc)
			info+='}'
			info=info.replace('/','\/')					
			
			tag = '%s[]%s'%(fixString(daodien), fixString(dienvien))						
			items.append(('%03d'%(page),titleVn,'%s[]%s'%(fixString(quocgia), fixString(theloai)),tag,titleEn,year,info))																
		return items
		
	def getLink(self,url):							
		url=url if '.html' in url else url+'xem-phim.html'
		body=make_request(url)
		u=xsearch('src="([^<]*?episodeinfo.+?)"',body)
		if 'http://' not in u:u='http://www.phimmoi.net/'+u
		hd['Referer']=url
		b=make_request(u,hd)
		c=xsearch("_responseJson='(.+?)'",b);href=''
		try:d=json.loads(c.replace('\\',''))
		except:d={}
		#print u,c,d
		L=[]
		if d.get('medias'):
			try:L=[(s.get('url'),resolu(str(s.get('resolution')))) for s in d.get('medias')]
			except:L=[]
			L=sorted(L, key=lambda k: int(k[1]),reverse=True)
		elif d.get('url'):L=[(d.get('url'),'1')]
		
		link=''
		for href,label in L:
			link=dl(href)
			if link:break
		return link			
		
	def getLink2(self,url):					
		body=make_request(url if '.html' in url else url+'xem-phim.html')
		
		u=xsearch('src="([^<]*?episodeinfo.+?)"',body)
		if 'http://' not in u:u='http://www.phimmoi.net/'+u
		hd['Referer']=url
		b=make_request(u,hd)
		c=xsearch("_responseJson='(.+?)'",b)
		try:d=json.loads(c.replace('\\',''))
		except:d={}
		
		href='';height=width=0
		for i in d.get('medias',[]):
			if i.get('height',0)>height:height=i.get('height');href=i.get('url')
			if i.get('width',0)>width:width=i.get('width');href=i.get('url')
		if href:
			s=make_request(href,resp='o')
			if s and s.status==302:
				href=s.headers.get('location')		
		
		return href
		
		#server quoc te khac
		content=xsearch('<div class="list-server">(.+?)</div>',body,1,re.DOTALL).replace('\n','')
		for label,subcontent in re.findall('class="server-title">(.+?)</h3>(.+?)</ul>',content):
			for href,title in re.findall('href="(.+?)">(.+?)</a>',subcontent):
				addir_info('2-%s %s'%(label,title),urlhome+href,img,'',mode,page,'pm_play')
		

class vaphim:		
	def additems(self,body,mode,page,query):
		items=[]
		pattern='<a data=.+?src="(.+?)[\?|\"].+?<h3.+?><a href="(.+?)" rel=.+?>(.+?)</a></h3>'
		for img,href,title in re.findall(pattern,body,re.DOTALL):
			title=title.replace('</br>','<br />').replace('<br/>','<br />')
			b = xread(href);v_b=re.sub('<(.+?)>','',b.replace('<br />','[]'))		
		
			year = xsearch('(\(\d{1,4}-\d{1,4}\))',title)
			if not year: year = xsearch('(\(\d{4}\))',title)
			if not year: year = xsearch('(\d{4})',title)
			if year:
				title=title.replace(year,'').replace('()','')
				year = year.replace('(','').replace(')','')			
			else:year = xsearch('Năm sản xuất:(.+?)\[\]',v_b).strip()
			try:
				titleVn=title.split(' <br /> ')[0].strip()
				titleEn=title.split(' <br /> ')[1].strip()										
			except:titleVn=title;titleEn=''						
			titleVn=vnu(titleVn);titleEn=vnu(titleEn)					
			
			thoiluong = xsearch('Thời lượng:(.+?)\[\]',v_b).strip()
			IMDb = xsearch('Đánh giá:(.+?)/10.*',v_b).strip()
			
			quocgia=xsearch('Quốc gia:(.+?)\[\]',v_b).strip()			
			daodien=xsearch('Đạo diễn:(.+?)\[\]',v_b).strip()
			dienvien=xsearch('Diễn viên:(.+?)\[\]',v_b).strip()				
			dienvien = dienvien.replace('-trong-vai:-','')
			
			theloai=xsearch('Thể loại:(.+?)\[\]',v_b).strip()
			
			tag = '%s[]%s'%(fixString(daodien), fixString(dienvien))
			
			desc=vnu(xsearch('Nội dung:</span></strong></h2>\s*<p>(.+?)</p>',b))
					
			eps = ""
																													
			tabs=re.findall('#(tabs-.+?)" >(.+?)<',b);v_href=''
			if tabs:								
				for tab,tab_label in sorted(tabs,key=lambda k: k[1],reverse=False):#lay 1080					
					content=xsearch('<div id="%s">(.+?)</div>'%tab,b,1,re.DOTALL)					
					label=subtitle=url=''
					for href, fn in re.findall('href="(.+?)".*?>(.+?)</a>',content):#<a title="" href co truong hop nay
						if ('/folder/' in href and 'phim-le' == query) or 'subscene.com' in href:continue#chua xu ly
						elif u2s(fn).lower() in ['phụ đề việt', 'sub việt']:
							subtitle=href
						elif '/file/' in href:url=href;label=tab_label											
						elif '/folder/' in href and 'phim-bo' == query:url=href;label=tab_label
					
					if url:
						v_url='{"label":'+json.dumps(label)+',"url":'+json.dumps(url)+',"subtitle":'+json.dumps(subtitle)+'}'
						if v_href:v_href+=','+v_url
						else:v_href=v_url
					
					#break #chi lay tab dau tien
			else:
				pattern='([\w|/|:|\.]+?fshare\.vn.+?|[\w|/|:|\.]+?subscene\.com.+?)[&|"|\'].+?>(.+?)</a>'
				label=subtitle=url=''
				for href, fn in re.findall(pattern,b):
					if ('/folder/' in href and 'phim-le' == query) or 'subscene.com' in href:continue#chua xu ly
					elif u2s(fn).lower() in ['phụ đề việt', 'sub việt']:
						subtitle=href
					elif '/file/' in href:url=href;label=''											
					elif '/folder/' in href and 'phim-bo' == query:url=href;label=tab_label
					
				if url:v_href='{"label":'+json.dumps(label)+',"url":'+json.dumps(url)+',"subtitle":'+json.dumps(subtitle)+'}'
					
			info='{'
			info+='"id":"vaphim-'+xsearch('#tabs-(.+?)-',b)+'"'
			info+=',"href":['+v_href+']'
			info+=',"titleVn":'+json.dumps(titleVn)		
			info+=',"titleEn":'+json.dumps(titleEn)
			info+=',"country":'+json.dumps(quocgia)
			info+=',"genre":'+json.dumps(theloai)
			info+=',"year":'+json.dumps(year)
			info+=',"writer":'+json.dumps(daodien)
			info+=',"director":'+json.dumps(dienvien)
			info+=',"duration":'+json.dumps(thoiluong)
			info+=',"thumb":'+json.dumps(img)
			info+=',"rating":'+json.dumps(IMDb)				
			info+=',"episode":'+json.dumps(eps)				
			info+=',"plot":'+json.dumps(desc)
			info+='}'
			info=info.replace('/','\/')													

			if v_href:items.append(('%03d'%(page),titleVn,'%s[]%s'%(fixString(quocgia), fixString(theloai)),tag,titleEn,year,info))
											
		return items
	
class fsharefilm:		
	def additems(self,body,mode,page,query):
		items=[]
		for href in re.findall('<div class="movie col-xs-6 col-sm-4 col-md-3 col-lg-3">\s*<a class="wrap-movie-img" href="(.+?)">',body,re.S):						
			b = xread(href)
			if 'Phim Bộ' in xsearch('<ol class="breadcrumb">(.+?)</ol>',b,1,re.DOTALL):#query=='phim-le' and 
				continue
			
			title=xsearch('"name": "(.+?)",',b)
			title=title.replace(' &#8211; ','<br />')
			
			year = xsearch('(\(\d{1,4}-\d{1,4}\))',title)
			if not year: year = xsearch('(\(\d{4}\))',title)
			if not year: year = xsearch('(\d{4})',title)
			if year:
				title=title.replace(year,'').replace('()','')
				year = year.replace('(','').replace(')','')
			else:year = xsearch('<b>Năm Phát Hành:</b></p>\s*<p class="info">(.+?)</p>',b).strip()			
			
			try:
				titleVn=title.split('<br />')[0]
				titleEn=title.split('<br />')[1]
			except:titleVn=title;titleEn=''						
			titleVn=vnu(titleVn);titleEn=vnu(titleEn)
			
			img=xsearch('"url":"(.+?.jpg)"',b)
	
			thoiluong = ''#xsearch('Thời lượng:</strong> (.+?)</li>',b).strip()
			IMDb = xsearch('<b>IMDB:</b></p>\s*<p class="info">(.+?)/10</p>',b).strip()			
			quocgia=xsearch('<b>Quốc Gia:</b></p>\s*<p class="info">(.+?)</p>',b).strip()
			daodien=xsearch('<b>Đạo Diễn:</b></p>\s*<p class="info">(.+?)</p>',b).strip()
			dienvien=xsearch('<b>Diễn Viên:</b></p>\s*<p class="info">(.+?), </p>',b).strip()
			dienvien=dienvien.replace('-trong-vai:-','')
									
			v_theloai=xsearch('<b>Thể Loại:</b></p>\s*<p class="info">(.+?)</p>',b).strip()
			theloai=', '.join(i.replace('Phim','') for i in re.findall('<a href=".+?" rel="category tag">(.+?)</a>',v_theloai))
			
			desc=xsearch('<h2>\s*<p>Cốt Truyện</h2>(.+?)</p>',b)			
			
			eps = ""
			
			tabs=re.findall('#(tabs-.+?)" >(.+?)<',b);v_href=''
			if tabs:								
				for tab,tab_label in sorted(tabs,key=lambda k: k[1],reverse=False):#lay 1080					
					content=xsearch('<div id="%s">(.+?)</div>'%tab,b,1,re.DOTALL)					
					label=subtitle=url=''
					for href, fn in re.findall('href="(.+?)".*?>(.+?)</a>',content):#<a title="" href co truong hop nay
						if ('/folder/' in href and 'phim-le' == query) or 'subscene.com' in href:continue#chua xu ly
						elif u2s(fn).lower() in ['phụ đề việt', 'sub việt']:
							subtitle=href
						elif '/file/' in href:url=href;label=tab_label											
						elif '/folder/' in href and 'phim-bo' == query:url=href;label=tab_label
					
					if url:
						v_url='{"label":'+json.dumps(label)+',"url":'+json.dumps(url)+',"subtitle":'+json.dumps(subtitle)+'}'
						if v_href:v_href+=','+v_url
						else:v_href=v_url
					
					#break #chi lay tab dau tien
			else:
				pattern='([\w|/|:|\.]+?fshare\.vn.+?|[\w|/|:|\.]+?subscene\.com.+?)[&|"|\'].+?>(.+?)</a>'
				label=subtitle=url=''
				for href, fn in re.findall(pattern,b):
					if ('/folder/' in href and 'phim-le' == query) or 'subscene.com' in href:continue#chua xu ly
					elif u2s(fn).lower() in ['phụ đề việt', 'sub việt']:
						subtitle=href
					elif '/file/' in href:url=href;label=''											
					elif '/folder/' in href and 'phim-bo' == query:url=href;label=tab_label
					
				if url:v_href='{"label":'+json.dumps(label)+',"url":'+json.dumps(url)+',"subtitle":'+json.dumps(subtitle)+'}'					
				
			info='{'
			info+='"id":"fsharefilm-'+xsearch('#tabs-(.+?)-',b)+'"'
			info+=',"href":['+v_href+']'
			info+=',"titleVn":'+json.dumps(titleVn)		
			info+=',"titleEn":'+json.dumps(titleEn)
			info+=',"country":'+json.dumps(quocgia)
			info+=',"genre":'+json.dumps(theloai)
			info+=',"year":'+json.dumps(year)
			info+=',"writer":'+json.dumps(daodien)
			info+=',"director":'+json.dumps(dienvien)
			info+=',"duration":'+json.dumps(thoiluong)
			info+=',"thumb":'+json.dumps(img)
			info+=',"rating":'+json.dumps(IMDb)				
			info+=',"episode":'+json.dumps(eps)				
			info+=',"plot":'+json.dumps(desc)
			info+='}'
			info=info.replace('/','\/')									
			
			tag = '%s[]%s'%(fixString(daodien), fixString(dienvien))
			if v_href:items.append(('%03d'%(page),titleVn,'%s[]%s'%(fixString(quocgia), fixString(theloai)),tag,titleEn,year,info))
		return items

class television:	
	def getLink(self,url):
		response = urlfetch.get(url)
		match = re.search(re.compile(r'iosUrl\s=\s\"(.*?)\"'), response.body)
		linklive = match.group(1)
		xbmc.log(linklive)
		cookie=response.cookiestring;
		headers = { 
					'User-Agent'		: 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
					'Cookie'			: cookie,
					'Referer'			: url,
					'X-Requested-With'	: 'XMLHttpRequest'					
				}
		data={'url':linklive,'type':'1'}
		response = urlfetch.post('http://hplus.com.vn/content/getlinkvideo/',data=data, headers=headers)
		if not response:
			return ''
		video_url = response.content
		xbmc.log(video_url)
		return video_url							
		
class hdvietnam:
	def __init__(self):
		self.hd={'User-Agent':'Mozilla/5.0','Referer':'http://www.hdvietnam.com/forums/'}
		self.urlhome='http://www.hdvietnam.com/'
						
	def forums(self,url):
		def cleans(s):return ' '.join(re.sub('&#\w+;|amp;','',s).split())#<[^<]+?>|\{[^\{]+\}|\[[^\[]+?\]|
		
		content=xread(url,self.hd).split('<div class="titleBar">')[-1]
		items=[]
		for s in [i for i in re.findall('(<li id="thread.+?/li>)',content,re.S) if 'class="sticky"' not in i]:
			id=xsearch('id="thread-(.+?)"',s)
			
			b=xsearch('<h3 class="title">(.+?)</h3>',s,1,re.DOTALL)
			
			href=self.urlhome+xsearch('<a href="(.+?)"',b)				
			title=xsearch('data-previewUrl=".*">(.+?)</a>',b)
			#img=xsearch('<img src="(.+?)"',content)
			items.append((id,cleans(title),href))
			
		pn=xsearch('<a href="(.+?)" class="text">Ti.+ &gt;</a>',content)
		if pn:
			pn=self.urlhome+pn
			items.append(('pageNext','[COLOR lime]Trang tiếp theo: %s[/COLOR]'%xsearch('/page-(\d+)',pn),pn))
		return items
		
	def threads(self,url):
		def cleans(s):return ' '.join(re.sub('&#\w+;|amp;|<','',s).split())#<[^<]+?>|\{[^\{]+\}|\[[^\[]+?\]|
		def srv(link):return [i for i in srvs if i in link]
		#srvs=['fshare.vn','4share.vn','tenlua.vn','subscene.com','phudeviet.org','youtube.com']
		srvs=['fshare.vn', 'docs.google.com']
		items=[]
		def getTitle(title,href,s):
			t=title
			if [i for i in srvs if i in title] or not title:
				title=xsearch('<b>Ðề: (.+?)</b>',s)
				if not title:
					title=' '.join(xsearch('<div style="text-align: center".+?>(\w[^<]+?)<',s).split())
			elif 'download' in title.strip().lower():
				title=xsearch('class="internalLink">([^<]+?)<',s[s.find(href)-500:])
				if not title:title=xsearch('<title>(.+?)</title>',content)
			if not title:title=t
			title=cleans(title)
			return title
		
		content=xread(url,self.hd)
		for s in re.findall('(<li id="post-.+?/li>)',content,re.S):
			img=xsearch('<img src="([^"]+?)" class="',s)
			if not img:img=xsearch('<img src="(.+?jpg)"',s)
			i=s
			while 'header-' in img and 'ogo' not in img:
				i=i[i.find(img)+10:]
				img=xsearch('<img src="(.+?jpg)"',i)
			
			i=re.findall('<a href="([^"]+?)" target="_blank"[^<]+?>(.+?)</a>',s)
			i= [(getTitle(title,href,s),href,img) for href,title in i if srv(href)]
			if i:items+=i
			else:items+=[('',i,img) for i in re.findall('(http[\w|:|/|\.|\?|=|&|-]+)',s.replace('amp;','')) if srv(i)]
			
		temp=[];list=[]
		for i in items:
			if i[1] not in temp:temp.append(i[1]);list.append(i)
		return list
			