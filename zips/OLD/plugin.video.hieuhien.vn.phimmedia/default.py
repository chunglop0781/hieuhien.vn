#!/usr/bin/env python
# -*- coding: utf-8 -*-

# V137: 2017-07-14

import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import json, os, re, requests, sys, urllib, urllib2
import HTMLParser
from bs4        import BeautifulSoup
from bs4        import SoupStrainer
html_parser = HTMLParser.HTMLParser()

# TEMP CODE: #########################################################
#
#
#
# TOGGLES ADDONS UPDATE ON
if not xbmc.getInfoLabel('Skin.String(Flag)'):
	j = json.loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "Settings.GetSettingValue", "params": {"setting": "general.addonupdates"}}'))
	addonupdates = str(j['result']['value'])
	if not addonupdates == '0':
		xbmc.executeJSONRPC('{"jsonrpc": "2.0", "id": 1, "method": "Settings.SetSettingValue", "params": {"setting": "general.addonupdates", "value": 0}}')
#
#
#
#
# TEMP CODE: #########################################################

addonId      = 'plugin.video.hieuhien.vn.phimmedia'
addon        = xbmcaddon.Addon(addonId)
addonDir     = xbmc.translatePath(addon.getAddonInfo('path'))
userdir      = xbmc.translatePath(addon.getAddonInfo('profile'))
dir_py       = os.path.join(addonDir, 'py/')
www_py       = 'https://v137.xyz/py/v137/'+addonId+'/?py='
agent        = 'V137'
icon         = os.path.join(addonDir, 'icon.png')
fanart       = 'https://v137.xyz/py/v137/img/phimmedia_01.jpg'
addonHandle  = int(sys.argv[1])
skin_used    = xbmc.getSkinDir()
domain       = 'http://www.phim.media/'
maxhistory   = 25
maxres       = 4
resolution   = {4:'1080', 3:'720', 2:'540', 1:'480', 0:'360'}

icons         = {
 'alpha'      : 'https://github.com/google/material-design-icons/raw/master/av/drawable-xxxhdpi/ic_sort_by_alpha_white_48dp.png',
 'compass'    : 'https://github.com/google/material-design-icons/raw/master/action/drawable-xxxhdpi/ic_explore_white_48dp.png',
 'genres'     : 'https://github.com/google/material-design-icons/raw/master/action/drawable-xxxhdpi/ic_class_white_48dp.png',
 'globe'      : 'https://github.com/google/material-design-icons/raw/master/action/drawable-xxxhdpi/ic_language_white_48dp.png',
 'hd'         : 'https://github.com/google/material-design-icons/raw/master/av/drawable-xxxhdpi/ic_hd_white_48dp.png',
 'history'    : 'https://github.com/google/material-design-icons/raw/master/action/drawable-xxxhdpi/ic_history_white_48dp.png',
 'hot'        : 'https://github.com/google/material-design-icons/raw/master/social/drawable-xxxhdpi/ic_whatshot_white_48dp.png',
 'intheatres' : 'https://github.com/google/material-design-icons/raw/master/action/drawable-xxxhdpi/ic_theaters_white_48dp.png',
 'language'       : 'https://github.com/google/material-design-icons/raw/master/communication/drawable-xxxhdpi/ic_chat_white_48dp.png',
 'movies'     : 'https://github.com/google/material-design-icons/raw/master/image/drawable-xxxhdpi/ic_movie_creation_white_48dp.png',
 'new'        : 'https://github.com/google/material-design-icons/raw/master/av/drawable-xxxhdpi/ic_fiber_new_white_48dp.png',
 'nextpage'   : 'https://github.com/google/material-design-icons/raw/master/navigation/drawable-xxxhdpi/ic_last_page_white_48dp.png',
 'pinwheel'   : 'https://github.com/google/material-design-icons/raw/master/hardware/drawable-xxxhdpi/ic_toys_white_48dp.png',
 'popular'    : 'https://github.com/google/material-design-icons/raw/master/image/drawable-xxxhdpi/ic_remove_red_eye_white_48dp.png',
 'search'     : 'https://github.com/google/material-design-icons/raw/master/action/drawable-xxxhdpi/ic_search_white_48dp.png',
 'series'     : 'https://github.com/google/material-design-icons/raw/master/image/drawable-xxxhdpi/ic_movie_filter_white_48dp.png',
 'settings'   : 'https://github.com/google/material-design-icons/raw/master/action/drawable-xxxhdpi/ic_settings_white_48dp.png',
 'sofa'       : 'https://github.com/google/material-design-icons/raw/master/content/drawable-xxxhdpi/ic_weekend_white_48dp.png',
 'star'       : 'https://github.com/google/material-design-icons/raw/master/toggle/drawable-xxxhdpi/ic_star_white_48dp.png',
 'thumbup'    : 'https://github.com/google/material-design-icons/raw/master/action/drawable-xxxhdpi/ic_thumb_up_white_48dp.png',
 'warning'    : 'https://github.com/google/material-design-icons/raw/master/alert/drawable-xxxhdpi/ic_warning_white_48dp.png'
}

