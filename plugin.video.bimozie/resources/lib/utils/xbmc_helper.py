# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon
import os
import json
import re
import urlparse
import urllib

addon = xbmcaddon.Addon()
ADDON_ID = addon.getAddonInfo('id')
addon_data_dir = os.path.join(xbmc.translatePath('special://userdata/addon_data').decode('utf-8'), ADDON_ID)


def s2u(s): return s.decode('utf-8') if isinstance(s, str) else s


def getSetting(key):
    return addon.getSetting(key)


def has_file_path(filename):
    return os.path.exists(get_file_path(filename))


def get_file_path(filename):
    return os.path.join(addon_data_dir, filename)


def message(message='', title='', timeShown=5000):
    if message:
        title = ': [COLOR blue]%s[/COLOR]' % title if title else ''
        s0 = '[COLOR green][B]Bimozie[/B][/COLOR]' + title
        message = s2u(message)
        s1 = u'[COLOR %s]%s[/COLOR]' % ('red' if '!' in message else 'gold', message)
        message = u'XBMC.Notification(%s,%s,%s)' % (s0, s1, timeShown)
        xbmc.executebuiltin(message.encode("utf-8"))
    else:
        xbmc.executebuiltin("Dialog.Close(all, true)")


def write_file(name, content, binary=False):
    path = get_file_path(name)
    mode = 'w'
    if binary:
        mode = 'wb'
    f = open(path, mode=mode)
    f.write(content)
    f.close()
    return path


def read_file(name):
    content = None
    try:
        path = get_file_path(name)
        f = open(path, mode='r')
        content = f.read()
        f.close()
    except:
        pass
    return content


def search_history_save(search_key):
    if not search_key:
        return

    content = read_file('history.json')
    if content:
        content = json.loads(content)
    else:
        content = []

    idx = next((content.index(i) for i in content if search_key == i), -1)
    if idx >= 0 and len(content) > 0:
        del content[idx]
    elif len(content) >= 20:
        content.pop()

    content.insert(0, search_key)

    path = os.path.join(addon_data_dir, 'history.json')
    with open(path, 'w') as outfile:
        json.dump(content, outfile)


def search_history_clear():
    path = os.path.join(addon_data_dir, 'history.json')
    with open(path, 'w') as outfile:
        json.dump([], outfile)


def search_history_get():
    content = read_file('history.json')
    if content:
        content = json.loads(content)
    else:
        content = []

    return content


def wait(sec):
    xbmc.sleep(sec * 1000)


def convert_js_2_json(str):
    vstr = re.sub(r'(?<={|,)\s?([a-zA-Z][a-zA-Z0-9]*)(?=:)', r'"\1"', str)
    return json.loads(vstr)


def fixurl(url):
    # turn string into unicode
    if not isinstance(url, unicode):
        url = url.decode('utf8')

    # parse it
    parsed = urlparse.urlsplit(url)

    # divide the netloc further
    userpass, at, hostport = parsed.netloc.rpartition('@')
    user, colon1, pass_ = userpass.partition(':')
    host, colon2, port = hostport.partition(':')

    # encode each component
    scheme = parsed.scheme.encode('utf8')
    user = urllib.quote(user.encode('utf8'))
    colon1 = colon1.encode('utf8')
    pass_ = urllib.quote(pass_.encode('utf8'))
    at = at.encode('utf8')
    host = host.encode('idna')
    colon2 = colon2.encode('utf8')
    port = port.encode('utf8')
    path = '/'.join(  # could be encoded slashes!
        urllib.quote(urllib.unquote(pce).encode('utf8'), '')
        for pce in parsed.path.split('/')
    )
    query = urllib.quote(urllib.unquote(parsed.query).encode('utf8'), '=&?/')
    fragment = urllib.quote(urllib.unquote(parsed.fragment).encode('utf8'))

    # put it back together
    netloc = ''.join((user, colon1, pass_, at, host, colon2, port))
    return urlparse.urlunsplit((scheme, netloc, path, query, fragment))
