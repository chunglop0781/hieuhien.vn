#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xbmc, xbmcaddon, xbmcplugin, xbmcgui
import os, re, requests, sys, urllib, urllib2

addonID      = 'plugin.video.hieuhien.vn.xemphimmienphi'
addon        = xbmcaddon.Addon(addonID)
addondir     = xbmc.translatePath(addon.getAddonInfo('path') ) 
pluginhandle = int(sys.argv[1])
skin_used    = xbmc.getSkinDir()
domain       = 'http://xemphimmienphi.net'


def Home():
	addDir('Phim bộ -- Series', 'http://xemphimmienphi.net/phim-bo/', 'index', os.path.join(addondir, 'icons', 'series.png'), '')
	addDir('Phim bộ theo quốc gia -- Series by country', 'http://xemphimmienphi.net/', 'seriesbycountry', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('Phim lẻ -- Movies', 'http://xemphimmienphi.net/phim-le/', 'index', os.path.join(addondir, 'icons', 'movies.png'), '')
	addDir('Phim lẻ theo thể loại -- Movies by category', 'http://xemphimmienphi.net/', 'moviesbycategory', os.path.join(addondir, 'icons', 'genres.png'), '')
	addDir('Phim khác -- Others', 'http://xemphimmienphi.net/phim-khac/', 'index', os.path.join(addondir, 'icons', 'others.png'), '')
	addDir('Phim theo quốc gia -- By country', 'http://xemphimmienphi.net/', 'bycountry', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('Phim theo năm -- By year', 'http://xemphimmienphi.net/', 'byyear', os.path.join(addondir, 'icons', 'years.png'), '')
	addDir('[ Tìm Kiếm -- Search ]', 'http://xemphimmienphi.net/tim-kiem/?tk=', 'search', os.path.join(addondir, 'icons', 'search.png'), '')
	if skin_used == 'skin.heidi':
		xbmc.executebuiltin('Container.SetViewMode(53)')

def SeriesByCountry():
	addDir('Phim Việt Nam', 'http://xemphimmienphi.net/phim-viet-nam/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('Phim Trung Quốc -- China series', 'http://xemphimmienphi.net/phim-trung-quoc/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('Phim Hàn Quốc -- Korea series', 'http://xemphimmienphi.net/phim-han-quoc/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('Phim Đài Loan --  Taiwan series', 'http://xemphimmienphi.net/phim-dai-loan/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('Phim Hồng Kông -- Hong Kong series', 'http://xemphimmienphi.net/phim-hong-kong/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('Phim Nhật Bản -- Japan series', 'http://xemphimmienphi.net/phim-nhat-ban/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('Phim Mỹ -- US series', 'http://xemphimmienphi.net/phim-my-us/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('Phim Thái Lan -- Thailand series', 'http://xemphimmienphi.net/phim-thai-lan/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
#	addDir('Hong Kong series (English sub)', 'http://xemphimmienphi.net/phim-hongkong-english-sub/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
#	addDir('Series (English sub)', 'http://xemphimmienphi.net/phim-bo-english-sub/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')

def MoviesByCategory():
	addDir('Phim hành động -- Action', 'http://xemphimmienphi.net/phim-hanh-dong/', 'index', os.path.join(addondir, 'icons', 'genres.png'), '')
	addDir('Phim kiếm hiệp -- Martial arts', 'http://xemphimmienphi.net/phim-kiem-hiep/', 'index', os.path.join(addondir, 'icons', 'genres.png'), '')
	addDir('Phim hài -- Comedy', 'http://xemphimmienphi.net/phim-hai/', 'index', os.path.join(addondir, 'icons', 'genres.png'), '')
	addDir('Phim phiêu lưu -- Adventure', 'http://xemphimmienphi.net/phim-phieu-luu/', 'index', os.path.join(addondir, 'icons', 'genres.png'), '')
	addDir('Phim kinh dị -- Horror', 'http://xemphimmienphi.net/phim-kinh-di/', 'index', os.path.join(addondir, 'icons', 'genres.png'), '')
	addDir('Phim tình cảm -- Romance', 'http://xemphimmienphi.net/phim-tinh-cam/', 'index', os.path.join(addondir, 'icons', 'genres.png'), '')
	addDir('Phim hoạt hình -- Animation', 'http://xemphimmienphi.net/phim-hoat-hinh/', 'index', os.path.join(addondir, 'icons', 'genres.png'), '')
	addDir('Phim viễn tưởng -- Fiction', 'http://xemphimmienphi.net/phim-vien-tuong/', 'index', os.path.join(addondir, 'icons', 'genres.png'), '')
	addDir('Phim tâm lý -- Psychological', 'http://xemphimmienphi.net/phim-tam-ly/', 'index', os.path.join(addondir, 'icons', 'genres.png'), '')
#	addDir('Phim 18+ -- Adult (18+)', 'http://xemphimmienphi.net/phim-18/', 'index', os.path.join(addondir, 'icons', 'genres.png'), '')
	addDir('Hài kịch -- Vietnamese comedy', 'http://xemphimmienphi.net/hai-kich/', 'index', os.path.join(addondir, 'icons', 'genres.png'), '')
	addDir('Phim chiến tranh -- War/combat', 'http://xemphimmienphi.net/phim-chien-tranh/', 'index', os.path.join(addondir, 'icons', 'genres.png'), '')
#	addDir('Animation (English sub)', 'http://xemphimmienphi.net/phim-hoat-hinh-english-sub/', 'index', os.path.join(addondir, 'icons', 'genres.png'), '')
	addDir('Thể thao -- Sports', 'http://xemphimmienphi.net/the-thao/', 'index', os.path.join(addondir, 'icons', 'genres.png'), '')
	addDir('Talk shows / TV shows', 'http://xemphimmienphi.net/talkshow-tivi-show/', 'index', os.path.join(addondir, 'icons', 'genres.png'), '')
#	addDir('Series (English sub)', 'http://xemphimmienphi.net/phim-le-english-sub/', 'index', os.path.join(addondir, 'icons', 'genres.png'), '')

def ByCountry():
	addDir('Vietnam', 'http://xemphimmienphi.net/country/vietnam-9/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('China', 'http://xemphimmienphi.net/country/china-5/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('Hong Kong', 'http://xemphimmienphi.net/country/hong-kong-18/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('Japan', 'http://xemphimmienphi.net/country/japan-11/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('Korea', 'http://xemphimmienphi.net/country/korea-1/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('Philippines', 'http://xemphimmienphi.net/country/philippines-4/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('Singapore', 'http://xemphimmienphi.net/country/singapore-17/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('Taiwan', 'http://xemphimmienphi.net/country/taiwan-2/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('Thailand', 'http://xemphimmienphi.net/country/thailand-3/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('United Kingdom', 'http://xemphimmienphi.net/country/united-kingdom-52/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')
	addDir('United States', 'http://xemphimmienphi.net/country/united-states-10/', 'index', os.path.join(addondir, 'icons', 'countries.png'), '')

def ByYear():
	addDir('2014-2015', 'http://xemphimmienphi.net/nam-phat-hanh/2015/', 'index', os.path.join(addondir, 'icons', 'years.png'), '')
	addDir('2013', 'http://xemphimmienphi.net/nam-phat-hanh/2013/', 'index', os.path.join(addondir, 'icons', 'years.png'), '')
	addDir('2012', 'http://xemphimmienphi.net/nam-phat-hanh/2012/', 'index', os.path.join(addondir, 'icons', 'years.png'), '')
	addDir('2011', 'http://xemphimmienphi.net/nam-phat-hanh/2011/', 'index', os.path.join(addondir, 'icons', 'years.png'), '')
	addDir('2010', 'http://xemphimmienphi.net/nam-phat-hanh/2010/', 'index', os.path.join(addondir, 'icons', 'years.png'), '')
	addDir('Trước năm 2010 -- Before 2010', 'http://xemphimmienphi.net/nam-phat-hanh/truoc-nam-2010/', 'index', os.path.join(addondir, 'icons', 'years.png'), '')

def Search():
	try:
		keyb = xbmc.Keyboard('', 'Enter search text')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText = urllib.quote_plus(keyb.getText())
		url = 'http://xemphimmienphi.net/tim-kiem/?tk=' + searchText
		Index(url)
	except: pass

def Index(url):
	link = GetUrl(url)
	match = re.compile('<div class="rowProduct">(.+?)<div class="fr_page_links">').findall(link)
	vidlist = re.compile('<a href="(.+?)" class="img" title="(.+?)"><img src="(.+?)" [^>]*/>(.+?)<span class="tap">(.*?)</span>').findall(match[0])
	for vurl, vnamefull, vthumb, vtmp, vquality in vidlist:
		if vthumb.find("http://") == -1:
			vthumb = domain + vthumb.replace("/ ", "/")
		if vquality.find("HD") != -1:
			vquality = "[B][COLOR yellow](" + vquality + ")[/COLOR][/B]"
		elif vquality != '':
			vquality = "[B][COLOR white](" + vquality + ")[/COLOR][/B]"
		addDir("[B]" + vnamefull + "[/B] " + vquality, domain + vurl, 'mirrors', vthumb, vnamefull)
	pagelist = re.compile('<div class="fr_page_links">(.+?)</div>').findall(link)[0]
	navmatch = re.compile('<a([^>]*)href="(.+?)"[^>]*>(.+?)<\/a>').findall(pagelist)
	for pcurrent, purl, pname, in navmatch:
		if pname == 'Prev': pname = '<< Previous Page ]'
		elif pname == 'Next' : pname = '[ Next Page >>'
		else: pname = '[ Page ' + pname + ' ]'
		addDir(pname, domain + purl, 'index', '', '')

def Mirrors(url, iconimage, vname):
	mirrorlink = GetVidPage(url)
	link = GetUrl(mirrorlink)
	serverlist = re.compile('<span class="server_name">(.+?)</span>').findall(link)
	for servername in serverlist:
		if '<' in servername: servername = 'Server Other'
		elif ('DOWNLOAD' in servername) or ('Download' in servername):
			pass
		else:
			addDir(servername, mirrorlink.encode("utf-8"), 'episodes', iconimage, vname)

def Episodes(url, name, iconimage, vname):
	link = GetUrl(url)
	if name == 'Server Other': name = ''
	servlist = re.compile('<span class="server_name">' + urllib2.unquote(name) + '</span>(.*?)</table>').findall(link)
	epilist = re.compile('<a [^>]*href="(.+?)">(.+?)</a>').findall(servlist[0])
	for vlink, vLinkName in epilist:
		addLink("Tập " + vLinkName.strip().encode("utf-8"), domain + vlink, 'loadvideo', iconimage, vname + ' [COLOR yellow](Tập ' + vLinkName.strip().encode("utf-8") + ')[/COLOR]')

def GetVidPage(url):
	url = url.split("/")[-1].replace(".html", "-1-1.html")
	return domain + "/xem-online/" + url

def LoadVideos(url, vname):
	vidcontent = GetUrl(url)
	if "youtube" in vidcontent:
		ytlink = re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(vidcontent)
		ytID = ytlink[0][len(ytlink[0])-1].replace('v/', '')
		url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + ytID.replace('?', '')
		video = xbmcgui.ListItem(vname)
		video.setProperty("IsPlayable", "true")
		video.setPath(url)
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, video)
	elif '{link:"' in vidcontent:
		link = re.compile('\{link:"(.+?)"').findall(vidcontent)[0]
		script = domain + '/gkphp/plugins/gkpluginsphp.php'
		gkp = requests.post(script, data={'link': link, 'f': 'true'}).json()
		if "list" in gkp:
			url = gkp["list"][0]["link"][-1]["link"]
		else:
			url = gkp["link"][-1]["link"]
		video = xbmcgui.ListItem(vname)
		video.setProperty('IsPlayable', 'true')
		video.setPath(str(url))
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, video)
	else:
		pass

def GetUrl(url):
	req = urllib2.Request(url)
	req.add_header('Host', 'xemphimmienphi.net')
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

def addLink(name, url, mode, iconimage, vname):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&vname=" + urllib.quote_plus(vname)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title":vname})
	liz.setProperty("IsPlayable", "true")
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
	return ok