# ##################################################################################### #

if not os.path.isdir(userdir):
	prompt = xbmcgui.Dialog().yesno('Chọn / Choose:','Chọn cách hiển thị danh sách phim?','How would you like to display movies?','','Kiểu danh sách','Kiểu Poster')
	if prompt:
		addon.setSetting('view_mode', '1')
	else:
		addon.setSetting('view_mode', '0')

if xbmc.getSkinDir() == 'skin.estuary':
	wideview = '55'
elif xbmc.getSkinDir() == 'skin.heidi':
	wideview = '52'
else:
	wideview = '50'

view_mode = str(addon.getSetting('view_mode'))

if view_mode == '1':
	if xbmc.getSkinDir() == 'skin.estuary':
		viewmode = '500'
	elif xbmc.getSkinDir() == 'skin.heidi':
		viewmode = '53'
	else:
		viewmode = '50'
else:
	viewmode = wideview
contenttype = 'Movies'


# ##################################################################################### #

# GET OS FLAGS
#Android     = xbmc.getCondVisibility("System.Platform.Android")
#Windows     = xbmc.getCondVisibility("System.Platform.Windows")

# SELECT OFFLINE / ONLINE MODE
#if Windows:
#	online = False
#else:
#	online = True

# ONLINE INDEXERS AND RESOLVERS
#if online:
#	if Android: # Android OS compatibility for URLIMPORT
#		if not os.path.exists(xbmc.translatePath('special://home/temp/urlimport')):
#			os.makedirs(xbmc.translatePath('special://home/temp/urlimport'))
#		os.environ['TMPDIR'] = xbmc.translatePath('special://home/temp/urlimport')
#	from resources.urlimport import urlimport
#	from datetime import timedelta
#	sys.path.append(www_py)
#	urlimport.config(
#		**{
#			'debug': 0,
#			'no_cache': False,
#			'cache_time': timedelta(0,3600), # 1 hour = 0 days and 3600 seconds
#			'cache_dir': dir_py,
#			'user_agent': agent, 
#		}
#	)
#	sys.path_importer_cache.clear()

# OFFLINE INDEXERS AND RESOLVERS
#else:
#	sys.path.append(dir_py)

#import unicodefix

# ##################################################################################### #

