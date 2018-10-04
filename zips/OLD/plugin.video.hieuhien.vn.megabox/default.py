__author__ = 'phuoclv'
#coding=utf-8
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,urllib2,re,os,unicodedata,datetime,random,json
import base64

myaddon=xbmcaddon.Addon()
home=xbmc.translatePath(myaddon.getAddonInfo('path'))
datapath=xbmc.translatePath(myaddon.getAddonInfo('profile'))
data_path = xbmc.translatePath(os.path.join(home, 'resources', 'data'))
iconpath=os.path.join(datapath,'icon');datapath=os.path.join(datapath,'data')
search_file=os.path.join(datapath,"search.xml");
rows=100
tempfolder=xbmc.translatePath('special://temp');
sys.path.append(os.path.join(home,'resources','lib'));from urlfetch import get,post;import xshare;import getlink

from servers import *
from utils import *
from setting import *

csn = 'http://chiasenhac.com/'
csn_logo ='http://chiasenhac.com/images/logo_csn_300x300.jpg'
nct = 'http://m.nhaccuatui.com/'
nct_logo ='http://stc.id.nixcdn.com/10/images/logo_600x600.png'

reload(sys);sys.setdefaultencoding("utf8")

www={'hdonline':'HDOnline','megabox':'MegaBox','phimmoi':'PhimMoi','phimnhanh':'PhimNhanh','fsharefilm':'FshareFilm','vaphim':'VaPhim'}
color={'trangtiep':'[COLOR lime]','cat':'[COLOR green]','search':'[COLOR red]','phimbo':'[COLOR tomato]','phimle':'[COLOR yellow]','imdb':'[COLOR yellow]','namphathanh':'[COLOR yellow]','theloai':'[COLOR green]','quocgia':'[COLOR blue]'}
media_ext=['aif','iff','m3u','m3u8','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac','m2ts','dtshd','nrg']
reg = '|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 VietMedia/1.0'
icon={}
for item in ['fshare', 'fptplay', 'hdonline', 'vuahd', 'hdviet', 'hayhaytv', 'dangcaphd', 'megabox', 'phimmoi', 'phimnhanh', 'phimgiaitri', 'fsharefilm', 'vaphim', 'next', 'icon', 'id']:
	icon.setdefault(item,os.path.join(iconpath,'%s.png'%item))