def addDir(name, url, mode, iconimage, vname):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&vname=" + urllib.quote_plus(vname)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={"Title":name})
	ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
	return ok

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

if type(url) == type(str()):
	url = urllib.unquote_plus(url)
if type(name) == type(str()):
	name = urllib.unquote_plus(name)
if type(iconimage) == type(str()):
	iconimage = urllib.unquote_plus(iconimage)
if type(vname) == type(str()):
	vname = urllib.unquote_plus(vname)

sysarg = str(sys.argv[1])

if mode == 'index':
	Index(url)
elif mode == 'seriesbycountry':
	SeriesByCountry()
elif mode == 'moviesbycategory':
	MoviesByCategory()
elif mode == 'bycountry':
	ByCountry()
elif mode == 'byyear':
	ByYear()
elif mode == 'search':
	Search()
elif mode=='mirrors':
	Mirrors(url, iconimage, vname)
elif mode=='episodes':
	Episodes(url, name, iconimage, vname)
elif mode=='loadvideo':
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create('XemPhimMienPhi', 'Đang tải. Xin chờ...')
	try:
		LoadVideos(url, vname)
	except:
		xbmcgui.Dialog().ok('Xin lỗi', 'Nguồn phim hiện không xem được', 'Xin vui lòng thử nguồn khác')
	dialogWait.close()
	del dialogWait
else:
	Home()

xbmcplugin.endOfDirectory(int(sysarg))