def Home():
	AddDir('[COLOR orangered][B][ Tìm Kiếm ][/B][/COLOR]', domain + 'index.php?keyword=%s&do=phim&act=search', 'history', icons['search'])
	AddDir('[COLOR white][B]Phim đề cử[/B][/COLOR]', domain + 'phim-moi/', 'index', icons['thumbup'])
	AddDir('[COLOR white][B]Phim lẻ mới[/B][/COLOR]', domain + 'phim-le/', 'index', icons['new'])
	AddDir('[COLOR white][B]Phim bộ mới[/B][/COLOR]', domain + 'phim-bo/', 'index', icons['new'])
	AddDir('[COLOR white][B]Top xem nhiều trong ngày[/B][/COLOR]', '0', 'top', icons['hot'])
	AddDir('[COLOR white][B]Top xem nhiều trong tuần[/B][/COLOR]', '1', 'top', icons['hot'])
	AddDir('[COLOR white][B]Top xem nhiều trong tháng[/B][/COLOR]', '2', 'top', icons['hot'])
	AddDir('[COLOR orangered][B]+ Thể loại[/B][/COLOR]', '0', 'submenu', icons['genres'])
	AddDir('[COLOR orangered][B]+ Quốc gia[/B][/COLOR]', '1', 'submenu', icons['globe'])
	AddDir('[COLOR orangered][B]+ Phim lẻ theo năm[/B][/COLOR]', '2', 'submenu', icons['movies'])
	AddDir('[COLOR orangered][B]+ Phim bộ theo năm[/B][/COLOR]', '3', 'submenu', icons['series'])
	AddDir('[COLOR orangered][B]+ Phim tiếng Việt[/B][/COLOR]', '4', 'submenu', icons['language'])
	AddDir('[COLOR white][B]Cài đặt[/B][/COLOR]', '', 'settings', icons['settings'])
	EndDir()
	xbmc.executebuiltin('Container.SetViewMode(50)')

def SubMenu(url):
	print('| SubMenu | %s' % url)
	html = GetUrl(domain, domain)
	menu = re.compile(u'<ul role="menu" class="dropdown-menu">(.+?)</ul>').findall(html)[int(url)]
	items = re.compile(u'<a href="(.+?)">([^<]*)<').findall(menu)
	for link, name in items:
		link = link.replace(domain, '')
		link = domain + urllib.quote(link)
		try:
			AddDir('[COLOR white]' + name + '[/COLOR]', link, 'index', icon)
		except:
			pass
	EndDir()
	xbmc.executebuiltin('Container.SetViewMode(50)')

def Top(url):
	if url == '0':
		period = 'topviewday'
	elif url == '1':
		period = 'topviewweek'
	elif url == '2':
		period = 'topviewmonth'
	html = GetUrl(domain, domain)
	menu = re.compile(u'<ul .+? id="%s"[^>]*>(.+?)</ul>' % period).findall(html)[0]
	items = re.compile(u'>([^>]*)</span.+?<a title=".+?" href="(.+?)"[^>]*>([^<]*)</a>([^<]*)<').findall(menu)
	for pos, link, name, year in items:
		pos = '[COLOR orangered]' + pos + '[/COLOR]. '
		name = html_parser.unescape(name).strip().replace('"', "'")
		name = '[COLOR white]' + name + '[/COLOR]'
		year = '[COLOR grey]' + year + '[/COLOR]'
		AddDir(pos + name + year, link, 'mirrors', icon, vname=name, fanart=icon)
	EndDir()
	xbmcplugin.setContent(addonHandle, 'Movies')
	xbmc.executebuiltin('Container.SetViewMode(%s)' % wideview)

def History(url):
#	if True: # DEBUG #
	try:
		history = eval(addon.getSetting('history'))
		if len(history) == 0:
			raise
	except:
		history = '[]'
		addon.setSetting('history', history)
		Search(url, history)
	else:
		contextMenu = [('[COLOR white]XÓA TẤT CẢ[/COLOR]', 'XBMC.Container.Update(plugin://%s?mode=clear)' % addonId)]
		AddDir('[COLOR white][B]TÌM KIẾM MỚI[/B][/COLOR]', url, 'search', icons['search'], extra=str(history), context=contextMenu)
		for i, searchText in enumerate(reversed(history)):
			num = abs(i+1-len(history))
			searchText = urllib.unquote(searchText)
			contextMenu = [
				('[COLOR white]XÓA HÀNG[/COLOR]', 'XBMC.Container.Update(plugin://%s?mode=clear&extra=%d)' % (addonId, num)),
				('[COLOR white]XÓA TẤT CẢ[/COLOR]', 'XBMC.Container.Update(plugin://%s?mode=clear)' % addonId)
			]
			AddDir('[COLOR orangered][B]%s[/B][/COLOR]' % urllib.unquote_plus(searchText),  url % searchText, 'index', icons['history'], context=contextMenu)
		EndDir(viewMode=50)