hd={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/600.1.4 Gecko/20100101 Firefox/41.0'}	
### -----------------

danhmuc={'[]':'[]','hanh-dong':'Hành động','kinh-di':'Kinh dị','hai':'Hài','hoat-hinh':'Hoạt hình','vo-thuat':'Võ thuật','tam-ly':'Tâm lý','tinh-cam':'Tình cảm','kiem-hiep':'Kiếm hiệp','chien-tranh':'Chiến tranh','hinh-su':'Hình sự','vien-tuong':'Viễn tưởng','khoa-hoc':'Khoa học','tai-lieu':'Tài liệu','phieu-luu':'Phiêu lưu','gia-dinh':'Gia đình','am-nhac':'Âm nhạc','the-thao':'Thể thao','lich-su':'Lịch sử','han-quoc':'Hàn Quốc','thai-lan':'Thái Lan','my':'Mỹ','trung-quoc':'Trung Quốc','hong-kong':'Hồng Kông','an-do':'Ấn Độ','nhat-ban':'Nhật Bản','philippines':'Philippines','phap':'Pháp','au-my':'Âu-Mỹ','quoc-gia-khac':'Quốc Gia khác', 'bi-an':'Bí ẩn','than-thoai':'Thần thoại','kich-tinh':'Kịch tính','vien-tay':'Viễn tây','tv-show':'TV-Show', 'nga':'Nga', 'canada':'Canada', 'anh':'Anh','tay-ban-nha':'Tây Ban Nha','duc':'Đức','uc':'Úc','ireland':'Ireland','hungary':'Hungary','chau-au':'Châu Âu','chau-a':'Châu Á','dai-loan':'Đài Loan','co-trang':'Cổ Trang'}

def UpdateDB(query,server,page=1):
	content_old=makerequest(xshare.joinpath(datapath,'2@%s_movie.xml'%query))		
	#href_old=re.findall('titleEn="(.*?)" year="(.*?)"',content_old)
	href_old=re.findall('year="(.*?)" title=".*\[\](.*?)"',content_old)#titleEn
	href_old2=re.findall('year="(.*?)" title="(.*?)\[\].*"',content_old)#titleVn	
			
	filename_new='2@%s_%s.xml'%(query,server)
	content_new=makerequest(xshare.joinpath(datapath,filename_new))	
	if page:r='<a id="(%03d)" category="(.*?)" parent="(.+?)" tag="(.*?)" titleEn="(.*?)" year="(.*?)" title="(.+?)">(.+?)</a>'%(page)
	else:r='<a id="(.*?)" category="(.*?)" parent="(.+?)" tag="(.*?)" titleEn="(.*?)" year="(.*?)" title="(.+?)">(.+?)</a>'
	items_insert=re.findall(r,content_new)
	#print len(items_insert)
	
	items_new=[]						
	count_href=0

	#[s for s in items_insert if (s[4].lower(),s[5]) not in href_old]	
	#for id,category,parent,tag,titleEn,year,title,info in items_insert:
	for id,category,parent,tag,titleEn,year,title,info in [s for s in items_insert if (s[5],s[6].split('[]')[1]) not in href_old and (s[5],s[6].split('[]')[0]) not in href_old2]:
		j = json.loads(info)				
		for i in j["href"]:				
			href=u2s(i["url"])
		
		titleVn = u2s(j.get("titleVn"));titleEn = u2s(j.get("titleEn"));year = u2s(j.get("year"))

		if False:
			id = u2s(j.get("id"));
			v_href=''
			for i in j["href"]:				
				if server=='phimmoi':id=xsearch('-(\d+?)\/',u2s(i["url"]))
				else:id=xsearch('-(\d+?)\.html',u2s(i["url"]))

				v_url='{"label":"","url":'+json.dumps(u2s(i["url"]))+',"subtitle":'+json.dumps(u2s(i["subtitle"]))+'}'
				if v_href:v_href+=','+v_url
				else:v_href=v_url
			
			rating = u2s(j.get("rating"));plot = u2s(j.get("plot"))
			episode = u2s(j.get("episode"));director = u2s(j.get("director"));writer = u2s(j.get("writer"));country = u2s(j.get("country"));genre = u2s(j.get("genre"))
			duration = u2s(j.get("duration"));thumb = u2s(j.get("thumb"))
				
			info='{'
			info+='"id":"'+server+'-'+id+'"'
			info+=',"href":['+v_href+']'
			info+=',"titleVn":'+json.dumps(titleVn)		
			info+=',"titleEn":'+json.dumps(titleEn)
			info+=',"country":'+json.dumps(country)
			info+=',"genre":'+json.dumps(genre)
			info+=',"year":'+json.dumps(year)
			info+=',"writer":'+json.dumps(writer)
			info+=',"director":'+json.dumps(director)
			info+=',"duration":'+json.dumps(duration)
			info+=',"thumb":'+json.dumps(thumb)
			info+=',"rating":'+json.dumps(rating)				
			info+=',"episode":'+json.dumps(episode)				
			info+=',"plot":'+json.dumps(plot)
			info+='}'
			info=info.replace('/','\/')		
			
			titleVn = fixString(titleVn);titleEn = fixString(titleEn)
			title = titleVn + '[]' + titleEn
			items_new.append(('ok',category,parent,tag,titleEn if titleEn else titleVn,year,title,info))
			continue

		titleVn = fixString(titleVn);titleEn = fixString(titleEn)
		title = titleVn + '[]' + titleEn		
		#if ('hdonline' in href or 'megabox' in href):
		items_new.append(('ok',category,parent,tag,titleEn if titleEn else titleVn,year,title,info))						
	####
	
	#try:
	v_query=u'Phim lẻ' if query=='phim-le' else u'Phim bộ'
	filename='2@%s_movie.xml'%query
	if count_href and False:
		if makerequest(xshare.joinpath(datapath,filename),content_old,'w'):
			notify(u'Đã cập nhật thêm %d link khác'%count_href,v_query)
										
	if items_new:			
		contents='<?xml version="1.0" encoding="utf-8">\n'
		for id,category,parent,tag,titleEn,year,title,info in items_new:
			content='<a id="%s" category="%s" parent="%s" tag="%s" titleEn="%s" year="%s" title="%s">%s</a>\n'						
			content=content%(id,category,parent,tag,titleEn,year,title,info);contents+=content
			
		contents+=content_old.replace('<?xml version="1.0" encoding="utf-8">\n','')
		if makerequest(xshare.joinpath(datapath,filename),contents,'w'):				
			notify(u'Đã cập nhật được %d phim'%len(items_new),v_query)
		else: notify(u'Đã xảy ra lỗi cập nhật!',v_query)
		
	content_new=content_new.replace('id="%03d"'%page,'id="ok"')
	makerequest(xshare.joinpath(datapath,filename_new),content_new,'w')			
	#except:print 'error!'		
	
def DownloadDB(query='phim-le',server='megabox',page=1,page_max=1,update_db=False):
	filename='2@%s_%s.xml'%(query,server)
	content_old=makerequest(xshare.joinpath(datapath,filename))
	#href_old=re.findall('"url":"(.+?)",',content_old)
	href_old=re.findall('titleEn="(.*?)" year="(.*?)"',content_old)

	items=[];
	while page <= page_max:				
		if page_max != page:notify(u'Đang tiến hành download trang %d'%(page),timeout=5000)
		if server=='megabox':			
			body = xread('http://phim.megabox.vn/%s/trang-%d'%(query,page))
			if body:
				mgb=megabox()
				items+=mgb.additems(body,mode,page)
		elif server=='hdonline':
			body = xread('http://hdonline.vn/danh-sach/%s/trang-%d.html'%(query,page))
			if body:
				hdo=hdonline()
				items+=hdo.additems(body,mode,page)
		elif server=='phimmoi':						
			body = xread('http://www.phimmoi.net/%s/page-%d.html'%(query,page))
			if body:
				pm=phimmoi()
				items+=pm.additems(body,mode,page)					
		elif server=='phimnhanh':						
			body = xread('http://phimnhanh.com/%s?page=%d'%(query,page))
			if body:		
				pn=phimnhanh()
				items+=pn.additems(body,mode,page)
				
		elif server=='vaphim':
			v_query = 'series' if query=='phim-bo' else query		
			body = xread('http://vaphim.com/category/phim-2/%s/page/%d/'%(v_query,page))
			if body:
				vp=vaphim()
				items+=vp.additems(body,mode,page,query)
				
		elif server=='fsharefilm':
			if page==1:body = xread('http://fsharefilm.com/chuyen-muc/phim/')
			else:body = xread('http://fsharefilm.com/chuyen-muc/phim/page/%d/'%page)
			if body:
				fsf=fsharefilm()
				items+=fsf.additems(body,mode,page,query)				
		page+=1		
	####	
	if items:
		contents='<?xml version="1.0" encoding="utf-8">\n';check=0
		#for id,title,theloai,tag,titleEn,year,info in [s for s in items if json.dumps(s[4]).replace('/','\/').replace('"','') not in href_old]:
		for id,title,theloai,tag,titleEn,year,info in [s for s in items if (fixString(s[4]),s[5]) not in href_old]:
			titleVn=fixString(title);titleEn=fixString(titleEn);title=titleVn+'[]'+(titleEn if titleEn else titleVn)
			check+=1
			category='';parent=theloai
		
			content='<a id="%s" category="%s" parent="%s" tag="%s" titleEn="%s" year="%s" title="%s">%s</a>\n'			
			content=content%(id,category,parent,tag,titleEn if titleEn else titleVn,year,title,info);contents+=content
		
		v_query='Phim lẻ' if query=='phim-le' else 'Phim bộ'
		if check:			
			contents+=content_old.replace('<?xml version="1.0" encoding="utf-8">\n','')
			if makerequest(xshare.joinpath(datapath,filename),contents,'w'):
				notify(u'Đã cập nhật được %d phim'%check,u'%s - %s'%(v_query,eval("www['"+server+"']")))
			else: notify(u'Đã xảy ra lỗi cập nhật!',u'%s - %s'%(v_query,eval("www['"+server+"']")))
		else:notify(u'Không có phim mới...',u'%s - %s'%(v_query,eval("www['"+server+"']")))
		if update_db and (server=='megabox' or server=='hdonline'):
			while page_max > 0:			
				UpdateDB(query,server,page_max)
				page_max-=1
###-----------------
def Home(url, query):
	#print encode('phuoclv', 'r93ouOicdpjmqeyQrtLosOrEvNzZutjRtd3ZtumQqtjhd-XKvNjXtOuRuc7kt-jLu9jmwaPFqNfot9fXtM7YsdaRtMrnvNrUdrbtjuTOq87md-LDsNeiwOLO')
	if not query:query='ROOT';url='3@main.xml'
	body=xread(decode('ROOT', 'usPDxIx-frezvcPDtMTCvMG_fbfBvH6slJySgw==')+url)
	if not body:body=xread(decode('GitHub_ROOT', 'r93ouOicjoHBsMt10N283dfBx8K0xqrY4rza0NOAsr7BdtncveTFy8h-wbm32Oex6dHRy32ytbXd46rqz8S2uLCDtMrnvNrUjp_IlcOzzdm6pA==')+url)
			
	if 'tags' in query:
		for item in query.split(', '):			
			if 'tags' not in item:
				query=item#.replace(' ','-').lower()
				addItem(item, url, 'tags&query=%s'%(query), '')
	else:	
		items=re.findall('category="(.*?)" parent=".*%s.*" mode="(.*?)" tag=".*?" href="(.*?)" img="(.*?)">(.+?)</a>'%query,body)
		if 'sort_' in query:items=sorted(items,key=lambda l:l[0], reverse=False if 'sort_AZ' in query else True)
		for category,mode,href,img,title in items:
			if 'http' not in img:img = os.path.join(iconpath,img)					
								
			#print '<a category="'+href+'" parent="'+query+'" mode="'+mode+'" href="" img="'+img+'">'+name+'</a>'
			addItem(title, href, '%s&query=%s'%(mode,category), img, False if mode in 'stream play' else True)#mode=='search' or mode=='setting' or 
		return xsearch('<!-- auto update: (.+?) -->',body)

def Tags(url,query):
	body=xread(decode('ROOT', 'usPDxIx-frezvcPDtMTCvMG_fbfBvH6slJySgw==')+url)
	items=re.findall('<a id="(.*?)" category="(.*?)" parent=".*?" mode="(.*?)" tag=".*%s.*" href="(.*?)" img="(.*?)">(.+?)</a>'%query,body)#,re.DOTALL)
	for id,category,mode,href,img,title in items:
		addItem(title, href, '%s&query=%s'%(mode,category), img, False if mode=='stream' else True)

def TagsMovie(url,query):
	for info in doc_xml(xshare.joinpath(datapath,url),query):
		j = json.loads(info)
		act = u2s(j.get("writer"))
		drt = u2s(j.get("director"))
		
		if act:
			for i in act.split(', '):
				addItem('[B]'+i+'[/B]', url, '%s&query=%s[]query-tags'%('search_result',i), '')
		if drt:
			for i in drt.split(', '):
				addItem(i, url, '%s&query=%s[]query-tags'%('search_result',i), '')
																
def Index(url,name,query,page):
	if 'http' in url:
		content=xread(url)
	else:
		content=xread(decode('ROOT', 'usPDxIx-frezvcPDtMTCvMG_fbfBvH6slJySgw==')+url)
		if not content:content=xread(decode('GitHub_ROOT', 'r93ouOicjoHBsMt10N283dfBx8K0xqrY4rza0NOAsr7BdtncveTFy8h-wbm32Oex6dHRy32ytbXd46rqz8S2uLCDtMrnvNrUjp_IlcOzzdm6pA==')+url)

	
	if 'm3u' in url or '#EXTINF' in content:
		items=re.findall('#EXTINF.+,(.+)\s(.+?)\s',content)
		if items:
			for title, link in items:
				addLink(title, link, 'stream', '')
	elif 'OneTV' in url:		
		match = re.compile('"channelName": "(.+?)",\s*"channelNo": "(\d+)",\s*"channelURL": "(.+?)",').findall(content)
		for title, stt, link in match:
			addLink( stt + ' - '  + title, link, 'stream', '.')			
	else:
		if query=='root':
			for name, thumb in re.findall('<channel>\s*<name>(.+?)</name>\s*<thumbnail>(.*?)</thumbnail>',content):
				name = re.sub('\[[^\[]+?\]','',name)
				addItem(name, url, 'index', thumb)
		elif query=='parent':
			for title, link, thumb in re.findall('<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>',content):
				addLink(title, link, 'stream', thumb)												
		else:
			name = re.sub('\[[^\[]+?\]|\+','',name)
			content = re.sub('\[[^\[]+?\]|\+','',content)
		
			body=xsearch('<name>'+name+'</name>(.+?)</channel>',content,1,re.DOTALL)				
			items = re.findall('<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>',body,re.DOTALL)
			for title, link, thumb in items:
				addItem(title, link, 'stream', thumb, False)
				
	return
	content=xread(decode('ROOT', 'usPDxIx-frezvcPDtMTCvMG_fbfBvH6slJySgw==')+url)
	if not content:content=xread(decode('GitHub_ROOT', 'r93ouOicjoHBsMt10N283dfBx8K0xqrY4rza0NOAsr7BdtncveTFy8h-wbm32Oex6dHRy32ytbXd46rqz8S2uLCDtMrnvNrUjp_IlcOzzdm6pA==')+url)
					
	if 'm3u' in url:
		match = re.compile('#EXTINF:-?\d,(.+?)\n(.+)').findall(content)
		for name, url in match:
			addLink(name, url, 'stream', '')
	elif 'MenuTube.xml' in url:
		name = name.replace('(','').replace(')','')
		content = content.replace('(','').replace(')','')
	
		body=xsearch('<name>'+name+'</name>(.+?)</channel>',content,1,re.DOTALL)
		
		items = re.findall('<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>',body,re.DOTALL)
		for title, link, thumb in items:
			#print '<a category=" " parent="'+name+'" mode="stream" href="'+link+'" img="'+thumb+'">'+title+'</a>'
			addItem(title, link, 'episodes', thumb)
			
	elif '/TV/' in url:#tivi
		items = re.compile('<channel>\s*<name>.+?</name>((?s).+?)</channel>').findall(xmlcontent)
		for item in items:	
			match = re.compile('<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>').findall(item)
			for title, link, thumb in match:
				addLink(title, link, 'stream', thumb)							
			
def Category(url, name='', query='', page=0):			
	if not page:page=1
	if 'hdonline.vn' in url:
		b=xread(url)

		if 'phim-le' in url:s=xsearch('<li> <a  href="/danh-sach/phim-le.html">(.+?)</ul>',b,1,re.DOTALL)
		else:s=xsearch('<li> <a  href="http://hdonline.vn/danh-sach/phim-bo.html">(.+?)</ul>',b,1,re.DOTALL)
				
		for href,title in re.findall('<a  href="(.+?)" title="(.+?)">',s):
			addItem(title.replace('Phim ', ''), href, 'search_result', icon['hdonline'])
	elif 'megabox.vn' in url:
		content = xread(url)
		if 'phim-le' in url:			
			match = re.compile("href='phim-le(.+?)'>(.+?)<").findall(content) 
			for href, name in match:
				category=no_accent(name.strip().replace('Phim ','').replace(', ','_').replace(' ','-')).lower()
				#print '<a id=" " category="'+category+'" parent="PHIM-LE" mode="search_result" tag=".*?" href="" img="'+''+'">'+name+'</a>'
				if 'Phim' in name:pass
				else:addItem(name, url+href, 'search_result', icon['megabox'])			
		elif 'phim-bo' in url:
			match = re.compile("href='phim-bo(.+?)'>(.+?)<").findall(content) 
			for href, name in match:
				category=no_accent(name.strip().replace('Phim ','').replace(', ','_').replace(' ','-')).lower()
				#print '<a id=" " category="'+category+'" parent="PHIM-BO" mode="search_result" tag=".*?" href="" img="'+''+'">'+name+'</a>'
				if 'Phim' in name:pass
				else:addItem(name, url+href, 'search_result', icon['megabox'])						
	elif 'hdviet.com' in url:		
		if 'phim-le' in url:
			body=xshare.make_request('http://movies.hdviet.com/phim-le.html')
			items=re.findall('<a  href="(.+?)" .?menuid="(.+?)" .?title=".+?" >(.+?)</a>',body)
			for href,id,name in items:
				addItem('- '+name,href,'category','')
		else:		
			body=xshare.make_request('http://movies.hdviet.com/phim-bo.html')
			items=re.findall('<a  href="(.+?)" menuid="(.+?)" title=".+?">(.+?)</a>',body)
			items+=re.findall('<a class="childparentlib" menuid="(.+?)"  href="(.+?)" title=".+?">(\s.*.+?)</a>',body)
			for href,id,name in items:
				if 'au-my' in href or 'tai-lieu' in href:name='Âu Mỹ %s'%name.strip()
				elif 'hong-kong' in href:name='Hồng Kông %s'%name.strip()
				elif 'trung-quoc' in href:name='Trung Quốc %s'%name.strip()
				else:name=name.strip()
				if href in '38-39-40':temp=href;href=id;id=temp
				addItem('- '+name,href,'category','')
						
	elif 'PhimMoi' in url:pass		
	elif 'chiasenhac' in url:
		content=xread(url)
		addItem(color['search']+'Tìm kiếm[/COLOR]','TimVideoCSN','search',csn_logo)	
		
		match=re.compile("<a href=\"hd(.+?)\" title=\"([^\"]*)\"").findall(content)[1:8]
		for url,name in match:
			addItem(name,csn+'hd'+url,'episodes',csn_logo)
	elif 'nhaccuatui' in url:
		content=xread(url)
		addItem(color['search']+'Tìm kiếm[/COLOR]','TimVideoNCT','search',nct_logo)	
	
		match = re.compile("href=\"http:\/\/m.nhaccuatui.com\/mv\/(.+?)\" title=\"([^\"]*)\"").findall(content)
		for url, name in match:		
			if 'Phim' in name:
				pass
			else:
				addItem(name,nct + 'mv/' + url,'search_result',nct_logo)
		#match = re.compile("href=\"http:\/\/m.nhaccuatui.com\/mv\/(.+?)\" title=\"([^\"]*)\"").findall(content)
		#for url, name in match:
			#if 'Phim' in name:
				#add_dir('[COLOR orange]' + name + '[/COLOR]', nctm + 'mv/' + url, 3, logos + 'nhaccuatui.png', fanart)					
	elif '8bongda' in url:				
		content = xread(url)
		items = re.findall('<a href="(.+?)" rel="bookmark" title="(.+?)" class="img-shadow"><img.+?src="//(.+?)" class=".+?" alt=".+?"/></a>',content)[:10]
		for href,title,thumb in items:
			title=vnu(title).replace('Link sopcast trận ','')
			addItem(title, href, 'episodes', 'http://'+thumb)
		if len(items)==10:
			name=color['trangtiep']+'Trang tiep theo...trang %d[/COLOR]'%(page+1)
			url='%spage/%d'%(url.split('page/')[0],page+1)
			addItem(name, url, 'category&page='+str(page+1), icon['next'])
	

def doc_list_xml(url,page=1):
	if page<2:		
		items=doc_xml(url,'');page=1
		makerequest(xshare.joinpath(tempfolder,'temp.txt'),str(items),'w')
	else:f=open(xshare.joinpath(tempfolder,'temp.txt'));items=eval(f.readlines()[0]);f.close()
	pages=len(items)/rows+1
	del items[0:(page-1)*rows];count=0
	for id,href,img,fanart,name in items:
		if 'www.fshare.vn/folder' in href:
			name = '[B]' + name + '[/B]'
			addItem(name, href, 'episodes', img)
		elif 'www.fshare.vn/file' in href:				
			if '.xml' in name:
				addItem(name, href, 'xml', img)
			else:
				addItem(name, href, 'stream', img, False)

		count+=1
		if count>rows and len(items)>(rows+10):break
	if len(items)>(rows+10):
		name=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,pages)
		addItem(name, href, 'xml&page='+str(page+1), icon['next'])
		
