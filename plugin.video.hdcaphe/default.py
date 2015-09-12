#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib, urllib2, json, re, urlparse, sys, time, os, hashlib
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from BeautifulSoup import BeautifulSoup

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

my_addon = xbmcaddon.Addon()
subtitle_lang = my_addon.getSetting('subtitle')
video_quality = my_addon.getSetting('video_quality')
use_vi_audio = my_addon.getSetting('useViAudio') == 'true'
use_dolby_audio = my_addon.getSetting('useDolbyAudio') == 'true'
reload(sys);

fixed_quality = (video_quality != 'Chọn khi xem')

min_width = {'SD' : 0, 'HD' : 1024, 'Full HD' : 1366}
max_width = {'SD' : 1024, 'HD' : 1366, 'Full HD' : 10000}

header_web = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
			'Content-type': 'application/x-www-form-urlencoded',
			'Referer' : 'http://www.google.com'}
header_app = {'User-agent' : 'com.hdviet.app.ios.HDViet/2.0.1 (unknown, iPhone OS 8.2, iPad, Scale/2.000000)'}

def make_request(url, params=None, headers=None):
	if headers is None:
		headers = header_web
	try:
		if params is not None:
			params = urllib.urlencode(params)
		req = urllib2.Request(url,params,headers)
		f = urllib2.urlopen(req)
		body=f.read()
		f.close()
		return body
	except:
		pass
def login():
	#username = my_addon.getSetting('userhdviet')
	username = "tk.hdviet.com@gmail.com"
	#password = my_addon.getSetting('passhdviet')
	password = "hdviet.com"
	if len(username) < 5 or len(password) < 1:
		my_addon.setSetting("token", "none")
		xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s)'%('HDViet','[COLOR red]Log in Failed ![/COLOR]',2000)).encode("utf-8"))
		return "fail"
	h = hashlib.md5()
	h.update(password)
	passwordhash = h.hexdigest()
	result = make_request('https://api-v2.hdviet.com/user/login?email=%s&password=%s' % (username,passwordhash), None, header_app)
	if "AccessTokenKey" in result:
		res = json.loads(result)["r"]
		my_addon.setSetting("token", res["AccessTokenKey"])
		#xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s)'%('HDViet','[COLOR green]Logged in ![/COLOR]',2000)).encode("utf-8"))
		return res["AccessTokenKey"];
	else:
		#xbmcgui.Dialog().ok("HDViet", passwordhash)
		my_addon.setSetting("token", "none")
		#xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s)'%('HDViet','[COLOR red]Log in Failed ![/COLOR]',2000)).encode("utf-8"))
		return "fail"
def convert_vi_to_en(str):
	try:
		if str == '': return
		if type(str).__name__ == 'unicode': str = str.encode('utf-8')
		list_pat = ["á|à|ả|ạ|ã|â|ấ|ầ|ẩ|ậ|ẫ|ă|ắ|ằ|ẳ|ặ|ẵ", "Á|À|Ả|Ạ|Ã|Â|Ấ|Ầ|Ẩ|Ậ|Ẫ|Ă|Ắ|Ằ|Ẳ|Ặ|Ẵ",
					"đ", "Đ", "í|ì|ỉ|ị|ĩ", "Í|Ì|Ỉ|Ị|Ĩ", "é|è|ẻ|ẹ|ẽ|ê|ế|ề|ể|ệ|ễ", "É|È|Ẻ|Ẹ|Ẽ|Ê|Ế|Ề|Ể|Ệ|Ễ",
					"ó|ò|ỏ|ọ|õ|ô|ố|ồ|ổ|ộ|ỗ|ơ|ớ|ờ|ở|ợ|ỡ", "Ó|Ò|Ỏ|Ọ|Õ|Ô|Ố|Ồ|Ổ|Ộ|Ỗ|Ơ|Ớ|Ờ|Ở|Ợ|Ỡ",
					"ú|ù|ủ|ụ|ũ|ư|ứ|ừ|ử|ự|ữ", "Ú|Ù|Ủ|Ụ|Ũ|Ư|Ứ|Ừ|Ử|Ự|Ữ", "ý|ỳ|ỷ|ỵ|ỹ", "Ý|Ỳ|Ỷ|Ỵ|Ỹ"]
		list_re = ['a', 'A', 'd', 'D', 'i', 'I', 'e', 'E', 'o', 'O', 'u', 'U', 'y', 'Y']
		for i in range(len(list_pat)):
			str = re.sub(list_pat[i], list_re[i], str)
		return str.replace(' ', '-')
	except:
		traceback.print_exc()