def Search(url, history):
#	if True: # DEBUG #
	try:
		if '&act=search' in url:
			keyb = xbmc.Keyboard('', '[COLOR white][B]Nhập từ khóa để tìm:[/B][/COLOR]')
			keyb.doModal()
			if (keyb.isConfirmed()):
				searchText = urllib.quote_plus(keyb.getText())
				if not searchText == '':
					try:
						history = eval(history)
						if len(history) >= maxhistory: del history[0]
						history.append(searchText)
						addon.setSetting('history', repr(history))
					except:
						pass
		elif '-trang-' in url:
			keyb = xbmcgui.Dialog()
			searchText = keyb.input('Số trang:', type=xbmcgui.INPUT_NUMERIC)
		url = url % (searchText)
		print('| Search | %s' % url)
		Index(url)
	except:
		pass

def Clear(num):
	if num:
		history = eval(addon.getSetting('history'))
		del history[int(num)]
	else:
		history = []
	addon.setSetting('history', repr(history))
	if len(history) == 0:
		AddDir('[COLOR white][B]TÌM KIẾM MỚI[/B][/COLOR]', '', 'search', icons['search'], extra=str(history))
		EndDir(viewMode=50)
	else:
		xbmc.executebuiltin('Container.Refresh')

def Index(url):
	print('| Index | %s' % url)
	html = GetUrl(url, domain)
	vidlist = re.compile(u'<ul class="list-film">(.+?)</ul>').findall(html)[0]
	vidlist = re.compile(u'<li>(.+?)</li>').findall(vidlist)
	for video in vidlist:
		vthumb, vurl, vname, vyear = re.compile(u'<img alt=".+?" src="(.+?)" .+?<div class="name"><a title=".+?" href="(.+?)">([^<]*)</a>([^<]*)').findall(video)[0]
		vname = html_parser.unescape(vname).strip().replace('"', "'")
		vname = '[COLOR white]' + vname + '[/COLOR]'
		vyear = '[COLOR grey]' + vyear + ' - [/COLOR]'
		try:
			vname2 = re.compile(u'<div class="name2">([^<]*)<').findall(video)[0]
			vname2 = html_parser.unescape(vname2).strip().replace('"', "'")
			vname2 = '[COLOR grey]' + vname2  + '[/COLOR]'
		except:
			vname2 = ''
		try:
			vinfo = re.compile(u'<div class="status">([^<]*)<').findall(video)[0]
			vinfo = html_parser.unescape(vinfo).strip().replace('"', "'")
			vinfo = ' [COLOR orangered](' + vinfo + ')[/COLOR] '
			vinfo = vinfo.replace('Lồng Tiếng', 'LT').replace('(Phụ Đề)', '/').replace('Thuyết Minh', 'TM')
		except:
			vinfo = ' [COLOR orangered]/[/COLOR] '
#		try:
#			vinfo2 = re.compile('<div class="HD">([^<]*)<').findall(video)[0]
#			vinfo2 = html_parser.unescape(vinfo2).strip().replace('"', "'")
#			vinfo2 = ' [COLOR orangered](' + vinfo2 + ')[/COLOR] '
#		except:
#			vinfo = ' [COLOR orangered]/[/COLOR] '
		if 'Coming Soon' in vinfo:
			pass
		else:
#			if 'phim-le' in url:
#				folder = False
#			else:
#				folder = True
			folder = True
			AddDir(vyear + vname + vinfo + vname2, vurl, 'mirrors', vthumb, vname=(vname + ' / ' + vname2), folder=folder)

#	if True: # DEBUG #
	try:
		paging = re.compile(u'<div class="Paging">(.+?)</div>').findall(html)[0]
		if 'Next<' in paging:
			pageText = 'page' if '/phim-moi' in url else 'trang'
			try:
				page = int(re.compile('-%s-(\d+)' % pageText).findall(url)[0])
				pnext = re.sub('-%s-(\d+)' % pageText, '-%s-%s' % (pageText, str(page+1)), url)
			except:
				pnext = '%s-%s-2/' % (url.rstrip('/'), pageText)
			print(pnext)
			AddDir('[COLOR orangered]Trang kế >>[/COLOR]', pnext, 'index', 'http://www.iconsdb.com/icons/preview/red/arrow-32-xxl.png')
	except:
		pass

	if '&act=search' in url:
		EndDir(contentType='Movies', viewMode=wideview)
	else:
		EndDir(contentType=contenttype, viewMode=viewmode)

def Info(url):
#	if True: # DEBUG #
	try:
		src = GetUrl(url, domain)
		replacements = [('s"+"cript', 'script'), ('sc"+"ript', 'script'), ('scr"+"ipt', 'script'), ('scri"+"pt', 'script'), ('scrip"+"t', 'script'), ('s" + "cript', 'script'), ('sc" + "ript', 'script'), ('scr" + "ipt', 'script'), ('scri" + "pt', 'script'), ('scrip" + "t', 'script')]
		for rep in replacements: src = src.replace(rep[0], rep[1])
		soup = BeautifulSoup(src, 'html.parser')
		try:
			image = soup.find('meta', property='og:image')['content']
			if not image: raise
		except:
			image = re.compile('<meta property="og:image" content="(.+?)"').findall(src)[0]
		if image.startswith('/'): image = domain + image
		try:
			title = soup.find('meta', property='og:title')['content']
			if not title: raise
		except:
			title = re.compile('<meta property="og:title" content="(.+?)"').findall(src)[0]
		title = title.replace(' - Xem online', '').replace(' - Xemonline', '')
		info = str(soup.find(class_='movie-meta-info'))
		info = re.compile('<dt[^>]*>(.+?)</dt><dd[^>]*>(.+?)</dd>').findall(info) # WORK-AROUND
		info2 = ''
		for dt, dd in info:
			dd = re.sub('<a[^>]*>', '', dd)
			dd = re.sub('</a>', '', dd)
			info2 = info2 + ('[COLOR orangered]%s[/COLOR] [COLOR white]%s[/COLOR]' % (dt, dd)) + '\n'
		desc = soup.find(class_='detail-content-main')
		desc = str(desc).replace('<div>', '').replace('</div>', '<br/>').replace('<br/><br/>', '<br/>')
		soup = BeautifulSoup(desc, 'html.parser')
		desc = soup.text.replace('##br##', '\n').replace('\n\n', '\n')
		desc = desc.strip().replace(':', ': ').replace('"', "'")

		ACTION_MOVE_LEFT     = 1
		ACTION_MOVE_RIGHT    = 2
		ACTION_MOVE_UP       = 3
		ACTION_MOVE_DOWN     = 4
		ACTION_PREVIOUS_MENU = 10
		ACTION_BACK          = 92
		class InfoWindow(xbmcgui.WindowDialog):
			def __init__(self):
				# MAIN WINDOW
				self.window = xbmcgui.ControlImage(x=0, y=0, width=1280, height=720, filename=fanart, aspectRatio=0, colorDiffuse='0xFF666666')
				self.addControl(self.window)
				# IMAGE
				self.imageWindow = xbmcgui.ControlImage(x=47, y=47, width=306, height=406, filename=os.path.join(addonDir, 'resources/images/white.png'), aspectRatio=0, colorDiffuse='0x55FFFFFF')
				self.addControl(self.imageWindow)
				self.image = xbmcgui.ControlImage(x=50, y=50, width=300, height=400, filename=image, aspectRatio=1)
				self.addControl(self.image)
				# TEXT
				self.title = xbmcgui.ControlLabel(x=400, y=50, width=830, height=50, label=title, font='Volume', textColor='0xFFFFFFFF', alignment=0)
				self.addControl(self.title)
				self.textboxWindow = xbmcgui.ControlImage(x=400, y=125, width=830, height=175, filename=os.path.join(addonDir, 'resources/images/black.png'), aspectRatio=0, colorDiffuse='0x88444444')
				self.addControl(self.textboxWindow)
				self.textbox1 = xbmcgui.ControlTextBox(x=425, y=140, width=780, height=145, font='Details', textColor='0xFF00FFFF')
				self.addControl(self.textbox1)
				self.textbox1.setText(info2)
				self.textbox1.autoScroll(2500, 2500, 2500)
				self.textbox2 = xbmcgui.ControlTextBox(x=400, y=325, width=830, height=345, font='size22', textColor='0xFFFFFFFF')
				self.addControl(self.textbox2)
				self.textbox2.setText(desc)
				self.textbox2.autoScroll(2500, 2500, 2500)
				# BUTTON
				if xbmc.getSkinDir() == 'skin.estuary':
					self.button1 = xbmcgui.ControlButton(x=50, y=500, width=300, height=50, label='Xem | Watch', focusTexture=os.path.join(addonDir, 'resources/images/white.png'), noFocusTexture=os.path.join(addonDir, 'resources/images/white.png'), font='font36_title', textColor ='0xFF222222', alignment=6, disabledColor='0xFF222222', focusedColor='0xFF222222')
				else:
					self.button1 = xbmcgui.ControlButton(x=50, y=500, width=300, height=50, label='XEM', font='InfoTitle', alignment=6)
				self.addControl(self.button1)
				self.setFocus(self.button1)

			def onAction(self, action):
				if action == ACTION_PREVIOUS_MENU or action == ACTION_BACK:
					self.close()
					self.prompt = False

			def onControl(self, control):
				if control == self.button1:
					self.close()
					self.prompt = True

			def Response(self):
				return self.prompt

		window = InfoWindow()
		window.setCoordinateResolution(2)
		window.doModal()
		prompt = window.Response()
		del window
		return prompt

	except:
		return True