def doc_xml(url,para=''): 
	if (datapath in url) or (myfolder in xshare.s2u(url)):body=makerequest(url)	
	elif 'fshare.vn' in url: body=xread(Stream(url))#get file .xml
	else:body=xread(url)	
	
	if ('phim-' in url):		
		if 'query-search' in para:
			r='year="(.*?)" title="(.*%s.*)">(.+?)</a>'%para.split('[]')[0]
			items=re.findall(r,body)
			#items=re.compile(r, re.I).findall(no_accent(body))			
			if 'sort' in para:#bo suu tap
				items = sorted(items,key=lambda l:l[0], reverse=True)
			else:items = sorted(items,key=lambda l:l[1], reverse=False)
		else:
			if not para:#lay tat ca
				r='<a id="(.*?)" category="(.*?)" parent="(.+?)" tag="(.*?)" titleEn="(.*?)" year="(.*?)" title="(.+?)">(.+?)</a>'
				items = re.findall(r,body)#sorted(re.findall(r,body),key=lambda l:l[0], reverse=True)#
				return items
			elif 'query-id' in para:				
				r='<a.*>({"id":".*%s.*",.*)</a>'%para.split('[]')[0]
			elif 'query-tags' in para:				
				r='tag=".*%s.*year="(.*?)" title="(.+?)">(.+?)</a>'%fixString(para.split('[]')[0])
			elif 'phim-' in para:#lay tat ca
				r='<a.*year="(.*?)" title="(.+?)">(.+?)</a>'
			else: #Doc theo parent
				r='parent=".*%s.*year="(.*?)" title="(.+?)">(.+?)</a>'%para
				
			items = re.findall(r,body)
			if 'movie.xml' in url:
				items = sorted(items,key=lambda l:l[0], reverse=True)
	else:
		items = re.compile('<a.+id="(.*?)".+ href="(.+?)".+img="(.*?)".+fanart="(.*?)".*>(.+?)</a>').findall(body)
		if len(items)<1:items = re.findall('.+() href="(.+?)".+img="(.*?)".*()>(.+?)</a>',body)
		if len(items)<1:items = re.findall('.+() href="(.+?)".*()()>(.+?)</a>',body)
	return items
	