def get_movies_from_html(html):
	soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)

	number_of_pages = 1

	# number of pages
	pages = soup.find('ul', 'paginglist')
	if (pages):
		pages = pages.findAll('a')
		number_of_pages = int(pages[len(pages) - 1].string)

	# movies
	movies = []
	items = soup.find(attrs = 'box-movie-list')
	items = items.findAll('li', 'mov-item')

	for item in items:
		movie = {}
		movie['id'] = item.find('div', 'tooltipthumb2').get('href').replace('#tooltip', '')
		movie['title'] = item.find('a', 'mv-namevn').get('title')
		movie['thumbnail'] = item.img.get('src').replace('124x184', 'origins')
		movie['plot'] = item.find('span', 'cot1').string
		
		eps = item.find('span', 'labelchap2')
		
		if (eps):
			movie['eps'] = int(eps.string)
		else:
			movie['eps'] = 0

		if movie['title'].startswith('Phim '):
			movie['title'] = movie['title'].replace('Phim ', '')

		movies.append(movie)

	return movies, number_of_pages

def main_menu():
	addDir('Tìm Kiếm', {'mode':'search'}, '', '')
	addDir('Phim hot trong tháng', {'mode':'movies_from_url', 'url':'http://movies.hdviet.com/phim-hot-trong-thang/trang-1.html', 'page':'1'}, '', '')
	addDir('Phim Lẻ', {'mode':'sub_menu', 'type': '0'}, '', '')
	addDir('Phim Bộ', {'mode':'sub_menu', 'type': '1'}, '', '')

def sub_menu(movie_type):
	soup = BeautifulSoup(make_request('http://movies.hdviet.com/'))
	
	menus = []
	
	if movie_type == '0':
		menus = soup.find(id = 'menu-phimle')
	else:
		menus = soup.find(id = 'menu-phimbo')
	
	menus = menus.findAll('a')
	first_item = True
	parrent_group = '';
	for item in menus:
		if first_item == True:
			addDir(u'Tất cả', {'mode':'movies_from_url', 'url':item.get('href').replace('.html', '/trang-1.html'), 'page':'1'}, '', '')
			first_item = False
		else:
			group_name = item.string.strip()
			if item.parent.get('class') == 'childcols2':
				addDir('%s - %s' % (parrent_group, group_name), {'mode':'movies_from_url', 'url':item.get('href').replace('.html', '/trang-1.html'), 'page':'1'}, '', '')
			else:
				addDir(group_name, {'mode':'movies_from_url', 'url':item.get('href').replace('.html', '/trang-1.html'), 'page':'1'}, '', '')
				parrent_group = group_name

def search():
	query = ''
	try:
		keyboard = xbmc.Keyboard('', '')
		keyboard.doModal()
		if (keyboard.isConfirmed()):
			query = keyboard.getText()
	except:
		pass

	if query != '':
		movies_from_url('http://movies.hdviet.com/tim-kiem.html?keyword=%s&page=1' % urllib.quote(query, ''), '1')

def get_movie_info(movie_id):
	result = json.loads(make_request('https://api-v2.hdviet.com/movie?ep=1&movieid=%s&sign=sign&sequence=0' % movie_id, None, header_app))
	return result['r']

