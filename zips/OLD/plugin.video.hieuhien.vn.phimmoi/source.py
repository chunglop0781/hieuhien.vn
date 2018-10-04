# -*- coding: utf-8 -*-
import api
import urllib
import urlparse
import re


class Source:
	def __init__(self, cache_path):
		self.cache_path = cache_path
		self.base_url = 'http://www.phimmoi.net/'


	def __get_page__(self, url, cacheTime=3600000):
		return api.SOUPKit(cache_path=self.cache_path).SOUPFromURL(url, cacheTime=cacheTime)


	def base_url(self):
		return self.base_url


	def menu(self):
		page = self.__get_page__(self.base_url)
		menu = {}
		content = page.find('ul', {'id': 'mega-menu-1'})
		for li in content.children:
			a = li.find('a')
			label = unicode(a.text.strip())
			if 'href' in a.attrs:
				rel_link = a['href']
				if rel_link == './':
					rel_link = ''
				elif rel_link == 'trailer/':
					continue
				menu[label] = self.base_url + rel_link
			else:
				sub_ul = li.find('ul')
				sub_menu = []
				if sub_ul <> None:
					for sa in sub_ul.find_all('a'):
						rel_link = sa['href']
						if rel_link == './':
							rel_link = ''
						sub_menu.append({'href': self.base_url + rel_link, 'label': unicode(sa.text)})
					menu[label] = sub_menu
		return menu


	def contents(self, url):
		page = self.__get_page__(url)
		items = []
		duplicates = []
		sections = page.find_all('div', {'class': 'movie-list-index home-v2'})
		for section in sections:
			for a in section.select('li > a'):
				href = self.base_url + a['href']
				title1 = a.find('div', {'class': 'movie-title-1'}).text
				title2 = a.find('span', {'class': 'movie-title-2'}).text
				duration = a.find('span', {'class': 'movie-title-chap'}).text
				info = a.find('span', {'class': 'ribbon'}).text
				poster = a.find('div', {'class': 'public-film-item-thumb'})
				if poster <> None:
					poster = poster['style']
					poster = poster[poster.index("(") + 1 : poster.index(")")]
					poster = poster.replace("'", "")
				if not href in duplicates:
					duplicates.append(href)
					items.append({'title1': unicode(title1), 'title2': unicode(title2), 'href': href, 'duration': unicode(duration), 'info': unicode(info), 'poster': poster})
		tabs = page.find('div', {'id': 'tabs-movie'})
		if tabs <> None:
			for li in tabs.find_all('li', {'class': 'movie'}):
				a = li.find('a')
				href = self.base_url + a['href']
				duration = li.find('div', {'class': 'eps'}).text
				title1 = a.find('span', {'class': 'name-vn'}).text
				title2 = a.find('span', {'class': 'name-en'}).text
				poster = a.find('div', {'class': 'thumbn'})
				if poster <> None:
					poster = poster['style']
					poster = poster[poster.index("(") + 1 : poster.index(")")]
					poster = poster.replace("'", "")
				if not href in duplicates:
					duplicates.append(href)
					items.append({'title1': unicode(title1), 'title2': unicode(title2), 'href': href, 'duration': unicode(duration), 'info': unicode(info), 'poster': poster})
		for a in page.find_all('li', {'class': 'movie-item'}):
			href = self.base_url + a.find('a')['href']
			title1 = a.find('span', {'class': 'movie-title-1'}).text
			title2 = a.find('span', {'class': 'movie-title-2'}).text
			duration = a.find('span', {'class': 'movie-title-chap'}).text
			info = a.find('span', {'class': 'ribbon'})
			if info <> None:
				info = info.text
			else:
				info = ''
			poster = a.find('div', {'class': 'movie-thumbnail'})
			if poster <> None:
				poster = poster['style']
				poster = poster[poster.index("(") + 1 : poster.index(")")]
				poster = poster.replace("'", "")
			if not href in duplicates:
					duplicates.append(href)
					items.append({'title1': unicode(title1), 'title2': unicode(title2), 'href': href, 'duration': unicode(duration), 'info': unicode(info), 'poster': poster})

		next_page = self.__next_page__(page)
		return {'items': items, 'next_page': next_page}


	def media_items(self, url):
		page = self.__get_page__(url, 300000)

		watch = page.find('a', {'id': 'btn-film-watch'})
		if watch == None:
			return {}
		watch = self.base_url + watch['href']
		page = self.__get_page__(watch, 300000)

		poster = page.find('div', {'class': 'movie-l-img'}).find('img')['src']
		banner = None


		info = page.find('h1', {'class': 'movie-title'})
		title1 = info.find('span', {'class': 'title-1'}).text.replace('Xem phim', '').strip()
		title2 = info.find('span', {'class': 'title-2'}).text.replace('Xem phim', '').strip()
		isSeries = False
		for s in page.find_all('script'):
			m = re.search("(?i)filmInfo.isSeries=(.*)", s.text)
			if m:
				text = m.group(1)
				text = text[text.index('(') + 1 : text.index(')')]
				isSeries = eval(text)
		media_items = {}
		if isSeries:
			servers_list = page.find('div', {'class': 'list-server'})
		else:
			servers_list = page.find('ul', {'class': 'server-list'})

		if servers_list <> None:
			for s in servers_list.find_all('ul', {'class': 'list-episode'}):
				name = s.previous_sibling
				if name <> None:
					name = name.text.strip()
					name = name.replace('\r', '').replace('\n', '')

				for e in s.find_all('a'):
					ep_title = e.text.strip()
					ep_title = ep_title.replace('\r', '').replace('\n', '')
					if isSeries:
						ep_title = u''.join([u'Tập ', ep_title])
					else:
						ep_title = u''.join([u'Phần ', ep_title])
					ep_num = e['data-number']
					ep_part = e['data-part']
					href = self.base_url + e['href']
					s = []
					if ep_title in media_items:
						s = media_items[unicode(ep_title)]
					s.append({'title1': unicode(title1), 'title2': unicode(title2), 'ep_title': ep_title, 'poster': poster, 'banner': banner, 'server_name': unicode(name), 'href': href})
					media_items[unicode(ep_title)] = s

		if media_items == {}:
			media_items[u'DEFAULT'] = [{'title1': unicode(title1), 'title2': unicode(title2), 'ep_title': '', 'poster': poster, 'banner': banner, 'server_name': unicode('Server 1'), 'href': watch}]

		return media_items


	def search(self, query):
		term = urllib.quote_plus(query)
		search_url = self.base_url + 'tim-kiem/%s/' %term
		return self.contents(search_url)


	def __next_page__(self, page):
		pages = page.find('ul', {'class': 'pagination pagination-lg'})
		if pages is None:
			return None

		pages = pages.find_all('a')
		if page is None or len(pages) == 0:
			return None

		return self.base_url + pages[len(pages) - 1]['href']


	def resolve_stream(self, url):
		page = self.__get_page__(url, cacheTime=0)
		new_url = self.__get_stream__(page)
		headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36', 'Referer': url}
		res = api.JSONKit(cache_path=self.cache_path).ObjectFromURL(new_url, cacheTime=0, headers=headers)

		medias = res['medias']

		for m in medias:
			if m['resolution'] in [1080, 720]:
				if self.__is_youtube_url__(m['url']):
					return self.__get_youtube_stream__(m['url'])
				else:
					return m['url']

		u = medias[0]['url']
		if self.__is_youtube_url__(u):
			return self.__get_youtube_stream__(u)
		else:
			return u


	def __get_stream__(self, page):
		for s in page.find_all('script', {'async': 'true'}):
			if 'token' in s['src']:
				return s['src'].replace('javascript', 'json')
		return None


	def __get_youtube_stream__(self, url):
		vid = self.__get_video_id__(url)
		data =api.HTTPKit(cache_path=self.cache_path).Request('http://www.youtube.com/get_video_info?&video_id=' + vid, cacheTime=1000*60*5).content

		argsMap = {}
		for args in data.split('&'):
			val = args.split('=')
			if len(val) >= 2:
				argsMap[val[0]] = urllib.unquote(val[1])

		streams = {}
		if 'url_encoded_fmt_stream_map' in argsMap:
			for s in argsMap['url_encoded_fmt_stream_map'].split(','):
				query = urlparse.parse_qs(s)
				streams[int(query['itag'][0])] = query['url'][0]

		for s in [37, 22, 18]:
			if s in streams:
				return streams[s]
		return streams.itervalues().next()

	def __is_youtube_url__(self, url):
		r = re.compile('^.*((youtu.be\\/)|(v\\/)|(\\/u\\/w\\/)|(embed\\/)|(watch\\?))\\??v?=?([^#\\&\\?]*).*')
		m = r.match(url)
		if m:
			return True
		return False


	def __get_video_id__(self, url):
		qs = urlparse.parse_qs(url[url.index('?')+1:])
		return qs['v'][0]