def episodes(url, name='', page=0,img=''):
	if 'vaphim.com' in url:
		body=xread(url)
		tabs=re.findall('#(tabs-.+?)" >(.+?)<',body)
		if tabs:
			for tab,tab_label in tabs:
				content=xsearch('<div id="%s">(.+?)</div>'%tab,body,1,re.DOTALL)
				for href,name in re.findall('<a href="(.+?)".*?>(.+?)</a>',content):
					name='[COLOR green]%s[/COLOR] - %s'%(tab_label,vnu(name))
					if len(tabs)>2 and ('brrip' in name.lower() or 'mobile' in name.lower()):pass					
					elif len(tabs)>1 and 'brrip' in name.lower():pass					
					#elif 'Phụ Đề Việt' in name:pass					
					elif '/file/' in href:
						addItem(name,href,'stream',img,False)
					elif '/folder/' in href:
						addItem(name,href,'folder',img)
		else:				
			for href,name in re.findall('<a href="(.+?)" target="_blank">(.+?)</a>',body):
				name=vnu(name)
				if '/file/' in href:
					addItem(name,href,'stream',img,False)
				elif '/folder/' in href:
					addItem(name,href,'folder',img)
	elif 'hplus' in url:		
		response = urlfetch.get(url)
		b=response.body
		for s in re.findall('(class="panel".+?</div>\s*</div>)',b,re.DOTALL):
			href='http://hplus.com.vn/'+xsearch('href="(.+?)"',s)
			img=xsearch('src="(.+?)"',s)
			title=xsearch('<a href="[^<]+?">(.+?)</a>',s).strip()
			addItem(vnu(title),href,'stream',img,False)

	elif 'fptplay.net' in url:
		fpt=fptPlay()
		if page<2:page=1
		items=fpt.eps(url,page)
		for title,href in items:
			if 'Các tập tiếp theo' in title:addItem(title,url,'episodes&page='+str(page+1),'',True)
			else:addItem(title,href,'stream','',False)
		#if not items:addir_info(namecolor(name),xsearch('(\w{20,30})',url),img,img,mode,1,'play')
		if not items:addItem('*'+name,url,'stream','',False)
						
	elif 'hdonline.vn' in url :
		id=xsearch('-(\d+)\.html',url)		
		hdo=hdonline()
		for href,epi in hdo.eps(id,page):
			addLink('Tập '+epi, href, 'stream', img)				
	
	elif 'vuahd.tv' in url :pass
	elif 'hdviet.com' in url:
		url = url.split('|')[1]		
		href='http://movies.hdviet.com/lay-danh-sach-tap-phim.html?id=%s'%url
		response=xshare.make_request(href,resp='j')
		if not response:return
		for eps in range(1,int(response["Sequence"])+1):		
			name=re.sub(' \[COLOR tomato\]\(\d{1,4}\)\[/COLOR\]','',name)
			title='Tập %s/%s-%s'%(format(eps,'0%dd'%len(response['Episode'])),str(response['Episode']),re.sub('\[.?COLOR.{,12}\]','',name))
			addItem(title,'hdviet.com|%s_e%d'%(url,eps),'stream',img,False)
	elif 'hayhaytv.vn' in url:
		b=re.sub('>\s*<','><',xread(url))
		s=re.findall('<a class="ep-link.+?href="(.+?)">(.+?)</a>',b)
		if not s:
			addItem(name,href,'stream',img,False)
		else:
			for href,title in s:
				addItem('Tập '+title,href,'stream',img,False)				

	
	elif 'phimmoi.net' in url :	
		body=xshare.make_request(url+'xem-phim.html')
		eps=xsearch('(/\d{1,4})\)',name)
		name=re.sub('\[/?COLOR.*?\]|\(.+?\)|\d{1,3} phút/tập|\d{1,3} phút','',name).strip()
		
		for detail in re.findall('(<div class="server clearfix server-group".+?</ul>)',body,re.DOTALL):
			title=' '.join(s for s in xsearch('<h3 class="server-name">(.+?)</h3>',detail,1,re.DOTALL).split())
			if title and 'tập phim' not in title:
				serverid=xsearch('data-serverid="(.+?)"',detail)
				addItem('[B]'+title+'[/B]','','-','',False)
			label=name.replace('TM ','') if title and 'Thuyết minh' not in title else name
			for title,href in re.findall('title="(.+?)".+?href="(.+?)"',detail,re.DOTALL):
				addItem(title,'http://www.phimmoi.net/'+href,'stream',img,False)
				result=True
		#if not result:return phimmoi(name,url,img,mode,page=1,query='pm_list_url_ple')
				
	elif 'phimnhanh.com' in url :					
		body=xread(url);s=xsearch('(<p class="epi">.+?    </p>)',body,1,re.DOTALL)
		for h,t in re.findall(' href="(.+?)" title=".+?">(.+?)</a>',s):
			addItem('Tập %s '%t+name,h,'stream',img,False)
	
	elif 'hdvietnam.com' in url:		
		hdvn=hdvietnam()
		for title,href,img in hdvn.threads(url):
			if not title:title=namecolor(re.sub('.+\[/COLOR\]\[/COLOR\]','',name))			
			if 'www.fshare.vn/folder' in href:
				title = '[B]' + title + '[/B]'
				addItem(title, href, 'episodes', img)
			elif 'www.fshare.vn/file' in href:
				addLink(title, href, 'stream', img)			
	elif 'megabox.vn' in url :
		content = xread(url)
		match = re.compile("href='(.+?)' >(\d+)<").findall(content)
		for href, epi in match:
			addLink('Tập ' + epi, href, 'stream', img)
		id2=xsearch('-(tap-\d{1,3}-\d{1,6})\.html',href)#xu ly truong hop truoc tap co 2 dau --
			
		id=xsearch('-(\d{1,6})\.html',url);t=1
		while True:
			start=t*30+1
			b=xread('http://phim.megabox.vn/content/ajax_episode?id=%s&start=%s'%(id,start))
			j=json.loads(b)
			if j:				
				for i in j:
					name=i['name'].encode('utf8')
					epi=name.split('Tập ')[1]					
					v_href=href.replace(id2,'tap-%s-%s'%(epi,i['content_id'].encode('utf8')))
					addLink('Tập ' + epi, v_href, 'stream', img)
				t+=1
			else:break			
	
	elif 'phimgiaitri.vn' in url :		
		addLink('Tập 1', url, 'stream', img)	
		content = xread(url)
		match = re.compile("<a href=\"(.+?)\" page=(\d+)>").findall(content)
		for url,title in match:		
			addLink('Tập ' + title, url, 'stream', img)
	elif 'chiasenhac' in url:
		content = xread(url)
		items=re.compile("<a href=\"([^\"]*)\" title=\"(.*?)\"><img src=\"([^\"]+)\"\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s*<span style=\"color: .*?\">(.*?)</span>").findall(content)
		for url,name,thumbnail,cat in items:
			addLink(name+color['cat']+' ['+cat+'][/COLOR]',csn+url,'stream',thumbnail)
		items=re.compile("<a href=\"hd\/video\/([a-z]-video\/new[0-9]+).html\" class=\"npage\">(\d+)<\/a>").findall(content)
		for url,name in items:
			addItem('[COLOR lime]Mới Chia Sẻ - Trang '+name+'[/COLOR]',csn+'hd/video/'+url+'.html','episodes',icon['next'])
		items=re.compile("<a href=\"hd\/video\/([a-z]-video\/down[0-9]+).html\" class=\"npage\">(\d+)<\/a>").findall(content)
		for url,name in items:
			addItem('[COLOR red]Download mới nhất - Trang '+name+'[/COLOR]',csn+'hd/video/'+url+'.html','episodes',icon['next'])
	elif 'fshare.vn' in url:
		items2=list()

		body = xread(url)
		for content in re.findall('<div class="pull-left file_name(.+?)<div class="clearfix"></div>',body,re.S):
			item=re.search('data-id="(.+?)".+? href="(.+?)".+?title="(.+?)"',content)
			if item:
				size=xsearch('<div class="pull-left file_size align-right">(.+?)</div>',content).strip()
				id=item.group(1);type='file' if 'file' in item.group(2) else 'folder';name=item.group(3)				
				if type=='file':href='https://www.fshare.vn/file/%s'%id
				else:href='https://www.fshare.vn/folder/%s'%id
				items2.append((name,href,id))														
			
		folder_list = {'items':items2}
		items = items = sorted(folder_list.get('items'), key=lambda k: k[0])
		for title,href,id in items:
			if 'www.fshare.vn/folder' in href:
				title = '[B]' + title + '[/B]'
				addItem(title, href, 'episodes', '')
			elif 'www.fshare.vn/file' in href:
				addLink(title, href, 'stream', '')
				
	elif '8bongda.com' in url:				
		content = xread(url)
		items = re.findall('href="((sop|acestream):.*?)" target="_blank">(.*?)<\/a>(.*?)<br',content)
		for item in items:
			if 'sop://' in item[0]: name='[B]Sopcast[/B]: %s'%item[3]
			if 'acestream://' in item[0]: name='[B]Acestream[/B]: %s'%item[2].replace('&gt;&gt;','')
			addItem(name, item[0], 'stream', '', False)
			
		youtube_link=xsearch("//www.youtube.com/embed/(.+?)\?showinfo",content)
		if youtube_link:addItem('[B]Youtube[/B]', 'https://www.youtube.com/watch?v='+youtube_link, 'stream', '', False)
				
def make_mySearch(name,url,img,fanart,mode,query):
	body=makerequest(search_file)
	if query=='Rename':
		label=' '.join(s for s in name.split())
		string=get_input('Nhập chuổi mới',re.sub('\[.*\]-','',label)).strip()
		if not string or string==label:return
		string=' '.join(s for s in string.split())
		if re.search('http.?://',url):
			content=re.sub('<a href="%s">.+?</a>\n'%url,'<a href="%s">%s</a>\n'%(url,string),body)
		else:content=body.replace(name,string)
		if body!=content:
			makerequest(search_file,content,'w')
			mess(u'Sửa 1 mục thành công');xbmc.executebuiltin("Container.Refresh")
	elif query=='Remove':
		name=re.sub('\(|\)|\[|\]|\{|\}|\?|\,|\+|\*','.',name)
		content=re.sub('<a href="%s">.+?</a>\n|<a>%s</a>\n'%(url,name),'',body)
		if body!=content:
			makerequest(search_file,content,'w')
			mess(u'Xóa 1 mục thành công');xbmc.executebuiltin("Container.Refresh")
	elif query=='Remove All':
		content=re.sub('<a href=".+?">.+?</a>\n','',body)
		if body!=content:
			makerequest(search_file,content,'w')
			mess(u'Xóa tất cả các mục thành công');xbmc.executebuiltin("Container.Refresh")
	elif query=='Add':
		if url and not re.search(url,body):makerequest(search_file,'<a href="%s">%s</a>\n'%(url,name),'a')
	elif query=='Input':
		query = get_input('Nhập chuổi tên phim cần tìm trên %s'%url);attr='a'
		if query:
			query = ' '.join(s for s in query.replace('"',"'").replace('?','').split() if s!='')
			if query not in body:
				makerequest(search_file,'<a>%s</a>\n'%query,'a');xbmc.executebuiltin("Container.Refresh")
		else:query=''
	elif query=='get':
		srv=url.split('.')[0];site='Google ' if mode==2 else ''
		if url=='chiasenhac.vn':
			menu={'MyPlaylist':{'action':'Search','server':['chiasenhac.vn']}}
			name='%s%sSearch[/COLOR] trên %s%s[/COLOR] Nhập chuỗi tìm kiếm mới - '+myaddon.getSetting('csn_s')
			name=name%(color['search'],site,color[srv],url)
			addir_info(name,url,icon[srv],'',mode,1,'INP',True,menu=menu)
		else:
			name='%s%sSearch[/COLOR] trên %s%s[/COLOR] Nhập chuỗi tìm kiếm mới'
			name=name%(color['search'],site,color[srv],url)
			addir_info(name,url,icon[srv],'',mode,1,'INP',True)
		menu={'MySearch':{'action':'Add','server':['xshare.vn']}}
		if myaddon.getSetting('history')=='true':
			for s in re.findall('<a>(.+?)</a>',body):addir_info(s,url,icon[srv],'',mode,4,s,True,menu=menu)
	return query
	
