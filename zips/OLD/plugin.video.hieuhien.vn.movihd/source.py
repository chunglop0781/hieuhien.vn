# -*- coding: utf-8 -*-
import api
import urllib, urllib2
import re
from bs4 import BeautifulSoup
import json

class Source:
	def __init__(self, cache_path):
		self.cache_path = cache_path
		self.base_url = 'http://movihd.net/'


	def __get_page__(self, url, cacheTime=3600000):
		return api.SOUPKit(cache_path=self.cache_path).SOUPFromURL(url, cacheTime=cacheTime)


	def base_url(self):
		return self.base_url


	def menu(self):
		page = self.__get_page__(self.base_url)
		menu = {}
		content = page.find('nav', {'class': 'tn-gnav'}).find('ul')
		for li in content.children:
			a = li.find('a')
			if a <> None and not type(a) == int:
				href = self.base_url + a['href']
				label = a.text.strip()
				if not a['href'].startswith('javascript'):
					menu[unicode(label)] = href
				sub = li.find('div', {'class': 'gnavsub'})
				if sub <> None:
					sub_menu = []
					for a in sub.find_all('a'):
						href = self.base_url + a['href']
						if a['href'].startswith('/nam-'):
							label = u'NĂM'
						sub_label = a.text.strip()
						sub_menu.append({'href': href, 'label': sub_label})
					menu[unicode(label)] = sub_menu
		return menu


	def contents(self, url):
		page = self.__get_page__(url)
		items = []

		for li in page.find('ul', {'class': 'listfilmitem'}).find_all('div', {'class': re.compile('.*movie.*')}):
			a = li.find('a', {'class': 'film-name'})
			title1 = a.find('h2').text
			href = self.base_url + a['href']
			duration = li.find('span', {'class': 'episode'})
			if duration <> None:
				d = []
				for s in duration.stripped_strings:
					d.append(s)
				duration = u' '.join(d).strip()
			poster = self.base_url + li.find('img')['src']
			items.append({'title1': unicode(title1), 'title2': unicode(title1), 'href': href, 'duration': unicode(duration), 'info': '', 'poster': poster})


		return {'items': items, 'next_page': self.__next_page__(url, page)}


	def media_items(self, url):
		page = self.__get_page__(url, 300000)

		title = page.find('span', {'id': 'ctl00_ContentList_lbFilmDetail'}).find('h1').text
		title = title.split('-')
		if len(title) > 1:
			title1 = title[0].strip()
			title2 = title[1].strip()
		else:
			title1 = title[0].strip()
			title2 = title[0].strip()


		poster = self.base_url + page.find('img', {'class': 'thumb'})['src']
		banner = self.base_url + page.find('img', {'class': 'playerbg'})['src']

		media_items = {}

		section = page.find('div', {'class': 'section-title step'})
		if section <> None:
			for div in section.find_all('div', {'class': 'action left'}):
				name = unicode(div.find('span').text)
				for e in div.find_all('a'):
					ep_title = u''.join([u'Tập ', e.text.strip()])
					href = e['href']
					href = href[href.index("'")+1:href.rindex("'")]
					href = '%splaylist/%s.xml' %(self.base_url, href)
					s = []
					if ep_title in media_items:
						s = media_items[unicode(ep_title)]
					s.append({'title1': unicode(title1), 'title2': unicode(title2), 'ep_title': ep_title, 'poster': poster, 'banner': banner, 'server_name': unicode(name), 'href': href})
					media_items[unicode(ep_title)] = s

		if media_items == {}:
			href = page.find('div', {'class': 'playbutton'}).find('a')['href']
			href = href[href.index("'")+1:href.rindex("'")]
			href = '%splaylist/%s.xml' %(self.base_url, href)
			media_items[u'DEFAULT'] = [{'title1': unicode(title1), 'title2': unicode(title2), 'ep_title': '', 'poster': poster, 'banner': banner, 'server_name': unicode('Server 1'), 'href': href}]

		return media_items


	def search(self, query):
		search_url = self.base_url + 'instant-search'
		req = urllib2.Request(search_url)
		req.add_header('Content-Type', 'application/json; charset=UTF-8')
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
		response = urllib2.urlopen(req, json.dumps({'txt' : query}))
		content = response.read()
		content = api.JSONKit(cache_path=self.cache_path).ObjectFromString(content)

		data = BeautifulSoup(content['d'])
		items = []
		for a in data.find_all('a'):
			href = self.base_url + a['href']
			poster = self.base_url + a.find('img')['src']
			title = a.find_all('p', {'class': 'title'})
			title1 = title[0].text
			title2 = title[1].text

			items.append({'title1': unicode(title1), 'title2': unicode(title2), 'href': href, 'duration': '', 'info': '', 'poster': poster})
		return {'items': items, 'next_page': None}



	def __next_page__(self, url, page):
		pages = page.find('div', {'class': 'section-title pagination'})
		if pages is None:
			return None

		pages = pages.find_all('a')
		if pages is None or len(pages) == 0:
			return None

		i = re.search('(?i).*trang-(\\d+).*', url)
		if i:
			i = int(i.group(1))
		else:
			i = 1

		for a in pages:
			idx = re.search('(?i).*trang-(\\d+).*', a['href'])
			if idx:
				idx = int(idx.group(1))
				if i + 1 == idx:
					return self.base_url + a['href']
		return


	def resolve_stream(self, url):
		try:
			b = api.JSONKit(cache_path=self.cache_path).ObjectFromURL(url)['bitrates']
			max_rate = 0
			url = None
			for i in b:
				rate = i['bitrate']['bitrate_label'].replace('p', '')
				rate = int(rate)
				if rate > max_rate:
					max_rate = rate
					url = i['bitrate']['url_path']
			return url
		except:
			return None


