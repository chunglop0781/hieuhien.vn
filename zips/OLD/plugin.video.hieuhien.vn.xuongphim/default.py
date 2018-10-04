#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcaddon, xbmcgui
import os, re, requests, urllib, urllib2, uuid
from xbmcswift2 import Plugin

addonID  = 'plugin://plugin.video.hieuhien.vn.xuongphim'
domain   = 'http://xuongphim.tv'
plugin   = Plugin()
listMax  = 35 # Normal listing
foundMax = 28 # Listing for search results

@ plugin.route('/')
def Home():
	items = [
		{'label': '[COLOR white]Phim Được Đề Cử[/COLOR]', 'path': '%s/movies/voted/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv'))},
		{'label': '[COLOR white]Phim Lẻ Mới[/COLOR]', 'path': '%s/movies/new/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv'))},
		{'label': '[COLOR white]Phim Bộ Mới[/COLOR]', 'path': '%s/series/new/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv'))},
		{'label': '[COLOR white]Anime Mới Cập Nhật[/COLOR]', 'path': '%s/anime/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv'))},
		{'label': '[COLOR white]Phim Chiếu Rạp[/COLOR]', 'path': '%s/movies/theatre/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv'))},
		{'label': '[COLOR white]Top Xem Nhiều[/COLOR]', 'path': '%s/top/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv'))},
		{'label': '[COLOR grey]Phim Lẻ[/COLOR]', 'path': '%s/movies/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/danh-sach/phim-le/trang-%s.html'), 1)},
		{'label': '[COLOR grey]Phim Lẻ theo Thể Loại[/COLOR]', 'path': '%s/genres' % addonID},
		{'label': '[COLOR grey]Phim Bộ[/COLOR]', 'path': '%s/series/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/danh-sach/phim-bo/trang-%s.html'), 1)},
		{'label': '[COLOR grey]Phim Bộ theo Quốc Gia[/COLOR]', 'path': '%s/countries' % addonID},
		{'label': '[COLOR grey]TV Show[/COLOR]', 'path': '%s/tvshows/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-tv-show/trang-%s.html'), 1)},
		{'label': '[COLOR lime][ Tìm Kiếm ][/COLOR]', 'path': '%s/search' % addonID}
]
	return plugin.finish(items)