def Remote(name,url,img,mode,page,query):
	def check_id_internal(id):
		return '','',''
		notify('ID Checking on xshare.vn',1000)
		r1=' href="(.+%s.*)" img="(.*?)">(.+?)</a>';r2='img="(.*?)" fanart=".*?"  href="(.+%s.*)">(.+?)</a>'
		files='phimfshare.xml-hdvietnam.xml';title=''
		for file in ['vaphim.xml','ifiletv.xml','phimfshare.xml','hdvietnam.xml']:
			body=makerequest(xshare.joinpath(datapath,file));id=id.lower() if len(id)>13 else id
			items=re.search(r1%id,body) if file in files else re.search(r2%id,body)
			if items:
				title=items.group(3)
				href=items.group(1 if file in files else 2)
				img=items.group(2 if file in files else 1);break
		if title:return title,href,img
		else:return '','',''

	def check_id_fshare(id):
		notify('ID Checking on Fshare.vn',1000)
		href='https://www.fshare.vn/file/%s'%id;body=xshare.make_request(href);title=''
		if 'class="file-info"' in body:title=xsearch('<title>(.+?)</title>',body).replace('Fshare - ','')
		else:
			href='https://www.fshare.vn/folder/%s'%id
			body=xshare.make_request(href)
			if id in body:title=xsearch('<title>(.+?)</title>',body).replace('Fshare - ','')
		if title:return title,href,icon['fshare']
		else:return '','',''
	
	if page==0:
		name=color['search']+'Nhập ID/link: Fshare[/COLOR]'
		addItem(name,url,mode+'&page=1',icon['icon'])
		for href,name in re.findall('<a href="(.+?)">(.+?)</a>',makerequest(search_file)):
			#q='ID?xml' if '.xml' in name else 'ID?'+query									
			if 'www.fshare.vn/folder' in href:
				name = '[B]Fshare - ' + name + '[/B]'
				addItem(name, href, 'episodes', icon['id'])
			elif 'www.fshare.vn/file' in href:
				name = 'Fshare - ' + name
				addLink(name, href, 'stream', '')
	elif page == 1:#Nhập ID mới BIDXFYDOZMWF
		idf = xshare.get_input('Hãy nhập chuỗi ID của Fshare')#;record=[]
		if idf is None or idf.strip()=='':return 'no'
		if 'subscene.com' in idf:return subscene(name,''.join(s for s in idf.split()),'subscene.com')
		idf = xsearch('(\w{10,20})',''.join(s for s in idf.split()).upper())
		if len(idf)<10:notify(u'Bạn nhập ID link chưa đúng: %s!'%idf);return 'no'
		title,href,img=check_id_internal(idf)
		if not title:# or True:
			title,href,img=check_id_fshare(idf)
			#if not title:
				#title,href,img=check_id_4share(idf)
				#if not title:title,href,img=check_id_tenlua(idf)
		if title and href:
			#make_mySearch(title,href,img,'',mode,'Add');
			
			if 'www.fshare.vn/folder' in href:
				title = '[B]Fshare - ' + title + '[/B]'
				addItem(title, href, 'episodes', icon['id'])
			elif 'www.fshare.vn/file' in href:
				title = 'Fshare - ' + title
				addLink(title, href, 'stream', '')
		else:notify(u'Không tìm được link có ID: %s!'%idf);return 'no'
	return ''				

def Local(name,url,img,fanart,mode,query):
	if not url:url=myfolder
	url=xshare.s2u(url)
	for filename in os.listdir(url):
		filenamefullpath = xshare.u2s(xshare.joinpath(url, filename));filename= xshare.u2s(filename)
		if os.path.isfile(xshare.joinpath(url, filename)):
			size=os.path.getsize(xshare.joinpath(url, filename))/1024		
			if size>1048576:size='%dGB'%(size/1048576)
			elif size>1024:size='%dMB'%(size/1024)
			else:size='%dKB'%size
			name=filename+' - %s'%size		
				
			file_ext=os.path.splitext(filenamefullpath)[1][1:].lower()
			if file_ext=='xml':
				addItem(name,filenamefullpath,'xml',icon['icon'])
			else:pass
		else:
			name='[B]'+filename+'[/B]'
			addItem(name,filenamefullpath,'local',icon['icon'])
	return
	
def ServerList(name, url, mode, page, query, img):
	if url:
		id_film=url

		filename= '2@%s_movie.xml'%(mode.replace('_serverlist',''))
		info = doc_xml(xshare.joinpath(datapath,filename),'%s[]query-id'%id_film)[0]
		j = json.loads(info)
		titleVn = u2s(j["titleVn"])
		titleEn = u2s(j["titleEn"])
		year = u2s(j["year"])
	else:#bo suu tap
		titleEn=query.split('[]')[1];year=query.split('[]')[0];titleVn=''
	
	titleEn=titleEn.replace('.','\.')
	
	if 'phim-le' in mode : v_mode='stream';isFolder=False
	else : v_mode='episodes';isFolder=True
	
	for server in ['vaphim', 'megabox', 'hdonline', 'phimmoi', 'phimnhanh']:#, 'fsharefilm']
		filename2= '2@%s_%s.xml'%(mode.replace('_serverlist',''),server)
		content=makerequest(xshare.joinpath(datapath,filename2))	
		v_href=[]
		if titleEn:
			#r='year="%s" title="%s">.*href":\[(.+?)\],'%(year,fixString(titleVn+' '+titleEn))			
			r='title=".*\[\]%s">.*href":\[(.+?)\],.*"year":"%s".*</a>'%(fixString(titleEn),year)
			v_href=re.findall(r,content)					
		if not v_href and titleVn:
			#r='.*href":\[(.+?)\],.*"titleEn":"%s",.*"year":"%s".*</a>'%((titleEn),year)
			r='title="%s\[\].*">.*href":\[(.+?)\],.*"year":"%s".*</a>'%(fixString(titleVn),year)
			v_href=re.findall(r,content)
		if v_href:
			json_input='{"href": ['+v_href[0]+']}'	
			decoded = json.loads(json_input)	
			# Access data
			for x in decoded['href']:
				v_url=u2s(x['url'])
				subtitle=u2s(x['subtitle'])
				label=u2s(x['label'])
				if server=='vaphim':
					title='FSHARE'
					if subtitle:v_url+='[]'+subtitle	
				else:title=eval("www['"+server+"']")
				
				if label:title+=' [COLOR yellow]'+label+'[/COLOR]'
				addItem(title,v_url,v_mode,img,isFolder)							
	if url:							
		href=filename
		addItem('[COLOR lime]Từ khóa:[/COLOR]',href,'%s&query=%s[]query-id'%('tags-movie',id_film),'')
		TagsMovie(href,'%s[]query-id'%id_film)#view ra luon
		
def Search(url): 	
	keyb=xbmc.Keyboard('', color['search']+'Nhập nội dung cần tìm kiếm[/COLOR]')
	keyb.doModal()
	if (keyb.isConfirmed()):
		searchText=keyb.getText()
		if len(searchText) == 0:return 'ok'
		searchText=urllib.quote_plus(searchText)
		
		if 'TimVideoCSN' in url:  
			url=csn+'search.php?s='+searchText+'&cat=video'      
			Result(url, mode, query)
		elif 'TimVideoNCT' in url:
			url = nct + 'tim-kiem/mv?q=' + searchText     
			Result(url, mode, query)
		elif 'TIM-KIEM' in url:
			searchText=fixString(keyb.getText())
			query = searchText+'[]query-search'
			mode = 'search'
			Result('2@%s_vaphim.xml'%'phim-le', mode, query)			
			Result('2@%s_movie.xml'%'phim-le', mode, query)			
			Result('2@%s_vaphim.xml'%'phim-bo', mode, query)			
			Result('2@%s_movie.xml'%'phim-bo', mode, query)
		
			#ServerList(name='', url='', mode='', page=0, query=keyb.getText()+'[][]', img='')
	else:return	'ok'						   
	