def movies_from_url(url, page):
	page = int(page)
	
	url = re.sub(r'trang-\d+\.html', 'trang-%d.html' % page, url)
	url = re.sub(r'page=\d+', 'page=%d' % page, url)
	
	html = make_request(url)

	movies, number_of_pages = get_movies_from_html(html)
	items = []
	if (page > 1):
		addDir('Trang Trước', {'mode':'movies_from_url', 'url':url, 'page':page - 1}, '', '')

	for movie in movies:
		if (movie['eps'] == 0):
			if fixed_quality:
				addMovie(movie['title'], {'mode':'play', 'movie_id' : movie['id'], 'ep' : '1'}, movie['thumbnail'], movie['plot'])
			else:
				addDir(movie['title'], {'mode':'play', 'movie_id' : movie['id'], 'ep' : '1'}, movie['thumbnail'], movie['plot'])
		else:
			addDir(movie['title'], {'mode':'movie_detail', 'movie_id' : movie['id']}, movie['thumbnail'], movie['plot'])

	if page < number_of_pages:
		addDir('Trang Sau', {'mode':'movies_from_url', 'url':url, 'page':page + 1}, '', '')


def movie_detail(movie_id):
	movie_info = get_movie_info(movie_id)

	if movie_info['Episode'] == '0':
		# single ep
		if fixed_quality:
			addMovie('%s - %s' % (movie_info['KnownAs'], movie_info['MovieName']), {'mode':'play', 'movie_id' : movie_id, 'ep' : '1'}, movie_info['Poster'], movie_info['PlotVI'])
		else:
			addDir('%s - %s' % (movie_info['KnownAs'], movie_info['MovieName']), {'mode':'play', 'movie_id' : movie_id, 'ep' : '1'}, movie_info['Poster'], movie_info['PlotVI'])
	else:
		for  i in range (1, int(movie_info['Sequence']) + 1):
			if fixed_quality:
				addMovie(u'%s - %s - Tập %d' % (movie_info['KnownAs'], movie_info['MovieName'], i), {'mode':'play', 'movie_id' : movie_id, 'ep' : i}, movie_info['Poster'], movie_info['PlotVI'])
			else:
				addDir(u'%s - %s - Tập %d' % (movie_info['KnownAs'], movie_info['MovieName'], i), {'mode':'play', 'movie_id' : movie_id, 'ep' : i}, movie_info['Poster'], movie_info['PlotVI'])
	


def play(movie_id, ep = 0):
	token = my_addon.getSetting('token')
	# get link to play and subtitle
	if token == 'none': token = login()
	if token == 'fail': return
	res = make_request('https://api-v2.hdviet.com/movie/play?movieid=%s&accesstokenkey=%s&ep=%s' % (movie_id, token, ep), None, header_app)
	if "0000000000" in res:
		token = login()
		if token != 'fail': res = make_request('https://api-v2.hdviet.com/movie/play?movieid=%s&accesstokenkey=%s&ep=%s' % (movie_id, token, ep), None, header_app)
		
	movie = json.loads(res)["r"]
	if movie:
		subtitle_url = ''
		if subtitle_lang != 'Tắt':
			try:
				subtitle_url = movie['Subtitle'][subtitle_lang]['Source']
				if subtitle_url == '':
					subtitle_url = movie['SubtitleExt'][subtitle_lang]['Source']
				if subtitle_url == '':
					subtitle_url = movie['SubtitleExtSe'][subtitle_lang]['Source']
			except:
				pass

		# get link and resolution
		#link_to_play = re.sub(r'_\d+_\d+_', '_320_4096_', movie['LinkPlay'])
		link_to_play = movie['LinkPlay']
		result = make_request(link_to_play, None, header_app)

		# audioindex
		audio_index = 0
		if (use_vi_audio and movie['Audio'] > 0) or (movie['Audio'] == 0 and use_dolby_audio):
			audio_index = 1
		
		playable_items = []
		lines = result.splitlines()

		i = 0
		# find the first meaning line
		while (i < len(lines)):
			if 'RESOLUTION=' in lines[i]:
				break
			i += 1
		while (i < len(lines)):
			playable_item = {}
			playable_item['res'] = lines[i][lines[i].index('RESOLUTION=') + 11:]

			if lines[i + 1].startswith('http'):
				playable_item['url'] = lines[i + 1]
			else:
				playable_item['url'] = movie['LinkPlay'].replace('playlist.m3u8', lines[i + 1])

			playable_items.append(playable_item)
			i += 2

		if not fixed_quality:
			for item in playable_items:
				addMovie(item['res'], {'mode':'play_url', 'stream_url' : '%s?audioindex=%d' % (item['url'], audio_index), 'subtitle_url' : subtitle_url}, '', '')
		else:
			i = len(playable_items) - 1
			while (i >= 0):
				current_width = int(playable_items[i]['res'].split('x')[0])
				if (min_width[video_quality] <= current_width and max_width[video_quality] > current_width) or current_width < min_width[video_quality]:
					break
				i -= 1

			if i >= 0:
				set_resolved_url('%s?audioindex=%d' % (playable_items[i]['url'], audio_index), subtitle_url)

	