def Mirrors(url, iconimage, vname):
	newurl = url + 'xem-online.html'
	print('| Mirrors | %s' % newurl)
	html = GetUrl(newurl, domain)
	mlist = re.compile(u'<h4>([^>]*)</h4><div class="page-tap"><ul>(.+?)</ul>').findall(html)
	if mlist == []:
		pass
	else:
		if len(mlist) > 1:
			labels = [('[COLOR white]Nguồn ' + mirror[0].encode('utf-8') + '[/COLOR]')for mirror in mlist]
			prompt = -1
			prompt = xbmcgui.Dialog().select('Chọn / Choose:', labels)
			if prompt == -1:
				mlinks = ''
			else:
				mlinks = mlist[prompt][1]
		else:
			mlinks = mlist[0][1]
		html = mlinks
	if html == '':
		if mlist:
			AddLink('[COLOR white]Bấm RETURN để quay trở lại.[/COLOR]', '', '', '', '')
			AddLink('[COLOR white]Press RETURN to go back.[/COLOR]', '', '', '', '')
			EndDir()
		else:
			PlayVideo(url, iconimage, vname)
	else:
		Episodes(newurl, iconimage, vname, html)

def Episodes(url, iconimage, vname, html):
#	print('| Episodes | %s' % url)
	elist = re.compile(u'<a href="(.+?)" title="(.+?)"><span>([^<]*)</span>').findall(html)
	if elist:
		for elink, ename, ename2 in elist:
			ename = '[COLOR orangered](' + ename.strip() + ')[/COLOR]'
			ename2 = '[COLOR orangered]' + ename2.strip() + '[/COLOR]'
			vname = '[COLOR white]' + vname + '[/COLOR]'
			if len(elist) == 1:
				PlayVideo(elink, iconimage, vname)
			else:
				AddLink(ename2 + ' - ' + vname, elink, 'loadvideo', iconimage, vname + ' ' + ename )
		if len(elist) > 1:
			EndDir()
	else:
		PlayVideo(url, iconimage, vname)