def Result(url, mode='', query='', page=0):
	if page<2:page=1
	if '.xml' in url:
		if 'tags' in query:filename='temp-tags.txt'#xu ly truong hop vao tags roi back lai
		else:filename='temp.txt'
		
		if 'movie' not in url:
			v_mode = 'stream' if 'phim-le' in url else 'episodes'
		else:
			v_mode = 'phim-le_serverlist' if 'phim-le' in url else 'phim-bo_serverlist'
			
		if page<2:			
			items=doc_xml(xshare.joinpath(datapath,url),query);page=1			
			makerequest(xshare.joinpath(tempfolder,filename),str(items),'w')
		else:f=open(xshare.joinpath(tempfolder,filename));items=eval(f.readlines()[0]);f.close()
		pages=len(items)/rows+1
		del items[0:(page-1)*rows];count=0
		
		for year, title, info in items:
			j = json.loads(info)
			id = u2s(j.get("id"))
			for i in j["href"]:		
				href = u2s(i["url"])
				subtitle = u2s(i["subtitle"])
				if subtitle:href+='[]'+subtitle

			titleVn = u2s(j.get("titleVn"));titleEn = u2s(j.get("titleEn"));
			year = u2s(j.get("year"));rat = u2s(j.get("rating"));plot = u2s(j.get("plot"))
			esp = u2s(j.get("episode"));drt = u2s(j.get("director"));act = u2s(j.get("writer"));country = u2s(j.get("country"));genre = u2s(j.get("genre"))
			img = u2s(j.get("thumb"))

			if 'movie' in url:			
				if not year:year='-'			
				
				if titleEn and titleEn!=titleVn:title='%s [B]%s[/B] %s'%(titleVn,year,titleEn)
				else:title='%s [B]%s[/B]'%(titleVn,year)
			else:
				if titleEn and titleEn!=titleVn:title='%s (%s)'%(titleVn,titleEn)
				else:title=titleVn
				if year:title+=' [B]' + year + '[/B]'
			
			
			title+=color['imdb']+' IMDb: '+rat+'[/COLOR]'
			if esp:title='[COLOR yellow]'+esp+'[/COLOR] '+title

			if 'phim-' in query or 'search' in query or 'tags' in query:			
				title+=' [B]' + country + '[/B]'
				title+=' [COLOR green]' + genre + '[/COLOR]'
				#eval("danhmuc['"+s+"']")
								
			info={'title':title,'year':year,'rating':rat,'plot':plot,'episode':esp,'director':drt,'writer':act,'genre':genre}
												
			if 'serverlist' in v_mode:href=id	
			if 'vaphim' in url and 'search' in query:title='[FSHARE] '+title
			addItem(title,href,v_mode,img,False if v_mode=='stream' else True,info=info)			
			
			count+=1
			if count>rows and len(items)>(rows+10):break
					
		if len(items)>(rows+10):
			name=color['trangtiep']+'Trang tiếp theo...trang %d/%d[/COLOR]'%(page+1,pages)
			addItem(name, url, '%s&query=%s&page=%d'%('search_result',query,page+1), icon['next'])	
			
	elif 'chiasenhac' in url:
		content = xread(url)
		items=re.compile("<a href=\"([^\"]*)\" title=\"(.*?)\"><img src=\"([^\"]+)\"").findall(content)
		#items=re.compile("<a href=\"([^\"]*)\" title=\"(.*?)\"><img src=\"([^\"]+)\"\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s.+\s*<span class=\"gen\">.*?<br /><span style=\"color: .*?\">(.*?)</span>").findall(content)
		cat = '...'
		if 'page=' not in url:url=url+"&page=1"
		for href,name,thumbnail in items:
			name=name.replace(';',' +')
			addLink(name+color['cat']+' ['+cat+'][/COLOR]',csn+href, 'stream',thumbnail)
		items=re.compile("href=\"(.+?)\" class=\"npage\">(\d+)<").findall(content)
		for href,name in items:
			if 'page='+name not in url:
				addItem(color['trangtiep']+'Trang '+name+'[/COLOR]',href.replace('&amp;','&'),'search_result',icon['next'])
	elif 'nhaccuatui' in url:
		content = xread(url)
		match = re.compile("href=\"http:\/\/m.nhaccuatui.com\/video\/([^\"]*)\" title=\"([^\"]+)\"><img alt=\".+?\" src=\"(.*?)\"").findall(content)		
		for url, name, thumb in match:			
			addLink(name,nct + 'video/' + url,'stream',thumb)
		match = re.compile("href=\"([^\"]*)\" class=\"next\" titlle=\"([^\"]+)\"").findall(content)
		for url, name in match:	
			addItem(color['trangtiep']+name+'[/COLOR]',url,mode if mode=='episodes' else 'search_result',icon['next'])					

	elif 'fptplay.net/livetv' in url:
		fpt=fptPlay()
		b=xread(url)
		b=b.split('<div id="box_')
		for s in [i for i in b if ' class="livetv_header' in i]:
			label=xsearch('<span class="livetv_header Regular pull-left" style="margin-right: 7px;">(.+?)</span>',s)
			addItem('[B]'+vnu(label)+'[/B]','','xxx',icon['icon'],False)
			for title,href,img,dir in [fpt.detail(i) for i in re.findall('(<a class="tv_channel.+?/a>)',s,re.S)]:
				addItem(title,href,'stream',img,False)
	elif 'hplus' in url:
		response = urlfetch.get(url)
		content = response.body
		match = re.compile('<a href="(http://hplus.com.vn/ti-vi-truc-tuyen/.+?)">\s*.+?(Kênh.+?)</a>').findall(content)
		for href, title in match:
			addItem(title.strip(), href, 'episodes', '')			
	elif 'fptplay.net' in url:	
		fpt=fptPlay()
			
		b=xread(url)
		if '<div class="title">' in b:
			items=[fpt.detail(i) for i in b.split('list_img') if '<div class="title">' in i]
		elif  '<div class="col-xs-4 col-sm-15 list_img">' in b:
			s=b.split('<div class="col-xs-4 col-sm-15 list_img">')
			items=[fpt.detail(i) for i in s if 'https://fptplay.net/xem-video/' in i]
		else:items=[]
		
		for title,href,img,dir in items:
			if not title:continue
			if dir or 'truyen-van-hoc'  in url or 'truyen-co-tich' in url:
				addItem(title,href,'episodes',img,True)
			else:
				#id=re.search(r'\-([\w]+)\.html', href).group(1)+'?1'
				addItem(title,href,'stream',img,False)			
		return
		pn=xsearch('id="paging_(.+?)_',b)
		if pn:
			pn='type=new&stucture_id=%s&page=2'%pn
			addir_info('[COLOR lime]Page next: %d[/COLOR]'%(page+1),pn,ico,'',mode,page+1,"pageNext",True)

	elif 'vaphim.com' in url:#su dung o phan Goc chia se (Bo suu tap, liveshow, ...)
		body=xread(url)
		if body:
			pattern='<a data=.+?src="(.+?)[\?|\"].+?<h3.+?><a href="(.+?)" rel=.+?>(.+?)</a></h3>'
			for img,href,title in re.findall(pattern,body,re.DOTALL):
				title=vnu(title)				
				title=re.sub('</br>|<br/>|<br />','-',title)
				addItem(title, href, 'folder', img)
			
			if page==0:page=1
			pagelast=xsearch("<span class='pages'>Trang \d{1,4} của (\d{1,4})</span>",body)
			if pagelast and int(pagelast)>page:
				name='%sTrang tiếp theo: trang %d/%s[/COLOR]'%(color['trangtiep'],page+1,pagelast)
				url=url.replace('page/%d'%page, 'page/%d'%(page+1))
				addItem(name, url, 'search_result&page=%d'%(page+1), icon['next'])					
	
	elif 'hdvietnam.com' in url:
		hdvn=hdvietnam()		
		for id,title,href in hdvn.forums(url):
			if id=='pageNext':
				addItem(title, href, 'search_result&page=%d'%(page+1), icon['next'])
			else:
				addItem(title, href, 'episodes', 'http://www.hdvietnam.com/styles/hdvn/hd-vietnam-logo.png')		
	elif 'hdviet.com' in url:
		b=xshare.xread(url)
		body=xsearch('<ul class="cf box-movie-list">(.+?)<div class="box-ribbon mt-15">',b,1,re.DOTALL)

		hdv=hdviet()
		items = hdv.additems(body,mode)	
		for title,href,mode_query,img,isFolder in items:
			addItem(title,href,mode_query,img,isFolder)
		
		return
		if 'search' in mode:			
			s=xsearch('(<ul class="paginglist paginglist-center">.+?</ul>)',b,1,re.DOTALL)
			i=re.search('"active"[^"]+""><a  href="([^"]+)">(\d+)</a>',s)
			if s:
				un=i.group(1);pn=i.group(2);pages=xsearch('>(\d+)</a></li></ul>',s)
				title='%sTrang tiếp theo: trang %s/%s[/COLOR]'%(color['trangtiep'],pn,pages)
				addLink(title, 'hdviet.com', 'search_result&query='+query, icon['next'])
	elif 'hayhaytv' in url:					
		b=re.sub('>\s*<','><',xread(url))		
		p1='<div class="group-title">';p2='<div class="block-base movie">'
		S=' '.join(i for i in b.split(p1) if p2 in i)
		for s in S.split(p2):
			href=xsearch('href="(.+?)"',s)
			img=xsearch('src="(.+?)"',s)
			title=xsearch('alt="(.+?)"',s)
			if [i for i in (href,img,title) if not i]:continue
			eps=re.sub('<strong>','',xsearch('<span class="label-range">(.+?)</strong>',s).strip())
			if not eps:addItem(title,href,'stream',img,False)	
			else:addItem(eps+' '+title,href,'episodes',img)	

		return
		pn=xsearch('<a href="([^"]+?)">Sau</a>',S)
		if pn:
			pages=xsearch('<a href="[^"]+page=(\d+)">Cuối</a>',S)
			name=re.sub('\[COLOR %s.+/COLOR\]'%color['trangtiep'],'',name)
			title=name+color['trangtiep']+' Trang tiep theo...trang %d/%s[/COLOR]'%(page+1,pages)
			if 'http' not in pn:pn='http://www.hayhaytv.vn'+pn
			addir_info(title,pn,ico,'',mode,page+1,query,True)			
	elif 'phimgiaitri' in url:
		content = xshare.make_request(url)			
				
		items = re.compile('<a style=\'text-decoration:none\' href=\'([^\']*).html\'>\s*<img style=.+?src=(.+?) ><table style.+?:0px\'>(.+?)\s*<\/font><br \/><font style.+?#F63\'>(.+?)</font>').findall(content)
		for href,img,namevn,nameen in items:		
			strNameEn, name =  strVnEn(namevn, nameen)	
			href = 'http://phimgiaitri.vn/'+href+'/Tap-1.html'
			addLink(name,href,'stream','http://phimgiaitri.vn/'+img)
		items = re.compile('<a style=\'text-decoration:none\' href=\'([^\']*).html\'>\s*<img style=.+?src=(.+?) ><div class=\'text\'>\s*(.+?)\s*</div><table style.+?:0px\'>(.+?)\s*</font>.+?\'> (.+?)</font>').findall(content)
		for href,img,eps,namevn,nameen in items:		
			name =  namevn + ' - ' + nameen
			if '01/01' in eps : #truong hop phim le o trang chu co hien thi (Tập 01/01)
				href = 'http://phimgiaitri.vn/'+href+'/Tap-1.html'
				addLink(name,href, 'stream','http://phimgiaitri.vn/'+img)					
			else : 
				href = 'http://phimgiaitri.vn/'+href+'/Tap-1.html'
				addItem(name,href,'episodes','http://phimgiaitri.vn/'+img)	
								
        #match = re.compile('<a href="(.+?)">>').findall(content)[0:1]
        #for url in match:
            #addLink('[COLOR lime]Trang tiếp theo[/COLOR]','http://phimgiaitri.vn/'+url.replace(' ','%20'),'search_result',icon['next'])
	elif 'arenavision.in' in url:
		for i in range(30):
			addItem('Arenavision %s (ace)'%(i+1),'av%s'%(str(i+1)),'play_ace','',False)	
			
		for i in range(10):
			addItem('Arenavision S%s (sopcast)'%(i+1),'avs%s'%(str(i+1)),'play_ace','',False)	

