# -*- coding: utf-8 -*-

import cookielib
import urllib2




def BuildOpener(proxy = None):
	cookies = cookielib.LWPCookieJar()
	handlers = [urllib2.HTTPHandler(), urllib2.HTTPSHandler(), urllib2.HTTPCookieProcessor(cookies)]

	if proxy <> None:
		handlers += [urllib2.ProxyHandler(proxy)]

	opener = urllib2.build_opener(*handlers)
	try:
		if sys.version_info < (2, 7, 9): raise Exception()
		import ssl; ssl_context = ssl.create_default_context()
		ssl_context.check_hostname = False
		ssl_context.verify_mode = ssl.CERT_NONE
		handlers += [urllib2.HTTPSHandler(context=ssl_context)]
		opener = urllib2.build_opener(*handlers)
		opener = urllib2.install_opener(opener)
	except:
		pass

	return opener



def Retrieve(url, proxy=None, post=None, headers=None, mobile=True, cookie=None, timeout=10):
	opener = BuildOpener(proxy)

	#append headers
	_headers = {}
	if headers <> None:
		_headers.update(headers)

	#user agent handling, respect the one given in headers
	if 'User-Agent' not in _headers:
		if mobile:
			_headers['User-Agent'] = 'Apple-iPhone/701.341'
		else:
			_headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0'

	#add cookie, respect the one given in the headers
	if 'Cookie' not in _headers and cookie <> None:
		_headers['Cookie'] = cookie

	#add headers
	h = []
	for k, v in _headers.iteritems():
		h.append((k, v))
	opener.addheaders = h

	#send and read
	if post <> None:
		response = opener.open(url, post, timeout=timeout)
	else:
		response = opener.open(url, timeout=timeout)
	result = response.read()

	#close and return
	response.close()
	return result




