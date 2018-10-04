# -*- coding: utf-8 -*-

import urllib,urllib2,urlparse,xbmc,xbmcplugin,xbmcgui,xbmcaddon,sys
import HTTP
import player

try:
	import json
except:
	import simplejson as json

try:
	import StorageServer
except:
	import storageserverdummy as StorageServer


PLUGIN_ID = 'plugin.video.hieuhien.vn.zingtv'

# CACHING
cache = StorageServer.StorageServer(PLUGIN_ID, 3)
cache.table_name = PLUGIN_ID


action              = None
settings            = xbmcaddon.Addon(id=PLUGIN_ID)
xbmcplugin.setContent(int(sys.argv[1]), 'movies')


class main:
	COUNT = 25
	IMAGE_HOST = 'http://image.mp3.zdn.vn/'
	IMAGE_LARGE = 'http://image.mp3.zdn.vn/tv_media_1920_1080/'
	IMAGE_SMALL = 'http://image.mp3.zdn.vn/tv_media_210_120/'

	def __init__(self):
		global action
		params = {}
		splitparams = sys.argv[2][sys.argv[2].find('?') + 1:].split('&')
		for param in splitparams:
			if (len(param) > 0):
				splitparam = param.split('=')
				key = splitparam[0]
				try:    value = splitparam[1].encode("utf-8")
				except: value = splitparam[1]
				params[key] = value

		try:        action = urllib.unquote_plus(params["action"])
		except:     action = None
		try:        id = urllib.unquote_plus(params["id"])
		except:     id = None
		try:        page = urllib.unquote_plus(params["page"])
		except:     page = 1

		if action == None:                            self.main_menu()
		elif action == 'program':                     self.list_programs(id, int(page))
		elif action == 'program_info':                self.program_info(id)
		elif action == 'media':                       self.list_medias(id)
		elif action == 'play':                        self.play(id)
		elif action == 'Search':					  self.Search()


	def __build_url__(self, query):
		return sys.argv[0] + '?' + urllib.urlencode(query)


	def __request__(self, path, params={}, do_cache = True):
		cache_path = 'http://api.tv.zing.vn/3.0/%s?%s' %(path, urllib.urlencode(params))
		cached_result = cache.get(cache_path)

		if do_cache == True and cached_result <> None and cached_result <> '':
			return eval(cached_result)

		sparams = params.items() + {'os': 'android', 'app_version': 203, 'api_key': '7d3343b073f9fb9ec75e53335111dcc1', 'list_type': 'new', 'count': self.COUNT}.items()

		url = "http://api.tv.zing.vn/3.0/%s?%s" %(path, urllib.urlencode(sparams))
		proxy = None
		http_proxy = settings.getSetting('proxy')
		if http_proxy <> None and http_proxy <> '':
			proxy_username = settings.getSetting('proxy_username')
			proxy_password = settings.getSetting('proxy_password')
			if proxy_username <> None and proxy_username <> '':
				proxy = {'http': 'http://%s:%s@%s' %(urllib.quote(proxy_username), urllib.quote(proxy_password), http_proxy)}
			else:
				proxy = {'http': 'http://' + http_proxy }

		result = HTTP.Retrieve(url, proxy=proxy)
		result = json.loads(result)
		if do_cache == True:
			cache.set(cache_path, repr(result))
		return result


	def main_menu(self):
		xbmcplugin.setContent(int(sys.argv[1]), 'videos')

		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.__build_url__({'action': 'program', 'id': 82}),listitem=xbmcgui.ListItem(u'Phim Truyền Hình'),isFolder=True)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.__build_url__({'action': 'program', 'id': 78}),listitem=xbmcgui.ListItem(u'TV Show'),isFolder=True)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.__build_url__({'action': 'program', 'id': 83}),listitem=xbmcgui.ListItem(u'Hoạt Hình'),isFolder=True)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.__build_url__({'action': 'program', 'id': 86}),listitem=xbmcgui.ListItem(u'Hài Hước'),isFolder=True)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.__build_url__({'action': 'program', 'id': 87}),listitem=xbmcgui.ListItem(u'Giáo Dục'),isFolder=True)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.__build_url__({'action': 'program', 'id': 92}),listitem=xbmcgui.ListItem(u'Âm Nhạc'),isFolder=True)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.__build_url__({'action': 'program', 'id': 79}),listitem=xbmcgui.ListItem(u'Báo Chí'),isFolder=True)
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.__build_url__({'action': 'program', 'id': 81}),listitem=xbmcgui.ListItem(u'Thể Thao'),isFolder=True)

		#search
		item = xbmcgui.ListItem(u'Tìm Kiếm')
		xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=self.__build_url__({'action': 'Search'}), listitem=item, isFolder=True)

		xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)


	def list_programs(self, id, page = 1):
		params = {'genre_id': id, 'page': page}
		programs = self.__request__('program/list', params)

		total = 0
		if 'total' in programs:
			total = int(programs['total'])

		for p in programs['response']:
			item = xbmcgui.ListItem(unicode(p['name']))
			item.setArt({'poster': '%s%s' %(self.IMAGE_HOST, p['thumbnail']), 'fanart': '%s%s' %(self.IMAGE_HOST, p['thumbnail'])})
			item.setInfo('video', {'plot': p['duration']})
			xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.__build_url__({'action': 'program_info', 'id': p['id']}),listitem=item,isFolder=True)


		if self.COUNT * page < total:
			print "next page.... %d" %total
			xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.__build_url__({'action': 'program', 'id': id, 'page': page + 1}),listitem=xbmcgui.ListItem(u'Xem Them'),isFolder=True)
		xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)


	def program_info(self, id):
		series = self.__request__('program/info', {'program_id': id})
		if len(series['response']['series']) > 1:
			for s in series['response']['series']:
				item = xbmcgui.ListItem(unicode(s['name']))
				item.setArt({'poster': '%s%s' %(self.IMAGE_SMALL, s['thumbnail']), 'fanart': '%s%s' %(self.IMAGE_LARGE, s['thumbnail'])})
				item.setInfo('video', {'plot': '%d Video' %s['total']})
				xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.__build_url__({'action': 'media', 'id': s['id']}),listitem=item,isFolder=True)
			xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
		elif len(series['response']['series']) == 1:
			s = series['response']['series'][0]
			self.list_medias(s['id'])


	def list_medias(self, id):
		medias = self.__request__('series/medias', {'series_id': id})
		for m in medias['response']:
			ep_name = m['full_name']
			duration = m['duration']
			episode = m['episode']
			eid = m['id']
			title = m['program_name']
			thumbnail = m['thumbnail']
			item = xbmcgui.ListItem(unicode(ep_name))
			item.setArt({'poster': '%s%s' %(self.IMAGE_SMALL, thumbnail), 'fanart': '%s%s' %(self.IMAGE_LARGE, thumbnail)})
			xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=self.__build_url__({'action': 'play', 'id': eid}),listitem=item,isFolder=False)
		xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)


	def play(self, id):
		progress = xbmcgui.DialogProgress()
		progress.create(u'Đăng Tải Phim')

		try:
			media = self.__request__('media/info', {'media_id': id}, do_cache = False)
			info = media['response']
		finally:
			progress.close()
			del progress


		full_name = info['full_name']
		duration = info['duration']
		next_id = info['next_media_id']

		try:
			sub_title = info['sub_title']['vi']['src']
		except:
			sub_title = None

		file_url = info['file_url']

		other_url = info['other_url']
		quality = 'Video%s' %settings.getSetting('playback_quality')
		if quality in other_url:
			file_url = other_url[quality]

		if not file_url.startswith('http://'):
			file_url = 'http://' + file_url

		item = xbmcgui.ListItem(unicode(full_name))
		item.setArt({'poster': '%s%s' %(self.IMAGE_SMALL, info['program_thumbnail']), 'fanart': '%s%s' %(self.IMAGE_LARGE, info['program_thumbnail'])})
		if sub_title <> None and sub_title <> '':
			item.setSubtitles([sub_title])

		file_url = file_url.replace('android', 'web_flash')
		#player.player().play(file_url + '&start=0', item)
		xbmc.Player().play(file_url , item)



main()
