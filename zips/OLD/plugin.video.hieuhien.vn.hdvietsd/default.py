# -*- coding: utf-8 -*-

import urllib,urllib2,urlparse,xbmc,xbmcplugin,xbmcgui,xbmcaddon,sys,re
import HTTP

try:
	import json
except:
	import simplejson as json

try:
	import StorageServer
except:
	import storageserverdummy as StorageServer


PLUGIN_ID = 'plugin.video.hieuhien.vn.hdvietsd'

# CACHING
cache = StorageServer.StorageServer(PLUGIN_ID, 24)
cache.table_name = PLUGIN_ID

xbmcplugin.setContent(int(sys.argv[1]), 'movies')
action              = None


class hdviet:
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
		try:        categoryid = urllib.unquote_plus(params["categoryid"])
		except:     categoryid = None
		try:        offset = urllib.unquote_plus(params["offset"])
		except:     offset = 0
		try:        movie_id = urllib.unquote_plus(params["movie_id"])
		except:     movie_id = 0
		try:        episode = urllib.unquote_plus(params["episode"])
		except:     episode = 0


		if action == None:                            self.main_menu()
		elif action == 'list_movies':                 self.list_movies(categoryid, offset)
		elif action == 'play_movie':                  self.play_movie(movie_id, episode)
		elif action == 'list_seasons':                self.list_seasons(movie_id)
		elif action == 'list_episodes':               self.list_episodes(movie_id)
		elif action == 'Search':					  self.Search()


	def __request__(self, resource, query_params={}):
		url = 'https://api-v2.hdviet.com/%s' %resource
		if len(query_params) > 0:
			url = '%s?%s' %(url, urllib.urlencode(query_params))

		cached_result = cache.get(url)
		if cached_result <> None and cached_result <> '':
			return json.loads(cached_result)

		result = HTTP.Retrieve(url)
		cache.set(url, result)
		return json.loads(result)

	def __build_url__(self, query):
		return sys.argv[0] + '?' + urllib.urlencode(query)

	def main_menu(self):
		xbmcplugin.setContent(int(sys.argv[1]), 'videos')
		categories = self.__request__('category/menu?mini=1')['r']
		if categories <> None:
			for c in categories:
				item = xbmcgui.ListItem(c['CategoryName'])
				u = self.__build_url__({'action': 'list_movies', 'categoryid': c['CategoryID']})
				xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)

			#search
			item = xbmcgui.ListItem(u'Tìm Kiếm')
			xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=self.__build_url__({'action': 'Search'}), listitem=item, isFolder=True)

			xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)


	def play_movie(self, movieid, episode=0):
		query_params = {'movieid': movieid, 'ep': episode}

		url = 'https://api-v2.hdviet.com/movie/play'
		if len(query_params) > 0:
			url = '%s?%s' %(url, urllib.urlencode(query_params))

		cached_result = cache.get(url)
		if cached_result is None or cached_result == '':
			try:
				progress = xbmcgui.DialogProgress()
				progress.create(u'Đang Tải Phim')
				d = self.__request__('movie/play', query_params)['r']
			finally:
				progress.close()
				del progress
		else:
			d = json.loads(cached_result)['r']

		name = d['MovieName']
		link = d['LinkPlay']
		if len(link) == 0:
			link = d['LinkPlayBackup']
		subtitles = []
		for m in d:
			if 'Subtitle' in m:
				for s in d[m]:
					if s == 'VIE':
						sub = d[m][s]['Source']
						if len(sub) > 0:
							subtitles.append(sub)
		#if int(episode) > 0:
		#    name = unicode.join(u'',[name, ' - ', u'Tập', ' ', episode])
		item = xbmcgui.ListItem(name)
		item.setSubtitles(subtitles)
		xbmc.Player().play(link, item)


	def list_movies(self, categoryid, offset, limit=20):
		query_params = {'categoryid': categoryid, 'offset': offset, 'limit': limit}
		p = re.compile('\(Season\s+\d+\)')
		movies = self.__request__('movie', query_params)['r']
		if movies <> None and 'Movies' in movies:
			total = 0
			if 'Total' in movies:
				total = int(movies['Total'])
			for m in movies['Movies']:
				_id = m['MovieID']
				name = m['MovieName']
				name = p.sub('', name).strip()
				aka = m['KnownAs']
				trailer = m['Trailer']
				poster = m['Poster']
				if 'Poster214x321' in m:
					poster = m['Poster214x321']
				runtime      = m['Runtime']
				plot         = m['PlotVI']
				rating       = m['ImdbRating']
				country      = m['Country']
				release_date = m['ReleaseDate']
				backdrop     = m['Backdrop']
				banner       = m['Banner']
				num_episodes = m['Episode']
				item = xbmcgui.ListItem(name)
				item.setInfo(type="Video", infoLabels={"Label": name, "Title": name, "Plot": plot, 'Year': release_date})
				item.setArt({'poster': poster, 'thumb': poster})
				item.setProperty("Fanart_Image", backdrop)
				if num_episodes == "0":
					u = self.__build_url__({'action': 'play_movie', 'movie_id': _id, 'episode': 0})
					isFolder = False
				else:
					if 'Season' in m and len(m['Season']) > 1:
						u = self.__build_url__({'action': 'list_seasons', 'movie_id': _id})
					else:
						u = self.__build_url__({'action': 'list_episodes', 'movie_id': _id})
					isFolder = True
				xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=isFolder)

			if int(offset) < total:
				u = self.__build_url__({'action': 'list_movies', 'categoryid': categoryid, 'offset': int(offset) + int(limit), 'limit': limit})
				item = xbmcgui.ListItem('Xem thêm')
				xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=isFolder)
			xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

	def list_seasons(self, movie_id):
		xbmcplugin.setContent(int(sys.argv[1]), 'seasons')
		query_params = {'movieid': movie_id}
		seasons = self.__request__('movie/getallseason', query_params)['r']
		if seasons <> None:
			for s in seasons:
				info = seasons[s]
				_id     = info['MovieID']
				moviename = info['MovieName']
				episode = info['Episode']
				poster  = info['Poster']
				backdrop = info['Backdrop']
				u = self.__build_url__({'action': 'list_episodes', 'movie_id': _id})
				item = xbmcgui.ListItem(moviename)
				item.setArt({'poster': poster, 'thumb': poster})
				item.setProperty("Fanart_Image", backdrop)
				xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=True)
			xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

	def list_episodes(self, movie_id):
		xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
		query_params = {'movieid': movie_id}
		m = self.__request__('movie', query_params)['r']
		_id = m['MovieID']
		name = m['MovieName']
		aka = m['KnownAs']
		trailer = m['Trailer']
		poster = m['Poster']
		if 'Poster214x321' in m:
			poster = m['Poster214x321']
		runtime      = m['Runtime']
		plot         = m['PlotVI']
		rating       = m['ImdbRating']
		country      = m['Country']
		release_date = m['ReleaseDate']
		backdrop     = m['Backdrop']
		banner       = m['Banner']
		num_episodes = m['Episode']
		thumbs = sorted(m['Thumbs'].keys(), key=lambda x: int(x))
		for thumb in thumbs:
			t = unicode.join(u'',[u'Tập', ' ', thumb])
			item = xbmcgui.ListItem(t)
			item.setInfo(type="Video", infoLabels={"Label": name, "Title": t, "Plot": plot, 'Year': release_date})
			epThumb = m['Thumbs'][thumb]
			item.setArt({'poster': epThumb, 'thumb': epThumb})
			item.setProperty("Fanart_Image", backdrop)
			u = self.__build_url__({'action': 'play_movie', 'movie_id': _id, 'episode': thumb})
			xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=item,isFolder=False)
		xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)

hdviet()