def GetVideo(url):
	print('| Video | %s' % url)
	html = GetUrl(url, domain)
#	if True: # DEBUG POINT - UNCOMMENT HERE
	try:
		if 'source src=' in html:
			links = re.compile(u'<source src="(.+?)".+?data-res="(.+?)"/>').findall(html)
			print('| LINKS | %s' % str(links))
			url = ChooseRes(links)
			url = url.replace('\/', '/').replace('\\/', '/').encode('utf-8')
		elif 'sources:' in html:
			links = re.compile(u'file: "(.+?)",label: "(.+?)"').findall(html)
			print('| LINKS | %s' % str(links))
			url = ChooseRes(links)
			url = url.replace('\/', '/').replace('\\/', '/').encode('utf-8')
		elif 'mediaplayer_html5_api' in html:
			url2 = re.compile('<iframe.+?"mediaplayer_html5_api".+?src=([^\s]*)').findall(html)[0]
			if url2.startswith('"'): url2 = re.compile('"(.+?)"').findall(url2)[0]
			print('| IFRAME | %s' % str(url2))
			if 'uniup.' in url2: # UNFINISHED
				url = ''
			else:
				url = ''
	except:
		try:
			url = GetYouTubeID(html)
		except:
			url = ''
			xbmcgui.Dialog().ok('Báo Lỗi / Error','Video này không còn xem được.', 'This video is no longer available.')
	return url

def GetYouTubeID(url):
	youtubeID = re.compile('watch\?v=(.+?[^"|\s|\']*)').findall(url)[0]
	url = 'plugin://plugin.video.youtube/play/?video_id=%s' % youtubeID
	return url

def LoadVideo(url, vname):
	url = GetVideo(url)
	print('| Resolved | %s' % url)
	video = xbmcgui.ListItem(vname)
	video.setProperty('IsPlayable', 'true')
	video.setPath(str(url))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, video)

def PlayVideo(url, iconimage, vname):
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create('PhimMedia', 'Đang tải. Xin chờ...')
#	if True: # DEBUG POINT - UNCOMMENT HERE
	try:
		url = GetVideo(url)
		print('| Resolved | %s' % url)
		video = xbmcgui.ListItem(vname, thumbnailImage=iconimage)
		xbmc.Player().play(url, listitem=video)
	except:
		xbmcgui.Dialog().ok('Xin lỗi', 'Phim hiện không xem được', 'Xin vui lòng thử phim khác')
	dialogWait.close()
	del dialogWait
	AddLink('[COLOR white]Bấm RETURN để quay trở lại.[/COLOR]', '', '', '', '')
	AddLink('[COLOR white]Press RETURN to go back.[/COLOR]', '', '', '', '')

def ChooseRes(src):
	# Forces order: 0. Label, 1. Link
	src2 = []
	if len(str(src[0][0])) > 7:
		for link, label in src:
			src2.append((label, link))
	else:
		src2 = src
	# Passes single Link
	if len(src2) == 1:
		return src2[0][1]
	else:
	# Auto chooses maximum resolution from settings
		for res in reversed(range(len(resolution))):
			if res <= maxres:
				for i, (label, link) in enumerate(src2):
					if resolution[res] in str(label):
						return link
	# Prompts user to choose resolution
		labels = [('[COLOR white]%s[/COLOR]' % label) for label, link in src2]
		dialog = xbmcgui.Dialog()
		prompt = -1
		prompt = dialog.select('Choose / Chọn:', labels)
		if prompt == -1:
			link = None
		else:
			link = src2[prompt][1]
		return link

