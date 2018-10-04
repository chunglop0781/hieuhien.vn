#!/usr/bin/python
# coding=utf8

import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import base64, os, re, sys, urllib, urllib2
import openload

addonID      = 'plugin.video.hieuhien.vn.myasiantv'
addon        = xbmcaddon.Addon(addonID)
addon_handle = int(sys.argv[1])
skin_used    = xbmc.getSkinDir()

def Home():
	addDir('[COLOR yellow]Korean Dramas[/COLOR]', 'http://myasiantv.se/drama/?selOrder=1&selCat=0&selCountry=4&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('[COLOR white]All Series[/COLOR]', 'http://myasiantv.se/drama', 'index', 'http://myasiantv.se/templates/default/images/logo.png', '')
	addDir('[COLOR white]All Movies[/COLOR]', 'http://myasiantv.se/movie', 'index', 'http://myasiantv.se/templates/default/images/logo.png', '')
	addDir('Top Day', 'http://myasiantv.se/', 'featured', 'http://myasiantv.se/templates/default/images/logo.png', '')
	addDir('Top Week', 'http://myasiantv.se/', 'featured', 'http://myasiantv.se/templates/default/images/logo.png', '')
	addDir('Top Month', 'http://myasiantv.se/', 'featured', 'http://myasiantv.se/templates/default/images/logo.png', '')
	addDir('[COLOR pink]Browse Series by Country[/COLOR]', 'http://myasiantv.se/', 'seriesbycountry', 'http://myasiantv.se/templates/default/images/logo.png', '')
	addDir('[COLOR pink]Browse Series by Genre[/COLOR]', 'http://myasiantv.se/', 'seriesbygenre', 'http://myasiantv.se/templates/default/images/logo.png', '')
	addDir('[COLOR pink]Browse Series by Year[/COLOR]', 'http://myasiantv.se/', 'seriesbyyear', 'http://myasiantv.se/templates/default/images/logo.png', '')
	addDir('[COLOR purple]Browse Movies by Country[/COLOR]', 'http://myasiantv.se/', 'moviesbycountry', 'http://myasiantv.se/templates/default/images/logo.png', '')
	addDir('[COLOR purple]Browse Movies by Genre[/COLOR]', 'http://myasiantv.se/', 'moviesbygenre', 'http://myasiantv.se/templates/default/images/logo.png', '')
	addDir('[COLOR purple]Browse Movies by Year[/COLOR]', 'http://myasiantv.se/', 'moviesbyyear', 'http://myasiantv.se/templates/default/images/logo.png', '')
	addDir('[ Search ]', 'http://myasiantv.se/search/%s/page-1', 'search', 'http://myasiantv.se/templates/default/images/logo.png', '')

def SeriesByCountry():
	addDir('Korean', 'http://myasiantv.se/drama/?selOrder=1&selCat=0&selCountry=4&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Japanese', 'http://myasiantv.se/drama/?selOrder=1&selCat=0&selCountry=6&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Chinese', 'http://myasiantv.se/drama/?selOrder=1&selCat=0&selCountry=5&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Taiwanese', 'http://myasiantv.se/drama/?selOrder=1&selCat=0&selCountry=7&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Hong Kong', 'http://myasiantv.se/drama/?selOrder=1&selCat=0&selCountry=8&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Others', 'http://myasiantv.se/drama/?selOrder=1&selCat=0&selCountry=1&selYear=0&btnFilter=Submit', 'index', '', '')

def MoviesByCountry():
	addDir('Korean', 'http://myasiantv.se/movie/?selOrder=1&selCat=0&selCountry=4&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Japanese', 'http://myasiantv.se/movie/?selOrder=1&selCat=0&selCountry=6&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Chinese', 'http://myasiantv.se/movie/?selOrder=1&selCat=0&selCountry=5&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Taiwanese', 'http://myasiantv.se/movie/?selOrder=1&selCat=0&selCountry=7&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Hong Kong', 'http://myasiantv.se/movie/?selOrder=1&selCat=0&selCountry=8&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Others', 'http://myasiantv.se/movie/?selOrder=1&selCat=0&selCountry=1&selYear=0&btnFilter=Submit', 'index', '', '')

def SeriesByGenre():
	addDir('Web-Drama', 'http://myasiantv.se/drama/?selOrder=1&selCat=52&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Action', 'http://myasiantv.se/drama/?selOrder=1&selCat=1&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Adventure', 'http://myasiantv.se/drama/?selOrder=1&selCat=7&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Horror', 'http://myasiantv.se/drama/?selOrder=1&selCat=4&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Romance', 'http://myasiantv.se/drama/?selOrder=1&selCat=5&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Family', 'http://myasiantv.se/drama/?selOrder=1&selCat=27&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Thriller', 'http://myasiantv.se/drama/?selOrder=1&selCat=6&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Comedy', 'http://myasiantv.se/drama/?selOrder=1&selCat=3&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Crime', 'http://myasiantv.se/drama/?selOrder=1&selCat=9&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Sci-Fi', 'http://myasiantv.se/drama/?selOrder=1&selCat=10&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Fantasy', 'http://myasiantv.se/drama/?selOrder=1&selCat=34&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Mystery', 'http://myasiantv.se/drama/?selOrder=1&selCat=29&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('War', 'http://myasiantv.se/drama/?selOrder=1&selCat=31&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Music', 'http://myasiantv.se/drama/?selOrder=1&selCat=32&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')

def MoviesByGenre():
	addDir('Action', 'http://myasiantv.se/movie/?selOrder=1&selCat=1&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Adventure', 'http://myasiantv.se/movie/?selOrder=1&selCat=7&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Horror', 'http://myasiantv.se/movie/?selOrder=1&selCat=4&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Romance', 'http://myasiantv.se/movie/?selOrder=1&selCat=5&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Family', 'http://myasiantv.se/movie/?selOrder=1&selCat=27&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Thriller', 'http://myasiantv.se/movie/?selOrder=1&selCat=6&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Comedy', 'http://myasiantv.se/movie/?selOrder=1&selCat=3&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Crime', 'http://myasiantv.se/movie/?selOrder=1&selCat=9&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Sci-Fi', 'http://myasiantv.se/movie/?selOrder=1&selCat=10&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Fantasy', 'http://myasiantv.se/movie/?selOrder=1&selCat=34&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Mystery', 'http://myasiantv.se/movie/?selOrder=1&selCat=29&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('War', 'http://myasiantv.se/movie/?selOrder=1&selCat=31&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')
	addDir('Music', 'http://myasiantv.se/movie/?selOrder=1&selCat=32&selCountry=0&selYear=0&btnFilter=Submit', 'index', '', '')

def Index(url):
	link = GetUrl(url)
	vidlist = re.compile('<a title="(.+?)</div>" href="[^>]*"><img src="(.+?)"[^>]*/></a><h2><a href="(.+?)"[^>]*>(.+?)</a>(.+?)</h2>').findall(link)
	for vplot, vthumb, vurl, vnamefull, vyear in vidlist:
		vplot = vplot.replace('|br| <div class="content"><p>','[CR][CR]')
		vplot = vplot.replace('</p><p>','[CR]')
		vplot = vplot.replace('<strong>','[COLOR cyan]')
		vplot = vplot.replace('</strong>','[/COLOR]')
		vplot = vplot.replace('&amp;','&')
		vplot = vplot.replace('"',"'")
		vplot = vplot.replace('&rsquo;',"'")
		vplot = vplot.replace('&rdquo;','"')
		vplot = vplot.replace('&lsquo;',"'")
		vplot = vplot.replace('&ldquo;','"')
		vplot = re.sub('<[^<]+?>', '', vplot)
		addDir("[B]" + vnamefull.replace('"', "'") + "[/B]", vurl, 'episodes', vthumb, vplot)
	navmatch = re.compile('<a class="prev" href="(.+?)">(.+?)</a>').findall(link.replace("'", '"'))
	for vurl, vname in navmatch:
		addDir('[COLOR yellow][< ' + vname + ' Page ][/COLOR]', vurl, 'index', '', '')
	navmatch = re.compile('<a class="pagelink" href="(.+?)">(.+?)</a>').findall(link.replace("'", '"'))
	for vurl, vname in navmatch:
		addDir('[COLOR yellow][ Page ' + vname + ' ][/COLOR]', vurl, 'index', '', '')
	navmatch = re.compile('<a class="next" href="(.+?)">(.+?)</a>').findall(link.replace("'", '"'))
	for vurl, vname in navmatch:
		addDir('[COLOR yellow][ ' + vname + ' Page >][/COLOR]', vurl, 'index', '', '')

def Featured(url):
	link = GetUrl(url)
	if name == 'Top Day':
		link = re.compile('<div id="sidebarlist-1">(.+?)<div id="sidebarlist-2">').findall(link)[0]
		print link
	if name == 'Top Week':
		link = re.compile('<div id="sidebarlist-2">(.+?)<div id="sidebarlist-3">').findall(link)[0]
	if name == 'Top Month':
		link = re.compile('<div id="sidebarlist-3">(.+?)</div></div></div>').findall(link)[0]
	vidlist = re.compile('<div><a href="[^>]*"><img src="(.+?)"[^>]*/></a><span>(.+?)</span><h2><a href="(.+?)">(.+?)</a>').findall(link)
	for vthumb, vpos, vurl, vname in vidlist:
		addDir(vpos + '. [B]' + vname.replace('"', "'") + '[/B]', vurl, 'episodes', vthumb, '')

def Search():
	try:
		keyb = xbmc.Keyboard('', 'Enter search text')
		keyb.doModal()
		if(keyb.isConfirmed()):
			searchText= urllib.quote_plus(keyb.getText())
		url = 'http://myasiantv.se/search/' + searchText
		Index(url)
	except: pass

def Episodes(url):
	link = GetUrl(url)
	try:
		match = re.compile('<ul class="list-episode">(.+?)</ul>').findall(link)[0]
	except:
		addLink('[COLOR yellow]Sorry, this show has been removed. Please try another show.[/COLOR]', '', '', '', '')
	else:
		elist = re.compile('<a title="[^>]*" href="(.+?)">(.+?)</a>').findall(match)
		if len(elist) == 1:
			elink, ename = elist[0]
			Mirrors(elink, ename)
		else:
			for elink, ename in elist:
				try:
					addDir(ename.replace("&nbsp;", "").strip().encode("utf-8"), elink, 'mirrors', '', '')
				except:
					addDir(str(ename), elink, 'mirrors', '', '') # Convert to strings to avoid ascii codec errors

def Mirrors(url, name):
	link = GetUrl(url)
	# Resolve openload
	if 'openload' in link:
		link = re.compile('<div id="mediaplayer"></div><iframe src="(.+?)"[^>]*>').findall(link)[0]
		addLink('Link: [COLOR white]' + name.replace("&nbsp;", "").strip().encode("utf-8") + '[/COLOR]', openload.resolve(link), 'loadvideo', '', name)
	else:
	# Resolve normal
		mlist = re.compile('window.atob\("(.+?)"\),label: "(.+?)",type:"mp4"').findall(link)
		for mlink, mname in mlist:
			addLink('Link: [COLOR white]' + mname.replace("&nbsp;", "").strip().encode("utf-8") + '[/COLOR]', base64.urlsafe_b64decode(mlink), 'loadvideo', '', name)

def LoadVideos(url, name):
	video = xbmcgui.ListItem(name)
	video.setProperty('IsPlayable', 'true')
	video.setPath(str(url))
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, video)

def GetUrl(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	link = ''.join(link.splitlines()).replace('\'', '"')
	link = link.replace('\n', '')
	link = link.replace('\t', '')
	link = re.sub('  +', ' ', link)
	link = link.replace('> <', '><')
	return link

def addLink(name, url, mode, iconimage, mirrorname):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&mirrorname=" + urllib.quote_plus(mirrorname)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage = iconimage)
	liz.setInfo(type = "Video", infoLabels = { "Title": name })
	liz.setProperty("IsPlayable", "true")
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz)
	return ok

def addDir(name, url, mode, iconimage, plot):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&plot=" + urllib.quote_plus(plot)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo(type = "Video", infoLabels = { "Title": name, "Plot": plot })
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

def parameters_string_to_dict(parameters):
	paramDict = { }
	if parameters:
		paramPairs = parameters[1:].split("&")
		for paramsPair in paramPairs:
			paramSplits = paramsPair.split('=')
			if(len(paramSplits)) == 2:
				paramDict[paramSplits[0]] = paramSplits[1]
	return paramDict

params = parameters_string_to_dict(sys.argv[2])
mode = params.get('mode')
url = params.get('url')
name = params.get('name')

if type(url) == type(str()):
	url = urllib.unquote_plus(url)

if type(name) == type(str()):
	name = urllib.unquote_plus(name)
sysarg = str(sys.argv[1])

if mode == 'index':
	Index(url)
elif mode == 'featured':
	Featured(url)
elif mode == 'search':
	Search()
	xbmcplugin.setContent(addon_handle, 'Movies')
elif mode == 'seriesbycountry':
	SeriesByCountry()
elif mode == 'seriesbygenre':
	SeriesByGenre()
elif mode == 'seriesbyyear':
	SeriesByYear()
elif mode == 'moviesbycountry':
	MoviesByCountry()
elif mode == 'moviesbygenre':
	MoviesByGenre()
elif mode == 'moviesbyyear':
	MoviesByYear()
elif mode == 'episodes':
	Episodes(url)
elif mode == 'mirrors':
	Mirrors(url, name)
elif mode == 'loadvideo':
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create('MyAsianTV.se', 'Loading video. Please wait...')
	LoadVideos(url, name)
	dialogWait.close()
	del dialogWait
else:
	Home()
#Sets content type (files, songs, artists, albums, movies, tvshows, episodes, musicvideos)
xbmcplugin.setContent(addon_handle, 'Movies')

xbmcplugin.endOfDirectory(int(sysarg))