@ plugin.route('/genres')
def ListGenres():
	items = [
		{'label': 'Hành Động', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-hanh-dong/trang-%s.html'), 1)},
		{'label': 'Phiêu Lưu', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-phieu-luu/trang-%s.html'), 1)},
		{'label': 'Kinh Dị', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-kinh-di/trang-%s.html'), 1)},
		{'label': 'Tình Cảm', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-tam-ly-tinh-cam/trang-%s.html'), 1)},
		{'label': 'Hoạt Hình', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-hoat-hinh/trang-%s.html'), 1)},
		{'label': 'Võ Thuật', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-vo-thuat/trang-%s.html'), 1)},
		{'label': 'Hài Hước', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-hai-huoc/trang-%s.html'), 1)},
		{'label': 'Tâm Lý', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-tam-ly-tinh-cam/trang-%s.html'), 1)},
		{'label': 'Viễn Tưởng', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-vien-tuong/trang-%s.html'), 1)},
		{'label': 'Thần Thoại', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-than-thoai/trang-%s.html'), 1)},
		{'label': 'Chiến Tranh', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-chien-tranh/trang-%s.html'), 1)},
		{'label': 'Kiếm Hiệp', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-kiem-hiep/trang-%s.html'), 1)},
		{'label': 'Lịch Sử', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-lich-su/trang-%s.html'), 1)},
		{'label': 'TV-Show', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-tv-show/trang-%s.html'), 1)},
		{'label': '3D', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-3d/trang-%s.html'), 1)},
		{'label': 'Hình Sự', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-hinh-su/trang-%s.html'), 1)},
		{'label': 'Cổ Trang', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-co-trang/trang-%s.html'), 1)},
		{'label': 'Âm Nhạc', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-am-nhac/trang-%s.html'), 1)},
		{'label': 'Khoa Học', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-khoa-hoc/trang-%s.html'), 1)},
		{'label': 'Tài Liệu', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-tai-lieu/trang-%s.html'), 1)},
		{'label': 'Phim Chiếu Rạp', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-chieu-rap/trang-%s.html'), 1)},
		{'label': 'Gia Đình', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-gia-dinh/trang-%s.html'), 1)},
		{'label': 'Thể Thao', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-the-thao/trang-%s.html'), 1)},
		{'label': 'Hài Tết', 'path': '%s/genres/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-hai-tet/trang-%s.html'), 1)}
]
	return plugin.finish(items)

@ plugin.route('/countries')
def ListCountries():
	items = [
		{'label': 'Việt Nam', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-viet-nam/trang-%s.html'), 1)},
		{'label': 'Trung Quốc', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-trung-quoc/trang-%s.html'), 1)},
		{'label': 'Hàn Quốc', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-han-quoc/trang-%s.html'), 1)},
		{'label': 'Hồng Kông - TVB', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-hong-kong/trang-%s.html'), 1)},
		{'label': 'Mỹ', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-my/trang-%s.html'), 1)},
		{'label': 'Châu Âu', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-chau-au/trang-%s.html'), 1)},
		{'label': 'Nhật Bản', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-nhat-ban/trang-%s.html'), 1)},
		{'label': 'Đài Loan', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-dai-loan/trang-%s.html'), 1)},
		{'label': 'Thái Lan', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-thai-lan/trang-%s.html'), 1)},
		{'label': 'Châu Á', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-chau-a/trang-%s.html'), 1)},
		{'label': 'Ấn Độ', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/quoc-gia-an-do/trang-%s.html'), 1)},
		{'label': 'Pháp', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-phap/trang-%s.html'), 1)},
		{'label': 'Anh', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-anh/trang-%s.html'), 1)},
		{'label': 'Hoạt Hình', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/xem-phim-hoat-hinh/trang-%s.html'), 1)},
		{'label': 'Đức', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-duc/trang-%s.html'), 1)},
		{'label': 'Tây Ban Nha', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-tay-ban-nha/trang-%s.html'), 1)},
		{'label': 'Ireland', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-ireland/trang-%s.html'), 1)},
		{'label': 'Hungary', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-hungary/trang-%s.html'), 1)},
		{'label': 'Nga', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-nga/trang-%s.html'), 1)},
		{'label': 'Philippines', 'path': '%s/countries/%s/%s' % (addonID, urllib.quote_plus('http://xuongphim.tv/phim-bo-philippines/trang-%s.html'), 1)}
]
	return plugin.finish(items)

@ plugin.route('/movies/voted/<url>')
def VotedMovies(url):
	pageContent = getUrl(url)
	sectionContent = re.compile('<section[^>]*>.+?<h[0-9]>.+?Phim Được Đề Cử.+?<\/h[0-9]>(.+?)<\/section>'.decode('utf-8')).findall(pageContent)[0]
	items = sortedItems(sectionContent, 0, 'votedmovies')
	return plugin.finish(items)

@ plugin.route('/movies/new/<url>')
def NewMovies(url):
	pageContent = getUrl(url)
	sectionContent = re.compile('<section[^>]*>.+?<h[0-9]>.+?PHIM LẺ MỚI.+?<\/h[0-9]>(.+?)<\/section>'.decode('utf-8')).findall(pageContent)[0]
	items = sortedItems(sectionContent, 0, 'newmovies')
	return plugin.finish(items)

@ plugin.route('/series/new/<url>')
def NewSeries(url):
	pageContent = getUrl(url)
	sectionContent = re.compile('<section[^>]*>.+?<h[0-9]>.+?PHIM BỘ MỚI.+?<\/h[0-9]>(.+?)<\/section>'.decode('utf-8')).findall(pageContent)[0]
	items = sortedItems(sectionContent, 0, 'newseries')
	return plugin.finish(items)

@ plugin.route('/anime/<url>')
def Anime(url):
	pageContent = getUrl(url)
	sectionContent = re.compile('<section[^>]*>.+?<h[0-9]>.+?ANIME MỚI CẬP NHẬT.+?<\/h[0-9]>(.+?)<\/section>'.decode('utf-8')).findall(pageContent)[0]
	items = sortedItems(sectionContent, 0, 'anime')
	return plugin.finish(items)

@ plugin.route('/movies/theatre/<url>')
def TheatreMovies(url):
	pageContent = getUrl(url)
	sectionContent = re.compile('<section[^>]*>.+?<h[0-9]>.+?PHIM CHIẾU RẠP.+?<\/h[0-9]>(.+?)<\/section>'.decode('utf-8')).findall(pageContent)[0]
	items = sortedItems(sectionContent, 0, 'theatremovies')
	return plugin.finish(items)

@ plugin.route('/top/<url>')
def Top(url):
	pageContent = getUrl(url)
	sectionContent = re.compile('<section[^>]*>.+?<h[0-9]>.+?TOP Xem Nhiều.+?<\/h[0-9]>(.+?)<\/section>'.decode('utf-8')).findall(pageContent)[0]
	items = sortedItems(sectionContent, 0, 'top')
	return plugin.finish(items)

@ plugin.route('/movies/<url>/<page>')
def Movies(url, page):
	items = sortedItems(url, page, 'movies')
	if xbmc.getSkinDir() == 'skin.heidi': return plugin.finish(items, view_mode = 55)
	else: return plugin.finish(items)

@ plugin.route('/series/<url>/<page>')
def Series(url, page):
	items = sortedItems(url, page, 'series')
	if xbmc.getSkinDir() == 'skin.heidi': return plugin.finish(items, view_mode = 55)
	else: return plugin.finish(items)

@ plugin.route('/tvshows/<url>/<page>')
def TVshows(url, page):
	items = sortedItems(url, page, 'series')
	if xbmc.getSkinDir() == 'skin.heidi': return plugin.finish(items, view_mode = 55)
	else: return plugin.finish(items)

@ plugin.route('/genres/<url>/<page>')
def Genres(url, page):
	items = sortedItems(url, page, 'genres')
	if xbmc.getSkinDir() == 'skin.heidi': return plugin.finish(items, view_mode = 55)
	else: return plugin.finish(items)

@ plugin.route('/countries/<url>/<page>')
def Countries(url, page):
	items = sortedItems(url, page, 'countries')
	if xbmc.getSkinDir() == 'skin.heidi': return plugin.finish(items, view_mode = 55)
	else: return plugin.finish(items)

@ plugin.route('/search/')
def Search():
	keyb = plugin.keyboard(heading = 'Tìm kiếm')
	if keyb:
		searchUrl = ('http://xuongphim.tv/tim-kiem/keyword/trang-%s.html').replace('keyword', keyb).replace(' ', '-')
		searchRoute = '%s/search/%s/%s' % (addonID, urllib.quote_plus(searchUrl), 1)
		plugin.redirect(searchRoute)

@ plugin.route('/search/<url>/<page>')
def SearchResults(url, page):
	pageNumber = int(page) + 1
	pageContent = getUrl((url % page).replace('/trang-1.html','.html'))
	match = re.compile('<div class="tn-bxitem"><a href="(.+?)"[^>]*>.+?<img src="(.+?)"[^>]*>.+?<p class="bxitem-txt">(.+?)<\/p>').findall(pageContent)
	items = []
	for path, thumbnail, label in match:
		video = {}
		video["label"] = "[COLOR white]%s[/COLOR]" % (prettyText(label))
		video["thumbnail"] = thumbnail
		video["path"] = '%s/%s/%s' % (addonID, "episodes", urllib.quote_plus(domain + path))
		items.append(video)
	if len(items) == foundMax:
		items.append({'label': 'Next >>', 'path': '%s/search/%s/%s' % (addonID, urllib.quote_plus(url), pageNumber), 'thumbnail': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Go-next-grey.svg/360px-Go-next-grey.svg.png'})
	return plugin.finish(items)

@ plugin.route('/episodes/<url>')
def Episodes(url):
	pageContent = getUrl(url)
	episodeList = []
	if '#danhsach' in pageContent:
		match = re.compile('<ul class="tn-uldef">(.+?)<\/ul>').findall(pageContent)[0]
		elist = re.compile('<a title="(.+?)" .+? href="(.+?)">[^>]*<\/a>').findall(match)
		if len(elist) > 0:
			for ename, elink in elist:
				episode = {}
				episode["path"] = '%s/mirrors/%s' % (addonID, urllib.quote_plus(domain + elink))
				episode["label"] = "%s: [COLOR white] %s [/COLOR]" % ('Xem', ename)
				episodeList.append(episode)
			return episodeList
		else:
			return Mirrors(url)
	else:
		return Mirrors(url)

@ plugin.route('/mirrors/<url>')
def Mirrors(url):
	pageContent = getUrl(url)
	mirrorList = []
# Multiple mirrors / resolutions found
	if 'label:' in pageContent:
		mlist = re.compile('{file: "(.+?)",label: "(.+?)"').findall(pageContent)
		for mlink, mname in mlist:
			mirror = {}
			mirror["is_playable"] = True
			mirror["label"] = "%s: [COLOR white] %s [/COLOR]" % ('Nguồn'.decode('utf-8'), mname)
			if '.srt' in pageContent:
				match = re.compile('file: "(.+?)"').findall(pageContent)
				msubs = [s for s in match if '.srt' in str(s)][0]
			if '.vtt' in pageContent:
				match = re.compile('file: "(.+?)"').findall(pageContent)
				msubs = [s for s in match if '.vtt' in str(s)][0]
			else:
				msubs = 'None'
			mirror["path"] = '%s/play/%s/%s' % (addonID, urllib.quote_plus(mlink), urllib.quote_plus(msubs))
# Only one mirror found
	else:
		mlink = re.compile('{file: "(.+?)"').findall(pageContent)[0]
		mirror = {}
		mirror["is_playable"] = True
		mirror["label"] = "%s: [COLOR white] %s [/COLOR]" % ('Nguồn'.decode('utf-8'), 'AUTO')
		if '.srt' in pageContent:
			match = re.compile('file: "(.+?)"').findall(pageContent)
			msubs = [s for s in match if '.srt' in str(s)][0]
		if '.vtt' in pageContent:
			match = re.compile('file: "(.+?)"').findall(pageContent)
			msubs = [s for s in match if '.vtt' in str(s)][0]
		else:
			msubs = 'None'
		mirror["path"] = '%s/play/%s/%s' % (addonID, urllib.quote_plus(mlink), urllib.quote_plus(msubs))
	mirrorList.append(mirror)
# Adds friendly message when no mirrors found
	if mirrorList == []:
		mirror = {}
		mirror["is_playable"] = True
		mirror["path"] = '/'
		mirror["label"] = "[COLOR yellow] %s [/COLOR]" % ('<< Phim hiện không có nguồn <<'.decode('utf-8'))
		mirrorList.append(mirror)
	return mirrorList

@ plugin.route('/play/<url>/<subs>')
def Play(url, subs):
	dialogWait = xbmcgui.DialogProgress()
	dialogWait.create('Xem Phim 73', 'Đang tải. Xin chờ...')
	try:
		plugin.set_resolved_url(item=LoadVideos(url), subtitles=subs)
	except:
		xbmcgui.Dialog().ok('Xin lỗi','Nguồn phim hiện không xem được','Xin vui lòng thử nguồn khác') #############################################################
	dialogWait.close()
	del dialogWait

def LoadVideos(url):
	if 'youtube' in url:
		youtubeID = re.compile('watch\?v=(.*)').findall(url)[0]
		url = 'plugin://plugin.video.youtube/play/?video_id=%s' % youtubeID
# Gets redirected URL
	else:
		response = urllib2.urlopen(url)
		url = response.geturl()
	return url

def sortedItems(url, page, route_name):
	if page > 0:
		pageNumber = int(page)+1
		pageContent = getUrl(url % page)
	else:
		pageContent = url
	match = re.compile('<div class="tn-bxitem"><a href="(.+?)"[^>]*>.+?<img src="(.+?)"[^>]*>.+?<p class="name-vi">(.+?)<\/p><p class="name-en">(.+?)<\/p>.+?<div class="tn-contentdecs mb10">(.+?)<\/div>').findall(pageContent)
	items = []
	for path, thumbnail, label, label2, plot in match:
		video = {}
		video["label"] = "[COLOR white]%s[/COLOR] | %s" % (prettyText(label), prettyText(label2))
		video["thumbnail"] = thumbnail
		video["info"] = {"plot": prettyText(plot)}
		video["path"] = '%s/%s/%s' % (addonID, "episodes", urllib.quote_plus(domain + path))
		items.append(video)
	if len(items) == listMax:
		items.append({'label': 'Next >>', 'path': '%s/%s/%s/%s' % (addonID, route_name, urllib.quote_plus(url), pageNumber), 'thumbnail': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Go-next-grey.svg/360px-Go-next-grey.svg.png'})
	return items

def prettyText(src):
	src = src.strip()
	src = src.replace('&#39;',"'").replace('"s',"'s")
	src = src.replace('&quot;','"')
	return src

def getUrl(url):
	r = requests.get(url=url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, sdch'})
	response = r.text
	response = ''.join(response.splitlines()).replace('\'', '"')
	response = response.replace('\n', '')
	response = response.replace('\t', '')
	response = re.sub('  +', ' ', response)
	response = response.replace('> <', '><')
	return response

if __name__ == '__main__':
	plugin.run()