# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from utils.mozie_request import Request
from utils.mozie_request import AsyncRequest
from utils.pastebin import PasteBin
import re
import json


def from_char_code(*args):
    return ''.join(map(chr, args))


class Parser:
    def get_movie_link(self, response):
        soup = BeautifulSoup(response, "html.parser")
        return soup.select_one('div#ah-pif > div.ah-pif-head > div.ah-pif-ftool > div.ah-float-left > span > a').get(
            'href')

    def get(self, response, skipEps=False):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }
        soup = BeautifulSoup(response, "html.parser")
        # get all server list
        servers = soup.select("div.ah-wf-body > div.ah-wf-le")
        for server in servers:
            server_name = server.select_one('div.ah-le-server > span').text.strip().encode('utf-8')
            if server_name not in movie['group']: movie['group'][server_name] = []
            for ep in server.select('ul > li > a'):
                movie['group'][server_name].append({
                    'link': ep.get('href').encode('utf-8'),
                    'title': 'Episode %s' % ep.text.encode('utf-8'),
                })

        return movie

    def get_link(self, response):
        movie = {
            'group': {},
            'episode': [],
            'links': [],
        }

        sources = re.search("document.getElementById\('ah-player'\).innerHTML.*src=\"(.*)\"", response)
        if sources:
            movie['links'].append({
                'link': self.get_playlist(sources.group(1)),
                'title': 'Link hls',
                'type': 'hls',
                'resolve': True
            })
            return movie

        sources = re.search(r"<iframe.*?src=['|\"](.*?)['|\"]\s?", response)
        if sources:
            res = Request()
            vkey = re.search('key=(.*)', sources.group(1)).group(1)
            # http://vl.animehay.tv/initPlayer/f555b31844becd2e378d4978457014521af38ab8e66834ade1062b44827ef642
            resp = res.post('http://vl.animehay.tv/initPlayer/%s' % vkey)
            resp = json.loads(resp)

            if 'fembed' in resp['availablePlayers']:
                data = json.loads(res.post('http://vl.animehay.tv/getDataPlayer/%s/%s' % ('fembed', vkey)))
                data = res.get(data['data'])
                source = re.search(r"<iframe.*?src=['|\"](.*?)['|\"]\s?", data).group(1)

                movie['links'].append({
                    'link': source,
                    'title': 'Link fembed',
                    'type': 'mp4',
                    'resolve': False
                })
                
            if 'okru' in resp['availablePlayers']:
                data = json.loads(res.post('http://vl.animehay.tv/getDataPlayer/%s/%s' % ('okru', vkey)))
                data = res.get(data['data'])
                source = re.search(r"<iframe.*?src=['|\"](.*?)['|\"]\s?", data).group(1)

                movie['links'].append({
                    'link': source,
                    'title': 'Link okru',
                    'type': 'mp4',
                    'resolve': False
                })

            if 'openload' in resp['availablePlayers']:
                data = json.loads(res.post('http://vl.animehay.tv/getDataPlayer/%s/%s' % ('openload', vkey)))
                data = res.get(data['data'])
                source = re.search(r"<iframe.*?src=['|\"](.*?)['|\"]\s?", data).group(1)

                movie['links'].append({
                    'link': source,
                    'title': 'Link openload',
                    'type': 'mp4',
                    'resolve': False
                })

            return movie

        sources = re.search('<script rel="nofollow" src="(.*)" async>', response)
        response = Request().get(sources.group(1))
        sources = json.loads(re.search('links: (.*?),', response).group(1))

        if len(sources) > 0:
            for key, value in sources.items():
                if value:
                    label = key[1:].encode('utf-8')
                    movie['links'].append({
                        'link': value,
                        'title': 'Link %s' % label,
                        'type': label,
                        'resolve': True
                    })

            movie['links'] = sorted(movie['links'], key=lambda elem: int(elem['type']), reverse=True)

        return movie

    def get_playlist(self, url):
        resp = Request().get(url)
        params = re.search('this.urls=(\[.*?\]);', resp)
        params = json.loads(params.group(1))[0]

        data = {
            'url': params['url'],
            'bk_url': params['burl'],
            'pr_url': params['purl'],
            'ex_hls[]': params['exhls'],
            'v': 2,
            'len': 0,
            'prefer': 'https://dd.ntl.clhcdn.net',
            'ts': '1551437409204',
            'item_id': 'gu3d5A0S',
            'username': 'animehay'
        }

        url = 'http://ch.animehay.tv/content/parseUrl'
        resp = json.loads(Request().get(url, params=data))
        if not resp['hls']:
            sorted(resp['formats'].iterkeys(), reverse=True)
            movie_link = resp['formats'].itervalues().next()
            if Request().head(movie_link).status_code < 400:
                return movie_link
            else:
                data['err[pr][dr][]'] = 'https://redirector.googlevideo.com'
                data['err[pr][num]'] = len(resp['formats'])
                data['err[pr][dr_s]'] = resp['sig']
                resp = json.loads(Request().get(url, params=data))

                return self.create_effective_playlist(resp['formats'])
        else:
            return self.create_effective_playlist(resp['formats'])

    def create_effective_playlist(self, sources):
        r = "#EXTM3U\n#EXT-X-VERSION:3\n"
        for key, value in sources.items():
            if '720' in key:
                return self.get_stream(value)
                r += "#EXT-X-STREAM-INF:BANDWIDTH=1998000,RESOLUTION=1280x720\n"
                r += "%s\n" % self.get_stream(value)
                break
            if '480' in key:
                return self.get_stream(value)
                r += "#EXT-X-STREAM-INF:BANDWIDTH=996000,RESOLUTION=640x480\n"
                r += "%s\n" % value
                break
            if '360' in key:
                return self.get_stream(value)
                r += "#EXT-X-STREAM-INF:BANDWIDTH=394000,RESOLUTION=480x360\n"
                r += "%s\n" % value
                break

        url = PasteBin().dpaste(r, name='animiehay', expire=60)
        return url

    def get_stream(self, url):
        req = Request()
        r = req.get(url)
        str = ""
        links = []
        for line in r.splitlines():
            if len(line) > 0:
                if re.match('http', line):
                    links.append(line)
                str += '%s\n' % line

        arequest = AsyncRequest(request=req)
        results = arequest.head(links)
        for i in range(len(links)):
            try:
                str = str.replace(links[i], results[i].headers['Location '])
            except:
                pass

        url = PasteBin().dpaste(str, name='animiehay', expire=60)
        return url
