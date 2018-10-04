# -*- coding: utf-8 -*-

import re
import urlparse
import urllib
import json
import api


class Source:
	def __init__(self, cache_path):
		self.cache_path = cache_path
		self.base_url = 'http://phim3s.net/'


	def __get_page__(self, url, cacheTime=3600000):
		return api.SOUPKit(cache_path=self.cache_path).SOUPFromURL(url, cacheTime=cacheTime)


	def base_url(self):
		return self.base_url


	def menu(self):
		page = self.__get_page__(self.base_url)
		menu = {}
		content = page.find('ul', {'class': 'container menu'})
		for li in content.children:
			a = li.find('a')
			if type(a) is int: continue
			submenu = []
			if 'href' in a.attrs and 'title' in a.attrs and a['href'] <> self.base_url and not a['href'].startswith('http'):
				submenu.append({'label': a.text.strip(), 'href': self.base_url + a['href'] + "?order_by=last_update"})
			sub_ul = li.find('ul', {'class': 'sub-menu'})
			if sub_ul <> None:
				for s in sub_ul.find_all('a'):
					submenu.append({'label': s.text.strip(), 'href': self.base_url + s['href'] + "?order_by=last_update"})
				if unicode(a.text) in menu:
					menu[unicode(a.text)].append(submenu)
				else:
					menu[unicode(a.text)] = submenu

		return menu


	def contents(self, url):
		page = self.__get_page__(url)
		contents = []
		temp = []
		for c in page.find_all('div', {'class': 'inner'}):
			a = c.find('a')
			href = self.base_url + a['href']
			if href in temp or href.startswith('clip'):
				continue
			temp.append(href)
			poster = a.find('img')['src']
			status = c.find('div', {'class': 'status'})
			if status <> None:
				status = status.text
			if status == 'Trailer':
				continue
			title1 = c.find('div', {'class': 'name'}).find('a').text
			title2 = c.find('div', {'class': 'name2'}).text

			contents.append({'title1': unicode(title1), 'title2': unicode(title2), 'href': href, 'duration': unicode(status), 'info': status, 'poster': poster})

		next_page = self.__next_page__(page)
		return {'items': contents, 'next_page': next_page}


	def media_items(self, url):
		page = self.__get_page__(url)
		poster = page.find('img', {'class': 'photo'})['src']
		title1 = page.find('span', {'class': 'fn'}).text
		title2 = page.find('div', {'class': 'name2 fr'}).find('h3').text

		watch = self.base_url + page.find('a', {'class': 'btn-watch'})['href']
		page = self.__get_page__(watch)

		media_items = {}
		serverList = page.find('div', {'class': 'serverlist'})
		if serverList <> None:
			for server in serverList.find_all('div', {'class': 'server'}):
				serverName = server.find('div', {'class': 'label'}).text
				streams = []
				for e in server.find('ul', {'class': 'episodelist'}).find_all('a'):
					href = '%sajax/episode/embed/?episode_id=%s' %(self.base_url, e['data-episode-id'])
					s = []
					ep_title = u''.join([u'Tập ', e.text])
					if ep_title in media_items:
						s = media_items[unicode(ep_title)]
					s.append({'title1': unicode(title1), 'title2': unicode(title2), 'ep_title': ep_title, 'poster': poster, 'banner': '', 'server_name': unicode(serverName), 'href': href})
					media_items[unicode(ep_title)] = s

		if media_items == {}:
			media_items['DEFAULT'] = [{'title1': unicode(title1), 'title2': unicode(title2), 'ep_title': '', 'poster': poster, 'banner': '', 'server_name': unicode('Server 1'), 'href': url}]
		return media_items


	def search(self, query):
		search_url = self.base_url + 'ajax/film/search?' + urllib.urlencode({'keyword': urllib.quote_plus(query)})
		result = api.JSONKit(cache_path=self.cache_path).ObjectFromURL(search_url, cacheTime=0)

		contents = []
		if 'json' in result:
			r = result['json']
			for i in r:
				m = r[i]
				contents.append({'title1': unicode(m['title']), 'title2': unicode(m['title_o']), 'href': self.base_url + m['link'], 'duration': unicode(m['status']), 'info': unicode(m['status']), 'poster': m['image_url']})
		return {'items': contents, 'next_page': None}


	def __next_page__(self, page):
		pages = page.find('span', {'class': 'page_nav'})
		if pages is None:
			return None
		n = pages.find('span', {'class': 'current'})
		if n is None:
			return None

		next_sib = n.nextSibling
		if next_sib <> None:
			n = next_sib.find('a')['href']
			return self.base_url + n
		return None


	def resolve_stream(self, url):
		result = api.JSONKit(cache_path=self.cache_path).ObjectFromURL(url, cacheTime=0, headers={'X-Requested-With': 'XMLHttpRequest'})
		url = '%s?%s' %(result['grabber'], urllib.urlencode({'link': result['video_url_hash'], 'json': 1}))

		result = api.JSONKit(cache_path=self.cache_path).ObjectFromURL(url, cacheTime=0)

		loc = None
		for c in result:
			if c['label'] == '720p':
				return c['file']
			elif c['label'] == '360p':
				locl = c['file']
		return loc