def set_resolved_url(stream_url, subtitle_url):
	h1 = '|User-Agent=' + urllib.quote_plus('HDViet/2.0.1 CFNetwork/711.2.23 Darwin/14.0.0')
	h2 = '&Accept=' + urllib.quote_plus('*/*')
	h3 = '&Accept-Language=' + urllib.quote_plus('en-us')
	h4 = '&Connection=' + urllib.quote_plus('Keep-Alive')
	h5 = '&Accept-Encoding=' + urllib.quote_plus('gzip, deflate')
	xbmcplugin.setResolvedUrl(addon_handle, succeeded=True, listitem=xbmcgui.ListItem(label = '', path = stream_url + h1 + h2 + h3 + h5))
	player = xbmc.Player()
	
	subtitlePath = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')).decode("utf-8")
	subfile = xbmc.translatePath(os.path.join(subtitlePath, "temp.sub"))
	try:
		if os.path.exists(subfile):
			os.remove(subfile)
		f = urllib2.urlopen(subtitle_url)
		with open(subfile, "wb") as code:
			code.write(f.read())
		xbmc.sleep(3000)
		xbmc.Player().setSubtitles(subfile)
	except:
		pass
	
	for _ in xrange(30):
		if player.isPlaying():
			break
		time.sleep(1)
	else:
		raise Exception('No video playing. Aborted after 30 seconds.')

	
def build_url(query):
	return base_url + '?' + urllib.urlencode(query)


def addDir(name,query,iconimage, plot):
	addItem(name, query, iconimage, plot, True)
	
def addMovie(name,query,iconimage, plot):
	addItem(name, query, iconimage, plot, False)
	
def addItem(name,query,iconimage, plot, isFolder):
	u=build_url(query)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={"Title": name, "Plot" : plot} )
	if not isFolder:
		liz.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=liz,isFolder=isFolder)
	return ok

mode = args.get('mode', None)

if mode is None:
	main_menu()
elif mode[0] == 'sub_menu':
	type = args.get('type', None)
	sub_menu(type[0])
elif mode[0] == 'movies_from_url':
	url = args.get('url', None)
	page = args.get('page', None)
	movies_from_url(url[0], page[0])
elif mode[0] == 'movie_detail':
	movie_detail(args.get('movie_id', None)[0])
elif mode[0] == 'play':
	play(args.get('movie_id', None)[0], args.get('ep', None)[0])
elif mode[0] == 'play_url':
	set_resolved_url(args.get('stream_url', None)[0], args.get('subtitle_url', None)[0])
elif mode[0] == 'search':
	search()
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))