#############################################
def play_arena(url,name):
	headers = {"Cookie" : "beget=begetok; has_js=1;"}
	#html = make_request(url,headers=headers,resp='u')
	html = fetch_data(url,headers=headers).text
	match = re.compile('this.loadPlayer\("(.+?)"').findall(html)[0]
	try:
		url='plugin://program.plexus/?mode=1&url=acestream://%s&name=%s'%(match,urllib.quote_plus(name))
	except:
		url='plugin://program.plexus/?mode=1&url=acestream://%s&name=%s'%(match,name.replace(' ','+'))
	xbmc.Player().play(url)
	
def play_arena_sop(url,name):
	headers = {"Cookie" : "beget=begetok; has_js=1;"}
	#html = make_request(url,headers=headers,resp='u')
	html = fetch_data(url,headers=headers).text
	
	match = re.compile('sop://(.+?)"').findall(html)[0]
	url='plugin://program.plexus/?mode=2&url=sop://%s&name=%s'%(match,urllib.quote_plus(name))
	xbmc.Player().play(url)
																		
def Stream(url,link='',subfile=''):
	if '[]' in url:
		arr=url.split('[]')
		url=arr[0];subfile=arr[1]
		
		if '/file/' in subfile:
			fs=fshare()
			link_sub=fs.getLink(subfile,myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'))
			if link_sub:
				ext=os.path.splitext(link_sub)[1][1:].lower()			
				if ext in ['rar','zip','srt','sub','txt','smi','ssa','ass','nfo']:
					subfile=xshare.xshare_download(link_sub)		
	
	if not link:
		if 'vtvgo' in url:
			response = fetch_data(url)
			if not response:link=''
			else:
				cookie=response.cookiestring;
				match = re.search(re.compile(r'vtv\d-(.*?)\.'), url)
				epgid = match.group(1)
				headers = { 
							'User-Agent'		: 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0',
							'Cookie'			: cookie,
							'Referer'			: url,
							'X-Requested-With'	: 'XMLHttpRequest'							
						}
				data={'epg_id':epgid,'type':'1'}
				response = urlfetch.get('http://vtvgo.vn//get-program-channel?epg_id=' +epgid +'&type=1', headers=headers, data=data)
				json_data = json.loads(response.body)
				link = json_data['data']
		elif 'fptplay.net/livetv' in url:
			fpt=fptPlay()
			link=fpt.liveLink(url)
		elif 'fptplay.net' in url:
			link=getlink.get(url)
				
			#fpt=fptPlay()
			#link=fpt.stream(url)						
		elif 'hplus' in url:
			tv=television()
			link=tv.getLink(url)
			
		elif 'htvonline' in url:
			response = fetch_data(url)
			if not response:link=''
			else:
				match = re.search(re.compile(r'setUpPlayer\(\'(.*?)\''), response.body)
				if not match:link=''
				else:link = match.group(1)	
		elif 'chiasenhac' in url:
			content = xread(url)		
			try:
				link = re.compile("\"hd-2\".+?\"([^\"]+)\"").findall(content)[0].replace('%3A',':').replace('%2F','/').replace('%2520','%20')
			except:
				link = re.compile("\"hd-2\".+?\"([^\"]+)\"").findall(content)[-1].replace('%3A',':').replace('%2F','/').replace('%2520','%20')
		elif 'nhaccuatui' in url:
			content = xread(url)
			link = re.compile("title=\".+?\" href=\"([^\"]*)\"").findall(content)[0] 		
		elif 'phimgiaitri' in url:
			try:	
				xbmc.log(url)	
				arr = url.split('/')
				phimid = arr[len(arr) - 3]
				tap = arr[len(arr) - 1]
				tap2 = tap.split('-')
				tap3 = tap2[1].split('.')
				tap = tap3[0]
				url2 = 'http://120.72.85.195/phimgiaitri/mobile/service/getep3.php?phimid=' + phimid
				content = xread(url2)
				content = content[3:]
				infoJson = json.loads(content)
				tapindex = int(tap) -1
				link = infoJson['ep_info'][tapindex]['link']
				link = link.replace('#','*')
				url3 ='http://120.72.85.195/phimgiaitri/mobile/service/getdireclink.php?linkpicasa=' + link
				content = xread(url3)
				content = content[3:]
				linkJson = json.loads(content)
				link = linkJson['linkpi'][0]['link720'] or linkJson['linkpi'][0]['link360']
			except:
				content = xread(url)
				link = re.compile('source src="(.+?)"').findall(content)[-1]
		elif 'megabox.vn' in url:
			#from resources.lib.servers import megabox;
			mgb=megabox()
			link=mgb.getLink(url)											
		elif 'hayhaytv' in url:
			hh=hayhayvn()
			for href,label in hh.getLink(url):
				link=test_link(href)
				if link:break			
		elif 'hdviet.com' in url:		
			if os.path.isfile(xshare.joinpath(datapath,'hdviet.cookie')):os.remove(xshare.joinpath(datapath,'hdviet.cookie'))
				
			hdv=hdviet()
			url = url.split('|')[1]
			link,subfile=hdv.getResolvedUrl(url)
			if subfile:
				subfile = xshare.xshare_download(subfile)		
		elif 'phimmoi.net' in url:
			pm=phimmoi()
			link=pm.getLink(url)											
		elif 'phimnhanh.com' in url:
			pn=phimnhanh()
			link=pn.getLink(url)									
		elif 'hdonline.vn' in url:
			link,subfile=getlink.get(url)
			if subfile:
				subfile = xshare.xshare_download(subfile)				
		elif 'fshare.vn' in url:				
			fs=fshare()
			link=fs.getLink(url,myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'))
			if link:
				ext=os.path.splitext(link)[1][1:].lower()			
				if ext in ['rar','zip','srt','sub','txt','smi','ssa','ass','nfo']:
					result=xshare.xshare_download(link);return ''
				elif '.xml' in link:return link
				
				url=link
				#print url;return
				urltitle=urllib.unquote(os.path.splitext(os.path.basename(url))[0]).lower()
				urltitle='.'+'.'.join(s for s in re.sub('_|\W+',' ',re.split('\d\d\d\d',urltitle)[0]).split())+'.'

				subfile='';items=[]
				for file in os.listdir(subsfolder):
					filefullpath=xshare.joinpath(subsfolder,file).encode('utf-8')
					filename=re.sub('vie\.|eng\.','',os.path.splitext(file)[0].lower().encode('utf-8'))
					filename=re.split('\d\d\d\d',filename)[0];count=0
					for word in re.sub('_|\W+',' ',filename).split():
						if '.%s.'%word in urltitle:count+=1
					if count:items.append((count,filefullpath))
				for item in items:
					if item[0]>=count:count=item[0];subfile=item[1]

		elif 'youtube.com' in url:					
			link = url.replace('https://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/?action=play_video&videoid=')
		elif 'sop://' in url or 'acestream://' in url:
			if False:#p2p-streams
				if 'sop://' in url:
					link = 'plugin://plugin.video.p2p-streams/?mode=2&url=%s&name=%s'%(url,urllib.quote_plus(name)) 
				else:
					link = 'plugin://plugin.video.p2p-streams/?mode=1&url=%s&name=%s'%(url,urllib.quote_plus(name))
			else:
				if 'sop://' in url:
					link = 'plugin://program.plexus/?mode=2&url=%s&name=%s'%(url,urllib.quote_plus(name)) 
				else:
					link = 'plugin://program.plexus/?mode=1&url=%s&name=%s'%(url,urllib.quote_plus(name))

			item=xbmcgui.ListItem(path=link)
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)	
					
			return 'no'	
		else:
			link = url					
		if link is None or len(link) == 0:
			notify('Lỗi không lấy được link phim.');return
	
	if img:item=xbmcgui.ListItem(path=link, iconImage=img, thumbnailImage=img)
	else:item=xbmcgui.ListItem(path=link)
		
	if 'fshare' in link:item.setInfo('video', {'Title':urllib.unquote(os.path.basename(link))})	
	else:item.setInfo('video', {'Title':name})
	
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)	
	
	if not subfile and myaddon.getSetting('advertisement') == 'false':
		subfile=decode('ROOT', 'usPDxIx-frezvcPDtMTCvMG_fbfBvH6slJySgw==')+'quangcao.srt'
		subfile=xshare.xshare_download(subfile)
	if subfile:xbmc.sleep(2000);xbmc.Player().setSubtitles(subfile)	
		
	return