def GetUrl(url, referer):
	r = s.get(url=url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, sdch', 'Referer': referer})
	r.encoding = 'utf-8'
	response = Minify(r.text)
	return response

def Minify(html):
	html = ''.join(html.splitlines()).replace('\'', '"')
	html = html.replace('\n', '')
	html = html.replace('\t', '')
	html = re.sub('  +', ' ', html)
	html = html.replace('> <', '><')
#	html = unicodefix.fix_bad_unicode(html)
	return html.encode('utf-8')

def AddLink(name, url, mode, iconimage, vname):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&vname=" + urllib.quote_plus(vname)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title":vname})
	liz.setProperty("IsPlayable", "true")
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
	return ok

def AddDir(name, url, mode, iconimage, vname='', folder=True, fanart=fanart, extra='', context=None, contextReplace=False):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&vname=" + urllib.quote_plus(vname) + "&extra=" + urllib.quote_plus(extra)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo(type="Video", infoLabels={"Title":name})
	# ADD CONTEXT MENU ITEMS
	if context:
		liz.addContextMenuItems(context, replaceItems=contextReplace)
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=folder)
	return ok

def EndDir(cache=True, contentType='Files', viewMode=50):
	# SET VIEW MODE
	xbmcplugin.setContent(addonHandle, contentType)
	xbmc.executebuiltin('Container.SetViewMode(%s)' % viewMode)
	# END DIR
	xbmcplugin.endOfDirectory(addonHandle, cacheToDisc=cache)

def parameters_string_to_dict(parameters):
	paramDict = {}
	if parameters:
		paramPairs = parameters[1:].split("&")
		for paramsPair in paramPairs:
			paramSplits = paramsPair.split('=')
			if len(paramSplits) == 2:
				paramDict[paramSplits[0]] = paramSplits[1]
	return paramDict

params    = parameters_string_to_dict(sys.argv[2])
url       = params.get('url')
mode      = params.get('mode')
name      = params.get('name')
iconimage = params.get('iconimage')
vname     = params.get('vname')
extra     = params.get('extra')

if type(url) == type(str()):
	url = urllib.unquote_plus(url)
if type(name) == type(str()):
	name = urllib.unquote_plus(name)
if type(iconimage) == type(str()):
	iconimage = urllib.unquote_plus(iconimage)
if type(vname) == type(str()):
	vname = urllib.unquote_plus(vname)
if type(extra) == type(str()):
	extra = urllib.unquote_plus(extra)

sysarg = str(sys.argv[1])
s = requests.session()

if   mode == 'index' or mode == 'self' : Index(url)
elif mode == 'submenu'   : SubMenu(url)
elif mode == 'top'       : Top(url)
elif mode == 'history'   : History(url)
elif mode == 'search'    : Search(url, extra)
elif mode == 'clear'     : Clear(extra)
elif mode == 'mirrors'   :
	if Info(url):
		Mirrors(url, iconimage, vname)
elif mode == 'loadvideo' :
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create('PhimMedia', 'Đang tải. Xin chờ...')
#	if True: # DEBUG POINT - UNCOMMENT HERE
	try:
		LoadVideo(url, vname)
	except:
		xbmcgui.Dialog().ok('Xin lỗi', 'Phim hiện không xem được', 'Xin vui lòng thử phim khác')
	dialogWait.close()
	del dialogWait
elif mode == 'settings'  : xbmc.executebuiltin('Addon.OpenSettings(%s)' % addonId)
else                     : Home()
