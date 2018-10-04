#!/usr/bin/python
# coding=utf8

import re, urllib2

def resolve(url):
	link = GetUrl(url)
	videourl = decodeOpenLoad(link)
	return videourl

def decodeOpenLoad(html):
    aastring = re.search(r"<video(?:.|\s)*?<script\s[^>]*?>((?:.|\s)*?)</script", html, re.DOTALL | re.IGNORECASE).group(1)
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟｰﾟ) + (ﾟΘﾟ))", "9")
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟｰﾟ))","8")
    aastring = aastring.replace("((ﾟｰﾟ) + (o^_^o))","7")
    aastring = aastring.replace("((o^_^o) +(o^_^o))","6")
    aastring = aastring.replace("((ﾟｰﾟ) + (ﾟΘﾟ))","5")
    aastring = aastring.replace("(ﾟｰﾟ)","4")
    aastring = aastring.replace("((o^_^o) - (ﾟΘﾟ))","2")
    aastring = aastring.replace("(o^_^o)","3")
    aastring = aastring.replace("(ﾟΘﾟ)","1")
    aastring = aastring.replace("(c^_^o)","0")
    aastring = aastring.replace("(ﾟДﾟ)[ﾟεﾟ]","\\")
    aastring = aastring.replace("(3 +3 +0)","6")
    aastring = aastring.replace("(3 - 1 +0)","2")
    aastring = aastring.replace("(1 -0)","1")
    aastring = aastring.replace("(4 -0)","4")
    decodestring = re.search(r"\\\+([^(]+)", aastring, re.DOTALL | re.IGNORECASE).group(1)
    decodestring = "\\+"+ decodestring
    decodestring = decodestring.replace("+","")
    decodestring = decodestring.replace(" ","")
    decodestring = decode(decodestring)
    decodestring = decodestring.replace("\\/","/")
    videourl = re.search(r'vr\s?=\s?"([^"]+)', decodestring, re.DOTALL | re.IGNORECASE).group(1)
    return videourl

def decode(encoded):
    for octc in (c for c in re.findall(r'\\(\d{2,3})', encoded)):
        encoded = encoded.replace(r'\%s' % octc, chr(int(octc, 8)))
    return encoded.decode('utf8')

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