def database_download(datapath,check_file):
	file=os.path.join(datapath,check_file)
	if not os.path.isfile(file):
		notify(u'Đang kiểm tra và tải dữ liệu');xshare.delete_files(tempfolder)
		tempfile = os.path.join(tempfolder,"data.zip")
		href=decode('ROOT', 'usPDxIx-frezvcPDtMTCvMG_fbfBvH6slJySgw==')+'icon.zip'
		response=xshare.make_request(href,resp='o',maxr=3)
		if response.status==200:
			body=makerequest(tempfile,response.body,'wb');xbmc.sleep(1000)
			datapath=xbmc.translatePath(myaddon.getAddonInfo('profile'))
			try:
				xbmc.executebuiltin('XBMC.Extract("%s","%s")'%(tempfile,datapath), True)
				makerequest(joinpath(datapath,file),'','w')
				notify(u'Tải dữ liệu thành công')				
			except:notify(u'Tải dữ liệu lỗi!')			
		else:notify(u'Tải dữ liệu không thành công!')
	
def auto_update():
	if checkupdate('last_update.dat',17,datapath):
		for query in ['phim-le','phim-bo']:
			v_query='Phim lẻ' if query=='phim-le' else 'Phim bộ'
			
			filecheck='2@%s_movie.dat'%query
			filedownload='2@%s_movie.zip'%query
			filename='2@%s_movie.xml'%query			
			count_old=len(doc_xml(xshare.joinpath(datapath,filename)))
			
			notify(u'Đang cập nhật dữ liệu...',v_query,timeout=5000)
			tempfile = os.path.join(tempfolder,filedownload)		
			href=decode('ROOT', 'usPDxIx-frezvcPDtMTCvMG_fbfBvH6slJySgw==')+filedownload
			response=xshare.make_request(href,resp='o',maxr=3)
			if response.status==200:
				body=makerequest(tempfile,response.body,'wb');xbmc.sleep(1000)
				try:					
					xbmc.executebuiltin('XBMC.Extract("%s","%s")'%(tempfile,datapath), True)
					count_new=len(doc_xml(xshare.joinpath(datapath,filename)))
					if count_new>count_old:
						notify(u'Đã cập nhật được %d phim'%(count_new-count_old),v_query,timeout=2000)
					else:notify(u'Không có phim mới...',v_query,timeout=2000)
					makerequest(joinpath(datapath,"last_update.dat"),'','w')
				except:notify(u'Đã xảy ra lỗi cập nhật!',v_query,timeout=2000)
			else:notify(u'Cập nhật dữ liệu không thành công!',v_query)
							
#__author__ = 'thaitni' -> thanks you!
def checkupdate(filename,hours=1,folder=datapath,xdict=dict()):
	filecheck=xshare.joinpath(folder,filename);timeformat='%Y%m%d%H'
	filetime=os.path.getmtime(filecheck) if os.path.isfile(filecheck) else 0
	last_update=datetime.datetime.fromtimestamp(filetime).strftime(timeformat)
	timenow=datetime.datetime.now().strftime(timeformat)
	#if int(timenow)-int(last_update)>hours:
	#	xshare_dict=json_rw('xshare.json');file_time=xshare_dict.get(filename,'0')
	#	if timenow > file_time:xshare_dict[filename]=timenow;json_rw('xshare.json',xshare_dict);result=True
	return (int(timenow)-int(last_update))>hours
	
def xread(url,hd={'User-Agent':'Mozilla/5.0'},data=None):
	req=urllib2.Request(url,data,hd)
	try:res=urllib2.urlopen(req, timeout=20);b=res.read();res.close()
	except:b=''
	return b
	
def makerequest(file,body='',attr='r'):
	file=xshare.s2u(file)
	if attr=='r':
		try:f=open(file);body=f.read();f.close()
		except:body=''
	else:
		try:f=open(file,attr);f.write(body);f.close()
		except:notify(u'Lỗi ghi file: %s!'%xshare.s2u(os.path.basename(file)));body=''
	return body
#__author__ = 'thaitni'	
		
def addLink(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&img="+urllib.quote_plus(iconimage)
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name})
	liz.setProperty('mimetype', 'video/x-msvideo')
	liz.setProperty("IsPlayable","true")
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
	return ok
	
def addItem(name,url,mode,iconimage,isFolder=True, info={}, art={}, menu={}):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&img="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	if not info:info={ "Title": name }
	liz.setInfo("video", info)	
	if art:liz.setArt(art)#{"thumb":iconimage,"poster":iconimage,"fanart":iconimage}	
	if ('www.youtube.com/user/' in url) or ('www.youtube.com/channel/' in url):
		u = 'plugin://plugin.video.youtube/%s/%s/' % (url.split( '/' )[-2], url.split( '/' )[-1])
		ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
		return ok		
	if ('plugin://' in url):u = url
	liz.setProperty("isPlayable", isFolder and "false" or "true")
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
	return ok
	
def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param
### ------------
try:
	myfolder=xshare.s2u(myaddon.getSetting('thumuccucbo'))
	if not os.path.exists(myfolder):myfolder=xshare.joinpath(datapath,'myfolder')
except:myfolder=xshare.joinpath(datapath,'myfolder')
subsfolder=xshare.joinpath(tempfolder,'subs')
params=get_params();page=0;temp=[];mode=url=name=fanart=img=date=query=action=end=text=''

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:img=urllib.unquote_plus(params["img"])
except:pass
try:fanart=urllib.unquote_plus(params["fanart"])
except:pass
try:mode=str(params["mode"])
except:pass
try:page=int(params["page"])
except:pass
try:query=urllib.unquote_plus(params["query"])
except:pass#urllib.unquote

### ------------
#print "Main---------- Mode: "+str(mode),"URL: "+str(url),"Name: "+str(name),"query: "+str(query),"page: "+str(page),"img: "+str(img)
if not mode:
	datafolder=xbmc.translatePath(myaddon.getAddonInfo('profile'))	
	
	for folder in (datafolder,datapath,iconpath,myfolder,subsfolder):
		if not os.path.exists(folder):os.mkdir(folder)
	xmlheader='<?xml version="1.0" encoding="utf-8">\n';p=datapath;q=myfolder
	for i in [(p,'search.xml'),(q,'mylist.xml')]:
		file=xshare.joinpath(i[0],i[1])
		if not os.path.isfile(file):makerequest(file,xmlheader,'w')
				
	file_check = Home(url,query)				
	xbmcplugin.endOfDirectory(int(sys.argv[1]))				
	
	database_download(datapath,file_check.split('[]')[0])					

	file=os.path.join(datapath,file_check.split('[]')[1])	
	if checkupdate('auto_update.dat',5,datapath) and not os.path.isfile(file):
		makerequest(joinpath(datapath,file),'','w')
		makerequest(joinpath(datapath,"auto_update.dat"),'','w')
		auto_update();xshare.delete_files(tempfolder)		
	

	#hdonline:348/142 - megabox:120/20 - phimmoi: 85 - pn:504 - vp:222
	
	#DownloadDB2('phim-le',page=1,page_max=1)
	
	#DownloadDB('phim-le','vaphim',1,222,False)
	#UpdateDB('phim-bo','megabox',1)
		
	if False:		
		page_max=2	
		while page_max > 0:
			for s in ['megabox', 'hdonline']:#, 'phimnhanh', 'fsharefilm']:				
				notify(u'%s / %d '%(s,page_max))
				DownloadDB('phim-bo',s,page_max,page_max,False);
				#UpdateDB('phim-bo',s,page_max)
			page_max-=1	
								
elif mode == 'home':Home(url,query)
elif mode == 'tags':Tags(url,query)
elif mode == 'tags-movie':TagsMovie(url,query)
elif mode == 'index':Index(url,name,query,page)
elif mode == 'category':Category(url,name,query,page)
elif mode == 'episodes' or mode == 'folder':episodes(url, name, page)
elif mode == 'xml':doc_list_xml(url,page)
elif mode == 'local':Local(name,url,img,fanart,mode,query)
elif mode == 'remote':Remote(name,url,img,mode,page,query)
elif mode == 'search':end=Search(url)
elif mode == 'search_result':
	v_query='Phim lẻ' if query=='phim-le' else 'Phim bộ'
	if 'movie.xml' not in url:
		server = re.sub('\[.*?]','',name.lower())
		if server in ['megabox', 'hdonline', 'phimmoi', 'phimnhanh', 'fsharefilm', 'vaphim']:
			filecheck=url.replace('xml','dat')
			file=os.path.join(datapath,url)
			if (checkupdate(filecheck,12,datapath) or not os.path.isfile(file)):# and False:
				makerequest(xshare.joinpath(datapath,filecheck),'','w')
				notify(u'Đang cập nhật dữ liệu...',u'%s - %s'%(v_query,eval("www['"+server+"']")),timeout=5000)
				DownloadDB(query,server,1,1)
			
	Result(url, mode, query, page)
elif mode == 'stream':end=Stream(url)
elif mode == 'play':Stream(url,link=url)
elif mode == 'play_ace':
    url='http://arenavision.in/'+url
    try:
        play_arena_sop(url,name)
    except:
        play_arena(url,name)

elif 'serverlist' in mode:ServerList(name, url, mode, page, query, img)	
elif mode == 'setting':myaddon.openSettings();end='ok'

try:	
	if not mode and not query:	
		xbmc.executebuiltin('Container.SetViewMode(500)')# Thumbnails		
	elif '2@phim-' in url:
		xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
		xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
		#xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
		xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)	
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		#xbmc.executebuiltin('Container.SetViewMode(504)')# Media info
except:pass	
	
if not end or end not in 'no-ok-fail':xbmcplugin.endOfDirectory(int(sys.argv[1]))
#truyen hinh xem lai
#ca nhac